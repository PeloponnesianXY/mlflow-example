FROM python:3.12-slim

WORKDIR /app

COPY requirements-docker.txt .

RUN pip install --no-cache-dir -r requirements-docker.txt

COPY train.py .
COPY wine-quality.csv .
COPY mlflow_local.py .
COPY mlflow.db .
COPY mlruns ./mlruns

CMD ["python", "train.py"]
