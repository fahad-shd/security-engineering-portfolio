FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY detector.py signatures.json ./
USER 10001
ENTRYPOINT ["python", "detector.py"]
CMD ["--once"]
