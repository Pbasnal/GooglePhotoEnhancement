#!/usr/bin/env python
import pika

USER_QUEUE = "user"
PHOTO_QUEUE = "photo"

class MessageBus:
    def __init__(self):
        self.MESSAGE_CHANNEL = None 
        self.listeners = []
        self.consumerThread = None

    def addListener(self, listener):
        if listener == None:
            return
        self.listeners.append(listener)

    def registerQueues(self, channel):
        self.MESSAGE_CHANNEL = channel
        channel.queue_declare(queue=USER_QUEUE)
        channel.queue_declare(queue=PHOTO_QUEUE)

    def connectToRabbitMq(self, host):
        if self.MESSAGE_CHANNEL != None and self.MESSAGE_CHANNEL.is_open:
            return

        print(f"Channel not initialized or is closed, creating new channel")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.MESSAGE_CHANNEL = connection.channel()
        self.registerQueues(self.MESSAGE_CHANNEL)

    def startListeners(self, host):
        self.connectToRabbitMq(host)

        for listener in self.listeners:
            listener.registerMessageListener(self.MESSAGE_CHANNEL)

        try:
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.MESSAGE_CHANNEL.start_consuming()

        except KeyboardInterrupt:
            print('Closing via keyboard interrupt')
    
    def publish(self, queue, message):
        print(f" [*] Sending message on {queue}")

        self.connectToRabbitMq("localhost")

        self.MESSAGE_CHANNEL.basic_publish(exchange='',
                            routing_key=queue,
                            body=message)
        print(f" [*] Message sent on {queue}")