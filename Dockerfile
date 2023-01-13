FROM python:alpine

WORKDIR /app

COPY README.md setup.py .
COPY src /app/src

RUN pip install .

EXPOSE 8080

CMD [ "run" ]

