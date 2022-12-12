import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random
import serial 

# define serial connection over bluetooth and its params
# s_posture = serial.Serial(
#         port='/dev/rfcomm0', # using the defined rfcomm0 as the port
#         baudrate = 9600,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=1
# )

# define serial connection over bluetooth and its params
# s_sitting = serial.Serial(
#         port='/dev/rfcomm0', # using the defined rfcomm0 as the port
#         baudrate = 9600,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=1
# )


# gotten from https://www.guidgen.com/
client_id = '278320da-7c3d-4236-905c-4518170a814f'

client_posturetelemetry_topic = client_id + '/postureTelemetry'
client_sittingtelemetry_topic = client_id + '/sittingTelemetry'
client_command_topic = client_id + '/command'

mqtt_client = mqtt.Client(client_id + 'gateway')
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    # commands
    print('Message received: ' , payload)
    if payload['buzzer'] == 'buzz': 
        # s.write(b'lightOn\n')
        print('BUZZ')

mqtt_client.subscribe(client_command_topic, qos=1)
mqtt_client.on_message = handle_command

while True:
    posture_arduino_telemetry = None
    sitting_arduino_telemetry = None

    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)
    posture_arduino_telemetry = b'(0.08255,0.51266,9.83899,-0.07,-0.02625,0.14,54.32451,-75.9826,0.48072,5,0,0,0,0)\n\r'
    sitting_arduino_telemetry = b'(0.08255,0.51266,9.83899,-0.07,-0.02625,0.14,54.32451,-75.9826,0.48072,5,0,0,0,0)\n\r'

    # read telemetry coming from arduino
    # posture_arduino_telemetry = s_posture.readline
    # sitting_arduino_telemetry = s_sitting.readline

    if posture_arduino_telemetry != None:
        # decode received bytes into string
        str_message = posture_arduino_telemetry.decode('utf-8-sig')
        # remove newline symbols
        str_message = str_message.replace('\n', '')
        posture_telemetry = str_message.replace('\r', '')
        posture_telemetry = posture_telemetry.replace('(', '')
        posture_telemetry = posture_telemetry.replace(')', '')
        posture_telemetry = posture_telemetry.replace(',5,0,0,0,0', '')
        posture_telemetry = posture_telemetry.split(',')
        posture_telemetry_float = [float(x) for x in posture_telemetry]

        telemetry = json.dumps({
            'timestamp' : ts,  
            'Orientation': posture_telemetry_float[6:]})

        print('Sending posture telemetry ', telemetry)
        mqtt_client.publish(client_posturetelemetry_topic, telemetry, qos=1)

    if sitting_arduino_telemetry != None:
        # decode received bytes into string
        str_message = sitting_arduino_telemetry.decode('utf-8-sig')
        # remove newline symbols
        str_message = str_message.replace('\n', '')
        sitting_telemetry = str_message.replace('\r', '')
        sitting_telemetry = sitting_telemetry.replace('(', '')
        sitting_telemetry = sitting_telemetry.replace(')', '')
        sitting_telemetry = sitting_telemetry.replace(',5,0,0,0,0', '')
        sitting_telemetry = sitting_telemetry.split(',')
        sitting_telemetry_float = [float(x) for x in sitting_telemetry]

        telemetry = json.dumps({
            'timestamp' : ts,  
            'Orientation': posture_telemetry_float[1:]})

        print('Sending sitting/standing telemetry ', telemetry)
        mqtt_client.publish(client_sittingtelemetry_topic, telemetry, qos=1)

    time.sleep(5)

