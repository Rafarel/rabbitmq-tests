import os
import sys
import pika
from time import sleep
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosedByBroker
from pika.spec import Basic, BasicProperties

SLEEP_DURATION = 60


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    params = pika.ConnectionParameters(host='localhost', credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        print("Message received, going to sleep for {} seconds".format(SLEEP_DURATION))
        sleep(SLEEP_DURATION)
        print("Sleep ended, trying to acknowledge")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except ChannelClosedByBroker as err:
        print("Rabbitmq timeout reached")
        print(err)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
