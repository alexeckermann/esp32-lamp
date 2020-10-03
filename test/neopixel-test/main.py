import time
import machine
import gc
from micropython import const

from machine import Pin
from machine import Timer

from button import Button
from colour import hsv_to_rgb

from neopixel import NeoPixel

import ntp

ZERO_PIN = const(0)
zero = Pin(ZERO_PIN, mode=Pin.IN)

LIGHT_PIN = const(12)
N_PIXELS = const(20)
N_COLOURS = const(3)
light = Pin(LIGHT_PIN, mode=Pin.OUT)
np = NeoPixel(light, n=N_PIXELS, timing=0)

IND_PIN = const(5)
indicator = Pin(IND_PIN, mode=Pin.OUT)
indicator.off()

timer = None
tick_lock = False
cycle = 0

# def tick(timer):
# 	global cycle
# 	for pixel in range(0, N_PIXELS):
# 		if pixel == cycle:
# 			np[pixel] = (0,0,255)
# 		else:
# 			np[pixel] = (255,0,0)
# 	np.write()
# 	if cycle < 20:
# 		cycle += 1
# 	else:
# 		cycle = 0

def float_to_byte(value: float):
	return round( value * 255 )

anim_buffer = list()
anim_buffer_len = 0

P_BUF_ORDER = (1, 0, 2)

def fill_buffer():
	global anim_buffer, anim_buffer_len
	for cycle in range(256):
		buf = bytearray(N_PIXELS * N_COLOURS)
		for pixel in range(0, N_PIXELS):
			hue = cycle + (pixel * 255 / N_PIXELS)
			rgb = list(map(lambda c: float_to_byte(c), hsv_to_rgb(hue / 255, 1.0, 0.3)))
			offset = pixel * N_COLOURS
			for i in range(N_COLOURS):
				buf[offset + P_BUF_ORDER[i]] = rgb[i]
		anim_buffer.append(buf)
	anim_buffer_len = len(anim_buffer)

anim_index = 0
last_tick = time.ticks_cpu()

def tick(timer):
	global np, anim_buffer, anim_index, anim_buffer_len, last_tick
	# if time.ticks_cpu() < last_tick:
	# 	print( "[tick] cpu tick < last" )
	# 	return

	np.buf = anim_buffer[anim_index]
	np.write()
	if anim_index < (anim_buffer_len - 1):
		anim_index += 1
	else:
		anim_index = 0

	print( "[t] %i" % time.ticks_diff(time.ticks_cpu(), last_tick) )
	last_tick = time.ticks_cpu()

# def tick(timer):
# 	global cycle, tick_lock
# 	if tick_lock:
# 		return
# 	tickLock = True
# 	for pixel in range(0, N_PIXELS):
# 		hue = cycle + (pixel * 255 / N_PIXELS)
# 		color = hsv_to_rgb(hue / 255, 1, 0.3)
# 		np[pixel] = ( float_to_byte(color[0]), float_to_byte(color[1]), float_to_byte(color[2]) )
# 	np.write()
# 	if cycle < 255:
# 		cycle += 1
# 	else:
# 		cycle = 0
# 	tickLock = False

def reset():
	global timer
	timer.deinit()
	timer = None

def button_changed(pin):
	global timer, anim_buffer
	if timer != None:
		reset()
		indicator.on()
		return
	indicator.on()
	timer = Timer(0)
	timer.init(period=32, mode=Timer.PERIODIC, callback=tick)
	# print( "Time: %i" % ntp.get_ntp_time("time.apple.com") )
	gc.collect()
	m0 = gc.mem_free()
	fill_buffer()
	gc.collect()
	md = m0 - gc.mem_free()
	print( "[buffer] length: %i" % len(anim_buffer) )
	print( "[buffer] size: %i" % md )
	print( "[gc] free: %i" % gc.mem_free() )
	indicator.off()

btn = Button(pin=zero, callback=button_changed)