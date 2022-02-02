import pika


credentials = pika.PlainCredentials("guest", "guest")
params = pika.ConnectionParameters(host="localhost", credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange="my_dlx", exchange_type="topic", durable=True)
channel.queue_declare("my_dlq", durable=True)
channel.queue_bind("my_dlq", "my_dlx", "my_key")

channel.exchange_declare(exchange="my_x", exchange_type="topic", durable=True)
channel.queue_declare("my_queue", durable=True, arguments={"x-dead-letter-exchange": "my_dlx"})
channel.queue_bind("my_queue", "my_x", "my_key")

body = "Hello World"
channel.basic_publish(exchange="my_x", routing_key="my_key", body=body)
print(" [x] Message sent!'")
connection.close()


