#!/usr/bin/env python3
from json import JSONDecodeError
import json
import socket 
from modules.Database import *
from modules.Rabbit import *
from modules.Sources.ClassicClass import *
import os
import sys
# Import root file to sys.path
sys.path.append(os.getcwd())  
# Get config.json file data
working_directory = os.getcwd() 
with open(working_directory+'/config.json', 'r') as c:
    data = c.read()
config = json.loads(data)

def callback(ch, method, properties, body):

    try:
        # Receive RabbitMQ message in body variable
        body = json.loads(body)
        print('=== CONSUMER - MESSAGE RECEIVED ===>', body)
        # Create a ClassicClass object initializing it with message params (body)
        classic_class_obj = ClassicClass(body)
        # Get parsed data using 'do_something' function
        parsed_data = classic_class_obj.do_something()
        # Create a new JSON object (it will contain the message for the next consumer)
        message_to_next_consumer = {"data":[]}
        # Loop parsed data and use it in order to execute a SQL query
        for data in parsed_data:
            dbcxn = DatabaseConnection()
            dbcxn.do_connection()
            # Executing query using 'do_query' function from 'Database'
            db_response = dbcxn.do_query(parsed_data)
            message_to_next_consumer['data'].append(db_response)
        # Send message to the next RabbitMQ consumer using 'send_message' function from 'Rabbit'
        rcxn.send_message({
            "message":message_to_next_consumer,
            "exchange":config['python-microservice-rabbitmq']['NEXTCONSUMEREXCHANGE'],
            "key": config['python-microservice-rabbitmq']['NEXTCONSUMERKEY']
            })
    except Exception as e:
        print('=== EXCEPTION ===>', e)
        print('=== MESSAGE BODY ===>', body)
        return


if __name__ == "__main__":

    # RABBIT CONNECTION AND START CONSUMING
    rcxn = RabbitConnection()
    channel = rcxn.do_connection()
    channel.basic_consume(queue=config['python-microservice-rabbitmq']['MYCONSUMERQUEUE'],
                          auto_ack=True,
                          on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
