FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5003

COPY . .

CMD ["python", "producer.py"]