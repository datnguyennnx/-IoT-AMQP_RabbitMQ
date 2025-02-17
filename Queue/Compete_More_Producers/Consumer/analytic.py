import pika
import time
import random
from pika.exchange_type import ExchangeType

#Establish a connection with RabbitMQ server.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel() 

#Declare a queue
queue = channel.queue_declare(queue='analytical', exclusive= True)

#Create an explicit exchange
channel.exchange_declare(exchange='mytopicexchange', exchange_type=ExchangeType.topic)

#Create binding key
channel.queue_bind(exchange='mytopicexchange', queue=queue.method.queue, 
                   routing_key='*.europe.*')

#Don't dispatch a new message unless the previous message has not been ackknowledged
channel.basic_qos(prefetch_count=1)

#Receiving messages from the queue
def callback(ch, method, properties, body):
    processing_time = random.randint(4,6)
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f" [x] Analytic-service received {body}")   

# We need to tell RabbitMQ that this particular callback function should receive messages from our analytical queue
channel.basic_consume(queue=queue.method.queue,
                      on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
