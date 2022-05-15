from fastapi import FastAPI
import paho.mqtt.client as mqtt
import ast
from db_script import add_row_well_data_too

app = FastAPI()

status = {
    'last_payload': None,
    'mqqt': 'not connected',
}

@app.get("/mqqt-server-status")
async def server_status():
    return status


def on_connect(client, userdata, flags, rc):
    global status
    status['mqqt'] = 'connected'
    client.subscribe("M/Qoraqalpog'iston/+/+/data")
    #client.subscribe("M/xorazm/+/+/data")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    global last_payload
    try:
        last_payload = str(msg.payload)[2:-1]
        last_payload = ast.literal_eval(last_payload)
        status['last_payload'] = last_payload
        add_row_well_data_too(last_payload)
    except:
        pass
    print(msg.topic+" "+str(last_payload))


client = mqtt.Client()
client.username_pw_set('emqx', '12345')
client.on_connect = on_connect
client.on_message = on_message

ip = '185.196.214.190'
port = 1883

client.connect(ip, port, 10)
client.loop_start()
