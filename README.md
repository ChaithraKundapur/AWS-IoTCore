# AWS-IoTCore - Steps used for implementation

#1 Connect the DHT22 sensor to the Raspberry Pi using a breadboard or jumper wires. Make sure to connect the data pin of the sensor to a GPIO pin of the Raspberry Pi.

#2 Install the necessary software packages on the Raspberry Pi. You will need to install the Raspbian operating system, Python, and the Adafruit DHT library.
- sudo apt-get update
- sudo apt-get install python3
- sudo pip3 install Adafruit_DHT
- python3 -c "import Adafruit_DHT; print(Adafruit_DHT.DHT22)"

Note : If the library is installed correctly, the output should be 22.

#3 Write a Python script to read the temperature and humidity data from the DHT22 sensor and publish it to AWS IoT Core using the AWS SDK for Python (Boto3).
-

#4 Create an AWS IoT Core Thing for the Raspberry Pi and configure it to receive data from the Python script. You will need to create an AWS IoT Core Thing, attach a certificate, and configure the Raspberry Pi to use the certificate to communicate with AWS IoT Core.

#5 Create an AWS IoT Core Rule to process the data received from the Raspberry Pi. You can create a rule that sends an email or SMS alert when the temperature or humidity goes above or below a certain threshold.

#6 Visualize the data using AWS IoT Analytics or AWS QuickSight. You can create a dashboard to monitor the temperature and humidity of the conference room in real-time.
