FROM python:3.6.9-alpine

WORKDIR /app

COPY requirements.txt /app/
COPY Weight/* /app/ 
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 7070
CMD ["python","app.py"]
