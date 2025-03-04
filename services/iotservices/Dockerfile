FROM python:3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app

COPY pressure_pb2.py .
COPY utils.py .
COPY services.py .
COPY resources resources

ENV PROTO="true"

CMD ["uvicorn", "services:app", "--host", "0.0.0.0", "--workers", "3", "--port", "8000"]