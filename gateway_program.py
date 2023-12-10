import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import serial
import time
import json

array = []
bluetooth = serial.Serial("/dev/rfcomm6", 9600)

def sendMsg(a):
    bluetooth.write(a.encode("utf-8"))

def receiveSwitchMessage():
    data = bluetooth.readline()
    data2 = data.decode("utf-8").rstrip()
    print(data2)
    # return numbers

def receiveDhtMessage():
    data = bluetooth.readline()
    data2 = data.decode("utf-8").rstrip()
    received_data = data2.split(" ")
    print(received_data)
    return received_data[0], received_data[1], received_data[2], received_data[3], received_data[4], received_data[5], received_data[6]

LED_PIN = 2
DHT_PIN = 5

# MQTT setup for Pi4
pi4_mqtt_server = "192.168.122.50"
pi4_mqtt_port = 1883
pi4_mqtt_username = "username"
pi4_mqtt_password = "password"

# MQTT setup for ThingsBoard
tb_mqtt_server = 'thingsboard.cloud'
tb_access_token = 'Raspberry_Pi_token'

def on_pi4_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Pi4 MQTT broker")
        client.subscribe("switch1")
        client.subscribe("switch2")
       
    else:
        print("Pi4 Connection failed with error code " + str(rc))

def on_pi4_message(client, userdata, msg):
    print("Pi4 Message arrived in topic: " + msg.topic)
    print("Pi4 Message: " + msg.payload.decode())

    if msg.topic == "switch1":
        if msg.payload.decode() == "ON":
            print("LED IS ON")
            sendMsg('a')
        elif msg.payload.decode() == "OFF":
            print("LED IS OFF")
            sendMsg('a')
    elif msg.topic == "switch2":
        if msg.payload.decode() == "ON2":
            print("LED2 IS ON")
            sendMsg('b')
        elif msg.payload.decode() == "OFF2":
            print("LED2 IS OFF")
            sendMsg('b')
   

def on_tb_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to ThingsBoard MQTT broker")
    else:
        print("ThingsBoard Connection failed with error code " + str(rc))

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# MQTT setup for Pi4
pi4_client = mqtt.Client()
pi4_client.username_pw_set(username=pi4_mqtt_username, password=pi4_mqtt_password)
pi4_client.on_connect = on_pi4_connect
pi4_client.on_message = on_pi4_message
pi4_client.connect(pi4_mqtt_server, pi4_mqtt_port, 60)

# MQTT setup for ThingsBoard
tb_client = mqtt.Client()
tb_client.username_pw_set(tb_access_token)
tb_client.on_connect = on_tb_connect
tb_client.connect(tb_mqtt_server, 1883, 60)

# MQTT loop for both clients
pi4_client.loop_start()
tb_client.loop_start()


try:
    while True:
       
        retries = 3
        while retries > 0:
            time.sleep(5)
            sendMsg('c')
            temperature, humidity, alarm, relay1, relay2, air, co = receiveDhtMessage()
           
            if humidity !='1' and temperature !='1':
                print("Temperature:", temperature)
                print("Humidity:", humidity)
                to_send = str(temperature) + ";" + str(humidity) + ";" + str(alarm) + ";" + str(relay1) + ";" + str(relay2) + ";" + str(air) + ";" + str(co)
                # Publish data to Pi4 MQTT
                pi4_client.publish("tempData", to_send)
                # Publish data to ThingsBoard MQTT
                sendingData = {'temperature': temperature, 'humidity': humidity, 'air quality': air, 'carbon monoxide': co}
                tb_client.publish('v1/devices/me/telemetry', json.dumps(sendingData), 1)
                break  # Exit the retry loop if successful
            else:
                print("Failed to retrieve DHT data")
                retries -= 1
                #time.sleep(2)  # Wait for 2 seconds before retrying

except KeyboardInterrupt:
    pass

# Cleanup GPIO and disconnect MQTT
GPIO.cleanup()
pi4_client.loop_stop()
pi4_client.disconnect()
tb_client.loop_stop()
tb_client.disconnect()
