import json
import os
import torch
import logging
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load CUAD dataset (assumes JSON format with 'text' and 'label' keys)
def load_data(data_path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found at {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    labels = []

    for document in data["data"]:
        for paragraph in document["paragraphs"]:
            # Each paragraph contains text in 'context' and QAs
            context = paragraph["context"]

            # Determine if there are any positive answers in the QAs
            has_risk = 0
            for qa in paragraph["qas"]:
                if qa["answers"] and len(qa["answers"]) > 0:
                    has_risk = 1
                    break

            texts.append(context)
            labels.append(has_risk)

    logger.info(f"Loaded {len(texts)} text samples with {sum(labels)} positive cases")
    return texts, labels


def preprocess_data(texts, labels, tokenizer, max_length=256):
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
    dataset = torch.utils.data.TensorDataset(
        torch.tensor(encodings["input_ids"]),
        torch.tensor(encodings["attention_mask"]),
        torch.tensor(labels),
    )
    return dataset


def save_model(trainer, model, tokenizer):
    # Create model directory if it doesn't exist
    model_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "app", "model")
    )
    os.makedirs(model_dir, exist_ok=True)

    logger.info(f"Saving model to {model_dir}")
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)
    logger.info("Model and tokenizer saved successfully")


def main():
    data_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "CUADv1.json")
    )
    logger.info(f"Loading data from: {data_file}")
    texts, labels = load_data(data_file)

    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # Load tokenizer and model
    model_name = "nlpaueb/legal-bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # Tokenize data
    train_encodings = tokenizer(
        train_texts, truncation=True, padding=True, max_length=256
    )
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)

    class ContractDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    train_dataset = ContractDataset(train_encodings, train_labels)
    val_dataset = ContractDataset(val_encodings, val_labels)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_strategy="epoch",
        save_steps=10_000,
        save_total_limit=2,
        logging_dir="./logs",
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # Train and save model
    trainer.train()
    save_model(trainer, model, tokenizer)


if __name__ == "__main__":
    main()
