import time
import paho.mqtt.client as mqtt
import json
import csv
import pandas as pd
import os

path_posture = 'posture_data.csv'
path_sitting = 'sitting_standing_data.csv'

# create csv file if not exist
if not (os.path.exists(path_posture)):
    with open('posture_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'pitch', 'posture', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# gotten from https://www.guidgen.com/
client_id = '278320da-7c3d-4236-905c-4518170a814f'

# mqtt topics
client_posturetelemetry_topic = client_id + '/postureTelemetry'
client_command_topic = client_id + '/command'


mqtt_client = mqtt.Client(client_id + 'cloudTelemetryProcessing')
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()



def handle_telemetry(client, userdata, telemetry):
    '''
    Gets posture telemetry and processes it:
    - classifies good and bad posture based on pitch thresholds
    - score the posture on a scale of 1-4
    '''
    payload = json.loads(telemetry.payload.decode())

    if 'pitch' in payload.keys():
        posture = 1 # takes 1 if good 0 if bad
        score = 4 # very good -80 -75

        OR = payload.get('pitch')
        print('Posture telemetry received: ' , OR)

        short_buzz_command = json.dumps({'buzzer' : 'short_buzz'})
        long_buzz_command = json.dumps({'buzzer' : 'long_buzz'})

        # pitch orientation thresholds
        pitch_th_small = -65.00
        pitch_th_big = -45.00
        if OR > pitch_th_small and OR < pitch_th_big:
            print('Sending short buzz command ', short_buzz_command)
            posture = 0
            score = 2 # okay
            mqtt_client.publish(client_command_topic, short_buzz_command, qos=1)
        elif OR > pitch_th_big:
            print('Sending long buzz command ', long_buzz_command)
            posture = 0
            score = 1 # bad
            mqtt_client.publish(client_command_topic, long_buzz_command, qos=1)
        elif OR < pitch_th_small and OR > -75:
            score = 3 # good

        payload_send1 = {'timestamp': payload['timestamp'],
                        'pitch':payload['pitch'], 
                        'posture':posture,
                        'score': score}

        with open('posture_data.csv', 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'pitch', 'posture', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # save to csv
            writer.writerow(payload_send1)

    elif 'Sitting' in payload.keys():
        state = None # takes 1 if standing and 0 if sitting

        ST = payload.get('Sitting')
        print('Sitting/standing telemetry received: ' , ST)

        if ST[0] > 7.9 and ST[1] < 9.0:
            state = 1 # standing
            print('Standing state !')
        elif ST[1] > 7.9 and ST[0] < 9.0:
            state = 0 # sitting
            print('Sitting state!')
        
        payload_send = {'timestamp': payload['timestamp'],
                        'Acc_y':payload['Sitting'][0], 
                        'Acc_z':payload['Sitting'][1], 
                        'state': state}
                        
        with open('sitting_standing_data.csv', 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'Acc_y', 'Acc_z', 'state']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # save to csv
            writer.writerow(payload_send)


mqtt_client.subscribe(client_posturetelemetry_topic, qos=1)
mqtt_client.on_message = handle_telemetry


while True:
    time.sleep(3)
    