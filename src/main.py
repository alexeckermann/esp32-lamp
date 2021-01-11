import gc
import micropython
import time

from micropython import const

from machine import Pin
from machine import Timer

from button import Button
from neuepixel.neuepixel import NeuePixel
from animation import RainbowAnimation #CrossFadeAnimation #RainbowFadeAnimation

ZERO_PIN = const(0)
zero = Pin(ZERO_PIN, mode=Pin.IN)

IND_PIN = const(5)
indicator = Pin(IND_PIN, mode=Pin.OUT)
indicator.off()

LIGHT_PIN = const(12)
N_PIXELS = const(20)
light_pin = Pin(LIGHT_PIN, mode=Pin.OUT)

gc.collect()
# Tablo Pink-red: 358deg, 98%

N_FRAMES = const(200)
animation = RainbowAnimation(pixels=N_PIXELS, frames=N_FRAMES)
# colour = (0,0,255)
# background = (255,0,0)
# animation = CrossFadeAnimation(colour, background, pixels=N_PIXELS, frames=N_FRAMES)
# animation = PulseAnimation(hue=(274 / 360), pixels=N_PIXELS, frames=N_FRAMES)
# animation = RainbowFadeAnimation(pixels=N_PIXELS, frames=N_FRAMES)
animation.build()
gc.collect()

neue = NeuePixel(N_PIXELS)
gc.collect()

timer = None
neue.setup(light_pin)
gc.collect()

animation_index = 0

T_PERIOD = const(28)

def tick(timer):
	global neue, animation, animation_index

	# t_start = time.ticks_us()
	frame = animation[animation_index]
	# t_frame = time.ticks_us()

	# if animation_index == 0:
	# 	print('frame[0]: {}'.format(t_frame - t_start)) 
	# print('[{}] {}'.format(animation_index, frame))

	t_start = time.ticks_us()
	for pixel in range(len(frame)):
		neue[pixel] = frame[pixel]
	t_d_set = time.ticks_us() - t_start

	neue.write()
	t_d_write = time.ticks_us() - t_start

	if animation_index == 0:
		print('neue[0]: set {} - write {}'.format(t_d_set, t_d_write)) 

	gc.collect()

	if animation_index < (animation.frame_count - 1):
		animation_index += 1
	else:
		animation_index = 0

def start():
	global timer
	timer = Timer(0)
	timer.init(period=T_PERIOD, mode=Timer.PERIODIC, callback=tick)

def reset():
	global timer
	timer.deinit()
	timer = None

def debug():
	micropython.mem_info()
	print('-----------------------------')
	print('Initial free: {} allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))

def button_changed(pin):
	global timer
	if timer != None:
		reset()
		indicator.on()
		return
	indicator.on()
	
	start()

	indicator.off()

# debug()

btn = Button(pin=zero, callback=button_changed)
