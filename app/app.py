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
    """Load the trained model or fallback to base model for testing"""
    try:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(
            os.path.join(MODEL_PATH, "config.json")
        ):
            logger.warning(
                f"Model not found at {MODEL_PATH}. Using mock model for testing..."
            )
            # Return None for testing environments
            return None, None

        logger.info(f"Loading model from {MODEL_PATH}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        return tokenizer, model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.info("Using mock model for testing...")
        return None, None


# Initialize model (will be None in testing environment)
tokenizer, model = load_model()
if model is not None:
    model.eval()


def analyze_contract(text):
    """Analyze contract text for risk assessment"""
    # Handle mock model for testing
    if tokenizer is None or model is None:
        logger.info("Using mock analysis for testing")
        # Return mock results for testing
        return {
            "risk_score": 0.3,
            "flagged": False,
            "explanation": "Mock analysis - model not loaded"
        }
    
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
