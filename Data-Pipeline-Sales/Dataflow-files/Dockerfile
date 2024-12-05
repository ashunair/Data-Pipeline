FROM python:3.9-slim

WORKDIR /app

COPY dataflow_pipeline.py /app
COPY requirements.txt /app
COPY data-pipleine-keys.json /app
RUN pip install --no-cache-dir -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/data-pipleine-keys.json

CMD ["python", "dataflow_pipeline.py"]
