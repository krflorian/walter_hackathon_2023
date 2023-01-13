FROM python:alpine

WORKDIR /app

COPY README.md setup.py requirements.txt .
COPY src /app/src

RUN pip install -r requirements.txt
RUN pip install .

EXPOSE 8080

CMD [ "run" ]

