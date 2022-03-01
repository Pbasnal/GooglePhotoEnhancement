#!/usr/bin/env python
import pika

USER_QUEUE = "user"
PHOTO_QUEUE = "photo"

class MessageBus:
    def __init__(self):
        self.MESSAGE_CHANNEL = None 

    def registerQueues(self, channel):
        self.MESSAGE_CHANNEL = channel
        channel.queue_declare(queue=USER_QUEUE)
        channel.queue_declare(queue=PHOTO_QUEUE)
        

    def publish(self, queue, message):
        if self.MESSAGE_CHANNEL == None:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.MESSAGE_CHANNEL = connection.channel()

        self.MESSAGE_CHANNEL.basic_publish(exchange='',
                            routing_key=queue,
                            body=message)
        print(f" [*] Message sent on {queue}")

Bus = MessageBus()