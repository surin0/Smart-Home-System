from machine import Pin,UART
uart = UART(1,9600)
import utime as time
from time import sleep
from machine import ADC
import utime
from dht import DHT11

relay1 = Pin(12, Pin.OUT)
relay2 = Pin(13, Pin.OUT)
relay1.on()
relay2.on()

irSensor = Pin(18, Pin.IN)
touchSnsr1 = Pin(17, Pin.IN)
touchSnsr2 = Pin(16, Pin.IN)
ldr = ADC(Pin(28))
smoke = ADC(Pin(26))
mq7 = ADC(Pin(27))
led = Pin(0, Pin.OUT)

trigger = Pin(11, Pin.OUT)
echo = Pin(10, Pin.IN)  # Configure echo pin as input
buzzer = Pin(14, Pin.OUT)
resetBtn = Pin(19, Pin.IN, Pin.PULL_DOWN)
def ultrasonicSnsr():
    timepassed = 0
    signaloff = 0  # Initialize signaloff variable
    signalon = 0  # Initialize signalon variable

    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()

    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()

    timepassed = signalon - signaloff
    distance_cm = (timepassed * 0.0343) / 2
    return distance_cm

def alarm():
    distance = ultrasonicSnsr()
   # print(distance)
    if distance<5.0:
        buzzer.on()
    if buzzer.value()==1 and resetBtn.value()==1:
       # print('on')
        buzzer.off()
    
        
    utime.sleep(0.1)

def read_dht11_sensor():
    # Wait 1 second to let the sensor power up
    #utime.sleep(1)

    pin = Pin(20, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)

    try:
        sensor.measure()
        
        temperature_value = sensor.temperature
        humidity_value = sensor.humidity
        #print("Temperature: {}".format(temperature_value))
        #print("Humidity: {}".format(humidity_value))
        return temperature_value, humidity_value
    except Exception as e:
        print("Error reading from DHT11 sensor:", e)
        return 1, 1



def sendMsg(a):
    
    sending  = str(a) +"\n"
    print(sending)
    uart.write(sending.encode("utf-8"))

def sendDht(a, b):
    if buzzer.value()==1:
        alarm='alarm'
    elif buzzer.value()==0:
        alarm = 'none'
    air, co = readAirQuality()
    sending = str(a) + " " + str (b) + " " + alarm  + " " + str(relay1.value()) + " " + str(relay2.value()) + " " + str(air) + " " + str(co) + "\n"
    print(sending)
    uart.write(sending.encode("utf-8"))
    
def receiveMsg():
    if uart.any():
        command = uart.readline()
        command= command.decode("utf-16")
        commands= str(command)
        print(commands)
        if commands == "a":
            relay1.toggle()
        if commands == "b":
            relay2.toggle()
        if commands == "c":
            c, d = read_dht11_sensor()
            if c is not None and c is not None:
                sendDht(c, d)
        if commands == "d":
            checkStatus()

def switchOnOff():
    if touchSnsr1.value():
        sleep(0.3)
        if touchSnsr1.value():
            relay1.toggle()
        sleep(0.1)
        
    if touchSnsr2.value():
        sleep(0.3)
        if touchSnsr2.value():
            relay2.toggle()
        sleep(0.1)

def infraredSensor():
    
    if irSensor.value()==0:
        relay2.toggle()
        sleep(0.1)
    
def autoBright():
    ldrVal = ldr.read_u16()
    
    light = round(ldrVal/65535*100,2)
   # print("light: " + str(light) +"%")
    
    if light<15.0:
        led.on()
    elif light>15.0:
        led.off()
        

def readAirQuality():
    airVal = smoke.read_u16()
    sleep(0.3)
    coVal = mq7.read_u16()
    sleep(0.3)
    voltage1 = (coVal / 65535) * 3.3  # Convert analog value to voltage
    co_ppm = (voltage1 - 0.4) / 0.02  # Convert voltage to CO concentration in ppm
    voltage2 = (airVal / 65535) * 3.3  # Convert analog value to voltage
    air_quality = (voltage2 / 3.3) * 100  # Convert voltage to air quality percentage
    if co_ppm<=0:
        co_ppm = 3
    return round(air_quality, 1), round(co_ppm, 1)
     


def checkStatus():
    string = str(relay1.value()) + str(relay2.value())
    sendMsg(string)
    #receiveMsg()
while True:
    alarm()
    switchOnOff()
    autoBright()
    #checkStatus()
    infraredSensor()
    receiveMsg()
    #sleep(1)

