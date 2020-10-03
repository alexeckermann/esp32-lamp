from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(12, Pin.OUT)
np = NeoPixel(pin, 20)

led = Pin(5, Pin.OUT)
led.off()

NUM_PIXELS = 20

def draw():
	for pixel in range(0, NUM_PIXELS):
		np[pixel] = (255,0,0)

time.sleep(5)
draw()
np.write()
led.on()