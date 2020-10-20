import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(cls, bases, dict)
        cls._instanceDict = {}

    def __call__(cls, *args, **kwargs):
        argdict = {"args": args}
        argdict.update(kwargs)
        argset = frozenset(argdict)
        if argset not in cls._instanceDict:
            cls._instanceDict[argset] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instanceDict[argset]


class RabbitConnection(metaclass=Singleton):
    def __init__(self):
        pass

    def do_connection(self):
        # PIKA CONFIGURATION
        credentials = pika.PlainCredentials(
            os.environ["RABBIT_USER"], os.environ["RABBIT_PWD"]
        )
        parameters = pika.ConnectionParameters(
            os.environ["RABBIT_HOST"], os.environ["RABBIT_PORT"], "/", credentials
        )
        # PIKA CONNECTION
        self.connection = pika.BlockingConnection(parameters)
        # CONNECTION TO RABBITMQ CHANNEL
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        # RETURN CHANNEL
        return self.channel

    def close_connection(self):
        self.connection.close()
        return "Rabbit connection terminated"

    def send_message(self, params):
        try:
            self.channel.basic_publish(
                exchange=params["exchange"],
                routing_key=params["key"],
                body=json.dumps(params["message"]),
                properties=pika.BasicProperties(delivery_mode=1),
            )
            print("== MESSAGE SENT TO {} QUEUE==".format(params["key"]))
        except Exception as e:
            print("== EXCEPTION ==", e)
            print(
                "=== WARNING: PROBLEM SENDING MESSSAGE TO {} QUEUE===>".format(
                    params["key"]
                )
            )

        return
