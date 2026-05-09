FROM python:3.11-slim
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "scan.py"]
