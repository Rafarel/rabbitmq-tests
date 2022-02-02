import os
import pika
import sys

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    params = pika.ConnectionParameters(host='localhost', credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
