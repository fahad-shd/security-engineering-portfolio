"""Train and evaluate the demo model on the bundled synthetic dataset."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from features import extract_features

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "urls.csv"
MODEL = ROOT / "model.joblib"
METRICS = ROOT / "metrics.json"

def train() -> dict:
    frame = pd.read_csv(DATA)
    required = {"url", "label"}
    if not required.issubset(frame.columns):
        raise ValueError("dataset must contain url,label columns")
    X = pd.DataFrame([extract_features(url) for url in frame["url"]])
    y = frame["label"].astype(int)
    if set(y.unique()) != {0, 1} or y.value_counts().min() < 2:
        raise ValueError("dataset must contain at least two examples per class (0=legitimate, 1=phishing)")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, max_depth=8,
                                   class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = {
        "dataset_type": "synthetic educational data",
        "samples": int(len(frame)),
        "test_samples": int(len(y_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "classification_report": classification_report(
            y_test, predictions, output_dict=True, zero_division=0
        ),
        "warning": "Not a real-world performance estimate."
    }
    joblib.dump({"model": model, "feature_names": list(X.columns)}, MODEL)
    METRICS.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics

if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
