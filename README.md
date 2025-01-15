# How to run:
```bash
docker-compose up --build
```
# Swagger docs:
http://127.0.0.1:8000/docs
# Kafka UI:
http://127.0.0.1:8080

# Running tests:
```bash
docker-compose up --build
```
```bash
python -m .venv
source .venv/bin/activate
pip install pytest requests
pytest tests.py
```
