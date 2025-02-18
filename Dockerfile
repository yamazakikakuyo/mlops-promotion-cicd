FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
