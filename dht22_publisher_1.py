import Adafruit_DHT
import boto3
import json
import ssl
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from properties import CA_PATH, CERT_PATH, KEY_PATH, IOT_ENDPOINT, CLIENT_ID

# Set up the DHT22 sensor on GPIO pin 4
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

print(F"[DEBUG] DHT set to Pin {DHT_PIN} on the Raspberry Pi")

# Set up the AWS IoT Core client
# client_id = 'my_raspberry_pi'
# iot_endpoint = 'a38z5cckdkeofh-ats.iot.ap-south-1.amazonaws.com'
# ca_path = '/home/niveus/Desktop/IoT-Core/AmazonRootCA1.pem'
# cert_path = '/home/niveus/Desktop/IoT-Core/06963ddd98a27ba5c3600c18097c5303c7846dbb785267ec5dfd5f5236cdad31-certificate.pem.crt'
# key_path = '/home/niveus/Desktop/IoT-Core/06963ddd98a27ba5c3600c18097c5303c7846dbb785267ec5dfd5f5236cdad31-private.pem.key'

mqtt_client = AWSIoTMQTTClient(CLIENT_ID)
print(F"[DEBUG] MQTT Client ID: {CLIENT_ID}")
mqtt_client.configureEndpoint(IOT_ENDPOINT, 8883)
mqtt_client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

# Set up the topic and message payload
topic = 'temperature/humidity'
message = {}
print('[INFO] Connecting to AWS IoT Core')
mqtt_client.connect(
    keepAliveIntervalSecond=60,
)
print('[INFO] Connected to AWS IoT Core')

while True:
    print('Reading the temperature and humidity from the DHT22 sensor')
    # Read the temperature and humidity from the DHT22 sensor
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    print('[INFO] Temperature: {:.1f} C'.format(temperature))
    print('[INFO] Humidity: {:.1f} %'.format(humidity))
    # If the data is valid, add it to the message payload
    if humidity is not None and temperature is not None:
        print(
            '[INFO] Successfully read the temperature and humidity from the DHT22 sensor')
        message['temperature'] = '{:.1f}'.format(temperature)
        message['humidity'] = '{:.1f}'.format(humidity)

        # Convert the message to JSON format
        message_json = json.dumps(message)
        print("Converted message to JSON format: {}".format(message_json))

        # Connect to AWS IoT Core and publish the message
        mqtt_client.publish(topic, message_json, 1)
        print('[INFO] Published message to AWS IoT Core')
        print('[INFO] Disconnected from AWS IoT Core')

        print('[INFO] Published message: {}'.format(message_json))
    else:
        print('[ERROR] Failed to get reading')

    print('[INFO] Waiting 5 seconds before reading again')

    # Wait for 5 seconds before reading again
    time.sleep(5)
    mqtt_client.disconnect()
