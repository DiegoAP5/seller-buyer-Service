import pika
import uuid
import json

class RabbitClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='35.168.45.250', port=5672, virtual_host='/', credentials=pika.PlainCredentials('diego', 'Diegoespro01'))
        )
        self.channel = self.connection.channel()
        # Declare a temporary response queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.response_queue = result.method.queue
        self.channel.basic_consume(queue=self.response_queue, on_message_callback=self.on_response, auto_ack=True)
    
    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call(self, queue, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            properties=pika.BasicProperties(
                reply_to=self.response_queue,
                correlation_id=self.corr_id
            ),
            body=json.dumps(message)
        )
        
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)

    def close(self):
        self.connection.close()
