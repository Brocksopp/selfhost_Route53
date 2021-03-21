FROM python:3.9.2-slim

WORKDIR /app


COPY requirements2.txt requirements2.txt
RUN pip install -r requirements2.txt

COPY . .

VOLUME ["/data"]
#COPY requirements2.txt requirements2.txt

CMD [ "python", "./selfhost_Route53.py"]
