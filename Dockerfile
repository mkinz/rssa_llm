FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -e .

EXPOSE 5050

ENV NAME World


CMD ["python", "-u", "src/main.py"]

