# app/app.py
import torch
from flask import Flask, request, jsonify, render_template_string
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


# HTML template for the home page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legal Document Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .input-section {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #555;
            font-weight: 600;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 150px;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 10px;
            display: none;
        }
        .result.safe {
            background: #d4edda;
            border: 2px solid #28a745;
        }
        .result.risky {
            background: #f8d7da;
            border: 2px solid #dc3545;
        }
        .result h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        .result.safe h3 {
            color: #155724;
        }
        .result.risky h3 {
            color: #721c24;
        }
        .result p {
            margin: 10px 0;
            font-size: 1.1em;
        }
        .risk-score {
            font-size: 2em;
            font-weight: bold;
            margin: 15px 0;
        }
        .loading {
            text-align: center;
            display: none;
            margin-top: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .examples {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .examples h4 {
            color: #555;
            margin-bottom: 10px;
        }
        .example-btn {
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #667eea;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        .example-btn:hover {
            background: #764ba2;
        }
        .api-info {
            margin-top: 30px;
            padding: 20px;
            background: #e9ecef;
            border-radius: 10px;
            font-size: 14px;
        }
        .api-info h4 {
            margin-bottom: 10px;
            color: #333;
        }
        .api-info code {
            background: #fff;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .api-info pre {
            background: #fff;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚖️ Legal Document Analyzer</h1>
        <p class="subtitle">AI-powered contract risk analysis using LegalBERT</p>
        
        <div class="input-section">
            <label for="contractText">Enter Contract Text:</label>
            <textarea id="contractText" placeholder="Paste your contract clause here..."></textarea>
        </div>
        
        <button onclick="analyzeContract()" id="analyzeBtn">Analyze Contract</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing contract...</p>
        </div>
        
        <div class="result" id="result"></div>
        
        <div class="examples">
            <h4>📝 Try Example Clauses:</h4>
            <span class="example-btn" onclick="useExample(0)">Indemnification</span>
            <span class="example-btn" onclick="useExample(1)">Standard Agreement</span>
            <span class="example-btn" onclick="useExample(2)">Liability Limitation</span>
            <span class="example-btn" onclick="useExample(3)">Governing Law</span>
        </div>
        
        <div class="api-info">
            <h4>🔌 API Endpoint</h4>
            <p>You can also use the API directly:</p>
            <pre><code>curl -X POST http://localhost:5000/analyze \\
  -H "Content-Type: application/json" \\
  -d '{"contract_text": "Your contract text here"}'</code></pre>
        </div>
    </div>
    
    <script>
        const examples = [
            "The party agrees to indemnify and hold harmless the other party from all claims, damages, and liabilities.",
            "This agreement constitutes the entire agreement between the parties and supersedes all prior agreements.",
            "In no event shall either party be liable for any indirect, incidental, or consequential damages.",
            "This agreement shall be governed by and construed in accordance with the laws of the State of California."
        ];
        
        function useExample(index) {
            document.getElementById('contractText').value = examples[index];
        }
        
        async function analyzeContract() {
            const text = document.getElementById('contractText').value.trim();
            const resultDiv = document.getElementById('result');
            const loadingDiv = document.getElementById('loading');
            const analyzeBtn = document.getElementById('analyzeBtn');
            
            if (!text) {
                alert('Please enter some contract text to analyze.');
                return;
            }
            
            // Show loading
            loadingDiv.style.display = 'block';
            resultDiv.style.display = 'none';
            analyzeBtn.disabled = true;
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ contract_text: text })
                });
                
                const data = await response.json();
                
                // Hide loading
                loadingDiv.style.display = 'none';
                analyzeBtn.disabled = false;
                
                // Display result
                const riskPercentage = (data.risk_score * 100).toFixed(2);
                const isSafe = !data.flagged;
                
                resultDiv.className = 'result ' + (isSafe ? 'safe' : 'risky');
                resultDiv.innerHTML = `
                    <h3>${isSafe ? '✅ Low Risk' : '⚠️ High Risk'}</h3>
                    <div class="risk-score" style="color: ${isSafe ? '#28a745' : '#dc3545'}">
                        Risk Score: ${riskPercentage}%
                    </div>
                    <p><strong>Analysis:</strong> ${data.explanation}</p>
                    <p><strong>Status:</strong> ${data.flagged ? 'Flagged for review' : 'Appears safe'}</p>
                `;
                resultDiv.style.display = 'block';
                
            } catch (error) {
                loadingDiv.style.display = 'none';
                analyzeBtn.disabled = false;
                alert('Error analyzing contract: ' + error.message);
            }
        }
        
        // Allow Enter key to submit (with Shift+Enter for new line)
        document.getElementById('contractText').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                analyzeContract();
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    """Home page with web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or "contract_text" not in data:
        return jsonify({"error": "Please provide contract_text in JSON payload."}), 400
    result = analyze_contract(data["contract_text"])
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
