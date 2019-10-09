from kafka import KafkaConsumer
from kafka import KafkaProducer
import json

def pop_task():
    consumer = KafkaConsumer('test_rhj')
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        print(recv)


def push_task():
    anchorId = 5555555
    Producer = KafkaProducer(bootstrap_servers='localhost:1234')
    msg_dict = {
        "anchorId": anchorId,
        'status': 1
    }
    msg = json.dumps(msg_dict)
    Producer.send('test_rhj', msg, partition=0)
    Producer.close()