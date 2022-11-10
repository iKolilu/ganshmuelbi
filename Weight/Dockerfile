FROM python:3.11.0-slim 

RUN mkdir /app
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ /app

ENTRYPOINT [ "python", "/app/app.py" ]