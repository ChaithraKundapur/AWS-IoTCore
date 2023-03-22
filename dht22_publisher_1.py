import Adafruit_DHT
import boto3
import json
import ssl
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Set up the DHT22 sensor on GPIO pin 4
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Set up the AWS IoT Core client
client_id = 'my_raspberry_pi'
iot_endpoint = 'a38z5cckdkeofh-ats.iot.ap-south-1.amazonaws.com' 
ca_path = '/home/niveus/Desktop/IoT-Core/AmazonRootCA1.pem'
cert_path = '/home/niveus/Desktop/IoT-Core/06963ddd98a27ba5c3600c18097c5303c7846dbb785267ec5dfd5f5236cdad31-certificate.pem.crt'
key_path = '/home/niveus/Desktop/IoT-Core/06963ddd98a27ba5c3600c18097c5303c7846dbb785267ec5dfd5f5236cdad31-private.pem.key'

mqtt_client = AWSIoTMQTTClient(client_id)
mqtt_client.configureEndpoint(iot_endpoint, 8883)
mqtt_client.configureCredentials(ca_path, key_path, cert_path)

# Set up the topic and message payload
topic = 'temperature/humidity'
message = {}

while True:
    # Read the temperature and humidity from the DHT22 sensor
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    # If the data is valid, add it to the message payload
    if humidity is not None and temperature is not None:
        message['temperature'] = '{:.1f}'.format(temperature)
        message['humidity'] = '{:.1f}'.format(humidity)

        # Convert the message to JSON format
        message_json = json.dumps(message)

        # Connect to AWS IoT Core and publish the message
        mqtt_client.connect()
        mqtt_client.publish(topic, message_json, 1)
        mqtt_client.disconnect()

        print('Published message: {}'.format(message_json))

    # Wait for 5 seconds before reading again
    time.sleep(5)

