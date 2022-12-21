import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random
import serial 

# define serial connection over bluetooth and its params
# s_posture = serial.Serial(
#         port='/dev/ttyS0', # using the defined rfcomm0 as the port
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

def parse_telemetry(binary_telemetry):
    # decode received bytes into string
    # print(type(binary_telemetry))
    str_message = binary_telemetry.decode('utf-8-sig')
    # remove newline symbols
    str_message = str_message.replace('\n', '')
    parse_telemetry = str_message.replace('\r', '')
    parse_telemetry = parse_telemetry.replace('(', '')
    parse_telemetry = parse_telemetry.replace(')', '')
    parse_telemetry = parse_telemetry.replace(',5,0,0,0,0', '')
    parse_telemetry = parse_telemetry.split(',')
    parse_telemetry_float = [float(x) for x in parse_telemetry]
    
    # TODO delete !
    rand_pitch = round(random.uniform(-85.0000, -20.0000), 4)
    parse_telemetry_float[7] = rand_pitch

    return parse_telemetry_float



def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    # commands
    print('Message received: ' , payload)
    if 'buzzer' in payload.keys():
        if payload['buzzer'] == 'short_buzz': 
            # s.write(b'lightOn\n')
            print('short BUZZ')
        if payload['buzzer'] == 'long_buzz': 
            # s.write(b'lightOn\n')
            print('long BUZZ')

mqtt_client.subscribe(client_command_topic, qos=1)
mqtt_client.on_message = handle_command

while True:
   
    # reset telemetry
    posture_arduino_telemetry = None
    sitting_arduino_telemetry = None

    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)

    try :
        # read telemetry coming from smartphone sensors
        # posture_arduino_telemetry = s_posture.readline()
        
        posture_arduino_telemetry = b'(0.08255,0.51266,9.83899,-0.07,-0.02625,0.14,54.32451,-75.9826,0.48072,5,0,0,0,0)\n'
        # if posture telemetry is received
        if posture_arduino_telemetry != None:
            if  (len(posture_arduino_telemetry) != 0):
                posture_telemetry_float = parse_telemetry(posture_arduino_telemetry)
                if len(posture_telemetry_float) == 9:
                    telemetry = json.dumps({
                        'timestamp' : ts,  
                        'pitch': posture_telemetry_float[7]})

                    print('Sending posture telemetry ', telemetry)
                    mqtt_client.publish(client_posturetelemetry_topic, telemetry, qos=1)

                    time.sleep(5)

            else: continue
        else: continue
    except :
        print('Serial Exception')


        
