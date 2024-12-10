FROM python:3.12-slim

WORKDIR /code/
COPY . /code/
ENV PYTHONUNBUFFERED=1
RUN pip install -r requirements.txt
RUN mkdir /code/logs

CMD python3 -m src.main
