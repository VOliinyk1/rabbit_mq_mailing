import sys
import json

import pika

import mongo_connect
from models import Users


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(message)
        for _id in message.values():
            user = Users(id=_id)
            user.update(is_mailed=True)
            print(f'User, is mailed')
            
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue='mailing_queue', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
