import json

from celery import Celery
from kombu import Queue
from core.config import config


app = Celery(
    'tasks',
    broker=f'amqp://{config.RABBITMQ_USER}:{config.RABBITMQ_PASSWORD}@{config.RABBITMQ_HOST}:{config.RABBITMQ_PORT}/{config.RABBITMQ_VHOST}',
    backend='rpc://',
    include=['util.rabbit.pusher'],
)


app.conf.task_queues = (
    Queue(config.RABBITMQ_QUEUE, durable=True),
)


app.conf.task_routes = {
    'util.rabbit.pusher.push_to_rabbit': {'queue': config.RABBITMQ_QUEUE},
    'util.rabbit.pusher.get_from_rabbit': {'queue': config.RABBITMQ_QUEUE},
    'util.rabbit.pusher.get_all_from_rabbit': {'queue': config.RABBITMQ_QUEUE},
}


@app.task(bind=True, max_retries=0)
def push_to_rabbit(self, message: str):
    try:
        self.update_state(state='PROGRESS', meta={'message': 'Pushing message to RabbitMQ'})
        with app.connection() as connection:
            with connection.channel() as channel:
                channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)
                if not isinstance(message, str):
                    message = json.dumps(message)
                channel.basic_publish(exchange='', routing_key=config.RABBITMQ_QUEUE, body=message)
        self.update_state(state='SUCCESS', meta={'message': 'Message pushed to RabbitMQ'})
    except Exception as e:
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise e


def push_message_to_rabbit(message: str):
    push_to_rabbit.delay(message)


@app.task(bind=True, max_retries=0)
def get_from_rabbit(self):
    try:
        self.update_state(state='PROGRESS', meta={'message': 'Getting message from RabbitMQ'})
        with app.connection() as connection:
            with connection.channel() as channel:
                result = channel.basic_get(queue=config.RABBITMQ_QUEUE)
                if result is None:
                    self.update_state(state='SUCCESS', meta={'message': 'No message in queue'})
                else:
                    method_frame, header_frame, body = result
                    self.update_state(state='SUCCESS', meta={'message': body.decode()})
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception as e:
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise e


def get_message_from_rabbit():
    get_from_rabbit.delay()


@app.task(bind=True, max_retries=0)
def get_all_from_rabbit(self):
    try:
        self.update_state(state='PROGRESS', meta={'message': 'Getting all messages from RabbitMQ'})
        with app.connection() as connection:
            with connection.channel() as channel:
                messages = []
                while True:
                    method_frame, header_frame, body = channel.basic_get(queue=config.RABBITMQ_QUEUE)
                    if method_frame:
                        messages.append(body.decode())
                        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    else:
                        break
                self.update_state(state='SUCCESS', meta={'message': messages})
    except Exception as e:
        self.update_state(state='FAILURE', meta={'message': str(e)})
        raise e


def get_all_messages_from_rabbit():
    get_all_from_rabbit.delay()