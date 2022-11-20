FROM python:3.7-alpine

WORKDIR .

EXPOSE 5002

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "consumer.py"]