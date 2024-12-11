# producer.py
import json
from confluent_kafka import Producer

KAFKA_BROKER = 'localhost:9092'  # או כתובת ה-Broker שלך
KAFKA_TOPIC = 'telegram-messages'  # שם הנושא

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def send_to_kafka(topic, data):
    producer.produce(topic, value=json.dumps(data).encode('utf-8'))
    producer.flush()
    print(f"Sent message to Kafka: {data}")
