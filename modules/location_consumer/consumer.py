import json
import logging
import os
import psycopg2

from modules.location_consumer.schemas import LocationSchema
from typing import Dict

from kafka import KafkaConsumer

#Kafka
TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

#DB
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-service")

def add_location_to_DB(location):
    '''consume location data and save it to the DataBase'''
    location_dict = json.loads(location)
    validation_result: Dict = LocationSchema().validate(location_dict)
    if validation_result:
        logger.warning(f"Unexpected data format in payload: {location}, reason: {validation_result}")
        return

    with psycopg2.connect(
        database = DB_NAME,
        user = DB_USERNAME,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    ) as conn:
        person_id = int(location_dict.get("person_id"))

        with conn.cursor() as cursor:
            try:
                query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, location_dict["latitude"], location_dict["longitude"])
                cursor.execute(query)
            except Exception as e:
                logger.error(f"Error while saving location data to Database: {e}")

# Create the kafka consumer
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

while True:
    for message in consumer:
        location_data = message.value.decode('utf-8')
        add_location_to_DB(location_data)