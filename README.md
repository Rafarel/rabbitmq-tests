# Rabbitmq tests

This repo is for trying Rabbitmq features/behavior.
It uses rabbitmq 3.8 and python scripts to publish and consume messages with the `pika` lib.

## What's in here?

The docker folder contains a docker-compose file that will bring up a rabbitmq 3.8 with its management tools.
It also contains the `rabbitmq.conf` file where you can tweak values like the consumer_timeout value.
The configuration file is available here : `docker/rabbitmq/etc/rabbitmq.conf`

At the project root, you have scripts to test different feature/behavior :
- `send.py` creates the exchanges, queue and dead letter queue (dlq), then send a message.
- `receive.py` just consume the queue and auto acknowledge the message.
- `receive_dlq.py` will consume the queue but will send messages in dead letter queue.
- `receive_timeout.py` will consume the queue but will sleep more than the consumer_timeout setting before trying to acknowledge the message.

## How to use?

1.  With docker installed on your machine, you have to launch the rabbitmq container.

```
cd docker
docker-compose up -d
```
2. Install the python dependencies with `pip install`
3. Then you can first launch the `send.py` script that will take care of exchanges and queues creation then send a message.
4. You can now execute one of the `receive*.py` to consume the message.
5. you have to execute `send.py` again if you want to push another message in the queue.

## The consumer_timeout problem

I have hard times to demonstrate that the `consumer_timeout` setting is working as expected.
I may have done things wrong or misunderstood the consumer_timeout behavior.

Basically, I have a `consumer_timeout` set to 10000ms (10sec) and then I try to consume the message with a call back
that sleeps a bit longer than the timeout value (20sec) before trying to acknowledge the message.

I am supposed to have a PRECONDITION_FAILED exception due to the timeout, but it is not the case.
I have the exception if I set the `SLEEP_DURATION` in `receive_timeout.py` way more than the `consumer_timeout` value.

Quote from https://www.rabbitmq.com/consumers.html#acknowledgement-timeout
> If a consumer does not ack its delivery for more than the timeout value (30 minutes by default), its channel will be closed with a PRECONDITION_FAILED channel exception.
