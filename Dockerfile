FROM python:alpine

WORKDIR /app

COPY README.md setup.py map.json .
COPY src /app/src

RUN pip install .
RUN pip install networkx 

EXPOSE 8080

CMD [ "run" ]

