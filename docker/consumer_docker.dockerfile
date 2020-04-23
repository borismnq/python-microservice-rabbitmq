FROM python:3.7
WORKDIR /usr/src/app
COPY src/modules/ ./modules/
COPY src/consumer.py ./worker.py
COPY bin/start.sh .
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip3 install -r requirements.txt
CMD ["sh", "start.sh"]