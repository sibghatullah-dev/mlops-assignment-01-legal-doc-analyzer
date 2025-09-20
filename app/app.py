# app/app.py
import torch
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the fine-tuned model and tokenizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")


def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(
        os.path.join(MODEL_PATH, "config.json")
    ):
        logger.error(
            f"Model not found at {MODEL_PATH}. Please train the model first using train.py"
        )
        # Fall back to the base model if trained model isn't available
        logger.info("Loading base legal-bert model instead...")
        return AutoTokenizer.from_pretrained(
            "nlpaueb/legal-bert-base-uncased"
        ), AutoModelForSequenceClassification.from_pretrained(
            "nlpaueb/legal-bert-base-uncased", num_labels=2
        )

    logger.info(f"Loading model from {MODEL_PATH}")
    return AutoTokenizer.from_pretrained(
        MODEL_PATH
    ), AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)


tokenizer, model = load_model()
model.eval()


def analyze_contract(text):
    # Preprocess and tokenize
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=256
    )
    # Model inference
    with torch.no_grad():
        outputs = model(**inputs)
    # Simple thresholding for risk (this is illustrative)
    risk_score = torch.softmax(outputs.logits, dim=1)[0][1].item()
    flagged = risk_score > 0.5
    explanation = "Clause appears risky." if flagged else "Clause seems safe."
    return {"risk_score": risk_score, "flagged": flagged, "explanation": explanation}


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "contract_text" not in data:
        return jsonify({"error": "Please provide contract_text in JSON payload."}), 400
    result = analyze_contract(data["contract_text"])
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
