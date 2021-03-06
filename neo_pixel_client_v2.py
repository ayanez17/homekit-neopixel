from neopixel import *
import board
import paho.mqtt.client as mqtt
import threading
import colorsys

global rgbs
global pixels_1
global pixels_2

pixel_pin_1 = board.D18
ORDER = GRB
# The number of NeoPixels
num_pixels = 16

pixels_1 = NeoPixel(
    pixel_pin_1, num_pixels, brightness=.5, auto_write=False,
    pixel_order=ORDER
)


# [Saturation, Hue, Brightness (0,1), R, G, B]
light_status = [0, 0, .5, 255, 255, 255]


def status(msg):
    import pdb;
    pdb.set_trace()
    payload = msg.payload.decode("utf-8")
    if payload == 'false':
        light_status[2] = 1 if light_status[2] == 0 else light_status[2]
    else:
        light_status[2] = 0

    pixels_1.brightness = light_status[2]
    pixels_1.show()

def brightness(msg):
    import pdb;
    pdb.set_trace()
    bn = int(msg.payload)
    bn = int(255 * bn * .01)
    light_status[2] = bn
    pixels_1.brightness = light_status[2]
    pixels_1.show()



def hue(msg):
    import pdb;
    pdb.set_trace()
    light_status[1] = int(msg.payload) / 360.0
    c = colorsys.hls_to_rgb(light_status[1], .5, light_status[0])
    light_status[3] = int(c[0] * 255)  # R
    light_status[4] = int(c[1] * 255)  # G
    light_status[5] = int(c[2] * 255)  # B
    color = (light_status[3],
             light_status[4],
             light_status[5])
    pixels_1.fill(color)
    pixels_1.show()


def saturation(msg):
    import pdb;
    pdb.set_trace()
    light_status[0] = int(msg.payload) * .01
    c = colorsys.hls_to_rgb(light_status[1], .5, light_status[0])
    light_status[3] = int(c[0] * 255)
    light_status[4] = int(c[1] * 255)
    light_status[5] = int(c[2] * 255)
    color = (light_status[3],
             light_status[4],
             light_status[5])
    pixels_1.fill(color)
    pixels_1.show()


def on_connect(client, userdata, flags, rc):
    # Light1
    client.subscribe("shelf/#")

def on_message(client, userdata, msg):
    import pdb; pdb.set_trace()
    if msg.topic == "shelf/status":
        status(msg)
    if msg.topic == "shelf/brightness":
        brightness(msg)
    if msg.topic == "shelf/saturation":
        saturation(msg)
    if msg.topic == "shelf/hue":
        hue(msg)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
