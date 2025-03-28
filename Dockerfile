FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
COPY .env /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src /app/src
COPY data /app/data

RUN chmod +x /app/src/usecases/zoom2text.py

CMD ["python", "src/usecases/zoom2text.py"]