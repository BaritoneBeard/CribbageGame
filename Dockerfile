FROM python:3.9

WORKDIR .

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY server.py .

CMD [ "python", "./server.py" ]
