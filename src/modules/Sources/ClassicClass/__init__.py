import os
import datetime
import iso8601
import pytz
import time
import requests
import json


class ClassicClass(object):
    def __init__(self, body):

        self.params = body["params"]
        pass

    def do_something(self):
        response = []

        data = self.params["data"]
        for each in data:
            response.append(each)

        return response
