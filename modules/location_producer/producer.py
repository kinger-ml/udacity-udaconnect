import grpc
import json
import location_pb2
import location_pb2_grpc
import logging
import os

from concurrent import futures
from kafka import KafkaProducer

#Kafka
TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Location Producer Service")

producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])

class LocationProducerServicer(location_pb2_grpc.LocationServiceServicer):
    def publish_location(self, location_data):
        print(f"Data to be sent to kafka: {location_data}")

        encoded_data = json.dumps(location_data).encode('utf-8')
        #print(f"Data to be sent to kafka: {encoded_data}")
        producer.send(TOPIC_NAME, encoded_data)
        producer.flush()

        logger.info(f"Published location data {location_data} to kafka successfully.")

    def Create(self, request, context):
        payload = {
            "person_id": int(request.person_id),
            "latitude": request.latitude,
            "longitude": request.longitude
        }

        logger.info((f"Payload:{payload}"))

        self.publish_location(payload)
        return location_pb2.LocationMessage(**payload)


# location gRPC server Initialization
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationProducerServicer(), server)
server.add_insecure_port("[::]:5005")
server.start()

# Do not kill the thread
server.wait_for_termination()