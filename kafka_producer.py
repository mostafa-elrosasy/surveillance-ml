import json
from kafka import KafkaProducer


class KafkaProducer:
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    
    def send(self, record):
        self.producer.send('notification', record)
    
    def flush(self):
        self.producer.flush()