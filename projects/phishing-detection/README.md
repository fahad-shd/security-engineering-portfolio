# Phishing Website Detection using Machine Learning

A small end-to-end demonstration that extracts lexical URL indicators, trains a Scikit-learn Random Forest classifier, exposes a Flask JSON API, and provides a simple review dashboard.

## Important data and model caveat
The included CSV is a **synthetic teaching dataset** using reserved `.test` domains and illustrative URLs. It is not a representative corpus of live phishing campaigns. Metrics produced from it are only a pipeline smoke test and must not be presented as real-world detection accuracy. URL-only classification is inherently limited: it cannot verify page content, domain reputation, certificate validity, redirect destinations, or current threat intelligence.

## Run locally
Python 3.10+.

```bash
python -m venv .venv
pip install -r requirements.txt
python train_model.py
python app.py
```
Open `http://127.0.0.1:5000`.

## API
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://account-check.example.test/login"}'
```
Response includes the predicted class, phishing probability, and extracted indicators. The API accepts only HTTP(S) URLs and does not fetch or visit submitted URLs.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Docker
```bash
docker build -t url-risk-demo .
docker run --rm -p 5000:5000 url-risk-demo
```
The Docker image trains the demo model at build time. For production, use a reviewed, versioned dataset and model artifact, add authentication/rate limiting, structured audit logging, model monitoring, and threat-intelligence enrichment.

## Responsible use
This tool performs static string analysis only. It does not open URLs, crawl websites, submit credentials, or interact with suspicious infrastructure. Treat outputs as triage signals, not definitive verdicts.