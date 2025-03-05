FROM python:3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY ContextVariable_pb2.py .
COPY cloudservice.py .

ENV PROTO="true"

CMD ["uvicorn", "cloudservice:app", "--host", "0.0.0.0", "--workers", "3", "--port", "8000"]