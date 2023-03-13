import json

import pika
from faker import Faker

import mongo_connect
from models import Users

# connect to rabbit mq
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
)
channel = connection.channel()

# drclare new exchange with `mailing_mock` name 
channel.exchange_declare(exchange='mailing_mock', exchange_type='direct')

#bind queue
channel.queue_bind(exchange='mailing_mock', queue='mailing_queue')
USERS_NUM = 5



class FakeUsersMongo():
    def __init__(self):
        self.LAST_USERS = []
        self.fake = Faker()

    def create_fake_users(self, users_num):
        for _ in range(users_num):
            new_user = Users(name=self.fake.name(),
                            email=self.fake.email())
            
            new_user.save()
            self.LAST_USERS.append(str(new_user.id))
    
    def get_last_ids(self):
        return self.LAST_USERS       
    

def main():
    fake = FakeUsersMongo()
    fake.create_fake_users(USERS_NUM)
    message = {f'id{num}': _id for num, _id in enumerate(fake.get_last_ids()) }
    print(message)
    channel.basic_publish(exchange='mailing_mock',
                        routing_key='mailing_queue',
                        body=json.dumps(message).encode(),
                        properties=pika.BasicProperties(
                            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                        ))

if __name__ == '__main__':
    main()

