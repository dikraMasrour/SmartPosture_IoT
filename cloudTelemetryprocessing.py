import time
import paho.mqtt.client as mqtt
import json
import csv
import pandas as pd


# with open('light_data.csv', 'w', newline='') as csvfile:
#     fieldnames = ['timestamp', 'light']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

# gotten from https://www.guidgen.com/
client_id = '278320da-7c3d-4236-905c-4518170a814f'

client_posturetelemetry_topic = client_id + '/postureTelemetry'
client_sittingtelemetry_topic = client_id + '/sittingTelemetry'
client_command_topic = client_id + '/command'


mqtt_client = mqtt.Client(client_id + 'cloudTelemetryProcessing')
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

STATE = ''
def handle_telemetry(client, userdata, telemetry):
    global STATE

    new_state = ''
    
    payload = json.loads(telemetry.payload.decode())
    ACC = payload.get('Acc')
    VELO = payload.get('Velo')
    OR = payload.get('Orientation')

    print('Telemetry received: ' , ACC, VELO, OR)

    # with open('light_data.csv', 'a', newline='') as csvfile:
    #     fieldnames = ['timestamp', 'light']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     # save to csv
    #     writer.writerow(payload)

    short_buzz_command = json.dumps({'buzzer' : 'short_buzz'})
    long_buzz_command = json.dumps({'buzzer' : 'long_buzz'})

    # pitch thresholds
    pitch_th_small = -65.00
    pitch_th_big = -45.00
    if OR[1] > pitch_th_small and OR[1] < pitch_th_big:
        print('Sending short buzz command ', short_buzz_command)
        mqtt_client.publish(client_command_topic, short_buzz_command, qos=1)
    elif OR[1] > pitch_th_big:
        print('Sending long buzz command ', long_buzz_command)
        mqtt_client.publish(client_command_topic, long_buzz_command, qos=1)

mqtt_client.subscribe(client_posturetelemetry_topic, qos=1)
mqtt_client.on_message = handle_telemetry


while True:
    time.sleep(5)     
    