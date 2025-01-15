FROM python:3.10-slim-bookworm
WORKDIR /app
RUN apt update && apt install -y gcc
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
CMD ["uvicorn", "invoice_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
