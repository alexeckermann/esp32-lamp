from machine import Pin
import time

pin = Pin(5, Pin.OUT)

pin.off()

def blink():
	pin.on()
	time.sleep_ms(100)
	pin.off()
	time.sleep_ms(100)

for _ in range(10):
	blink()