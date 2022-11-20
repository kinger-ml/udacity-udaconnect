import grpc
import location_pb2
import location_pb2_grpc
import random

def send_random_location_packets():
    random_person_id = random.randint(10, 100)
    random_latitude = random.randint(-90, 90)
    random_longitude = random.randint(-180, 180)

    payload = location_pb2.LocationsMessage(
        person_id=random_person_id,
        latitude=str(random_latitude),
        longitude=str(random_longitude)
    )
    return payload

if __name__ == "__main__":
    print("Sending sample payload...")
    channel = grpc.insecure_channel("127.0.0.1:5004")
    stub = location_pb2_grpc.LocationServiceStub(channel)
    # send 10 sample location data
    for i in range(10):
        res = stub.Create(send_random_location_packets())
        print(res)