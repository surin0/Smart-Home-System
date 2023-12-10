# Smart Home System with IoT functionality

The project is driven by a Pi Pico microcontroller, incorporates a relay module, ultrasonic sensor, buzzer, capacitive touch sensors, air quality sensors (MQ7, MQ135, DHT11), an infrared (IR) sensor, and a light-dependent resistor (LDR). The relay module allows remote control of two AC appliances. An ultrasonic sensor functions as security by detecting intruders, triggering a buzzer. A reset button disables the alarm. Capacitive touch sensors enable users to turn on/off the relay modules, while air quality sensors (MQ7, MQ135, DHT11) provide real-time data. An IR sensor acts as a motion detector for automatic lighting or ventilation control. An LDR offers ambient lighting control. An HC-05 Bluetooth module enables wireless communication with a Raspberry Pi 4 gateway for data exchange and remote control. The gateway receives MQTT messages from a smartphone app, facilitating two-way communication and comprehensive smart home system control. The app allows users to request sensor data, monitor alarm status, and remotely control appliances, including voice commands for added accessibility. The Raspberry Pi 4 gateway program uploads the sensor and appliance data to the ThingsBoard Cloud IoT platform.


Please note that the smartphone app, created using MIT App Inventor, cannot be uploaded as the code is not provided by MIT App Inventor for apps developed through their platform
## Installation

Install this in raspberry pi pico : Sensor_&_appliance_controller.py.

Install this in the Raspberry Pi 4:  gateway_program.py

