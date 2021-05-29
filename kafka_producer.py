import json
from kafka import KafkaProducer


class KafkaProducer:
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    def send(self, record):
        self.producer.send('black_list', record)
    
    def flush(self):
        self.producer.flush()