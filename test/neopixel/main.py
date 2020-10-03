from machine import Pin
from neopixel import NeoPixel
import time

from colours import hsv_to_rgb

pin = Pin(12, Pin.OUT)
np = NeoPixel(pin, 20)

led = Pin(5, Pin.OUT)
led.off()

NUM_PIXELS = 20 - 1
# NUM_PIXELS = 1

def float_to_byte(value: float):
	return round( value * 255 )

def rainbow():
	for firstPixelHue in range(0, 255):
		for pixel in range(0, NUM_PIXELS):
			pixelHue = firstPixelHue + (pixel * 255 / NUM_PIXELS)
			color = hsv_to_rgb(pixelHue / 255, 1, 0.5)
			np[pixel] = ( float_to_byte(color[0]), float_to_byte(color[1]), float_to_byte(color[2]) )
		np.write()
		time.sleep_ms(10)
		print('pixels:', np)
	return

rainbow()
led.on()
