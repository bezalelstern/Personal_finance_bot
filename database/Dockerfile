FROM python:3.12-slim

WORKDIR /app

COPY ../../../Downloads .

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["python", "data_fake.py"]
