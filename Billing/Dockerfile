FROM python:3.7-alpine
RUN python -m pip install --upgrade pip

COPY ./src /app
WORKDIR /app
RUN pip install -r requirements.txt