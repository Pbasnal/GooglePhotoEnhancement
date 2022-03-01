#!/usr/bin/env python
import pika

def publish(queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                        routing_key=queue,
                        body=message)
    print(f" [x] Sent message to {queue}")


    connection.close()