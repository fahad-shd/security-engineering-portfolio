from pathlib import Path
from collections import deque
import joblib
from flask import Flask, jsonify, render_template, request
from features import extract_features

BASE = Path(__file__).parent
MODEL_PATH = BASE / "model.joblib"
app = Flask(__name__)
history = deque(maxlen=100)

def load_model():
    if not MODEL_PATH.exists():
        raise RuntimeError("Model not found. Run python train_model.py first.")
    return joblib.load(MODEL_PATH)

@app.get("/")
def index():
    return render_template("index.html", recent=list(history))

@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    url = payload.get("url")
    if not isinstance(url, str):
        return jsonify({"error": "JSON body must include a string 'url'"}), 400
    try:
        features = extract_features(url)
        bundle = load_model()
        vector = [[features[name] for name in bundle["feature_names"]]]
        model = bundle["model"]
        prediction = int(model.predict(vector)[0])
        probabilities = model.predict_proba(vector)[0]
        result = {
            "url": url,
            "prediction": "phishing" if prediction == 1 else "legitimate",
            "phishing_probability": round(float(probabilities[list(model.classes_).index(1)]), 4),
            "features": features,
            "disclaimer": "Synthetic-demo model; use as a triage signal, not a verdict."
        }
        history.appendleft(result)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503

@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_available": MODEL_PATH.exists()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
