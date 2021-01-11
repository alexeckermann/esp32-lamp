from micropython import const 
import gc
import time

import sys

if sys.platform != 'darwin':
	from machine import Pin
	from esp32 import RMT

from neuepixel.timing import *

__all__ = [ 'NeuePixel', 'NeuePixelTiming_400Hz', 'NeuePixelChannelOrder_GRB', 'NeuePixelChannelOrder_RGB' ]

NeuePixelChannelOrder_GRB = (1, 0, 2)
NeuePixelChannelOrder_RGB = (0, 1, 2)

class NeuePixel:
	def __init__(self, pixel_count, timing=NeuePixelTiming_400Hz(), channel_order=NeuePixelChannelOrder_GRB, pixel_channels=3, channel_bits=8):
		self.pixel_count = pixel_count
		self.timing = timing
		
		self.pixel_channel_count = pixel_channels
		self.pixel_channel_bits = channel_bits
		self.pixel_channel_order = channel_order

		self.pulse_channel_width = self.pixel_channel_bits * len(timing.pulse(0))
		self.pulse_pixel_width = self.pulse_channel_width * self.pixel_channel_count

		self.pulses = []
		self.pulses_view = None
		self.pulses_length = 0
		self.rmt = None

		self.pulse_cache = NeuePixelTimingPulseCache(timing=self.timing, bit_count=self.pixel_channel_bits)
	
	def setup(self, pin, rmt_channel=1):
		if pin != None:
			self.rmt = RMT(rmt_channel, pin=pin, clock_div=4)
		
		reset_length = len(self.timing.pulse(-1))
		self.pulses = bytearray((self.pixel_count * self.pulse_pixel_width) + reset_length)
		self.pulses_view = memoryview(self.pulses)
		self.pulses_view[len(self.pulses)-reset_length:len(self.pulses)] = bytes(self.timing.pulse(-1))
		self.pulses_length = len(self.pulses)
		self.pulses_tuple = tuple(self.pulses)

		self.pulse_cache.build()

	def __setitem__(self, pixel_index, colour):
		if isinstance(colour, tuple) == False:
			raise TypeError('Colour values must be a tuple, got {}'.format(type(colour)))

		if len(colour) != self.pixel_channel_count:
			raise ValueError('Colour values must have {} channels, got {}'.format(self.pixel_channel_count, len(colour)))

		pulse_pixel_offset = pixel_index * self.pulse_pixel_width
		pulses = []

		for channel_index in range(self.pixel_channel_count):
			value = int(colour[channel_index])
			pulses = self.pulse_cache[value]

			channel_pulse_index = self.pixel_channel_order[channel_index]
			start = pulse_pixel_offset + (channel_pulse_index * self.pulse_channel_width)
			end = start + len(pulses)
			self.pulses_view[start:end] = pulses
	
	def write(self):
		if self.rmt == None:
			raise RuntimeError('RMT has not been initialised for this instance of NeuePixel - likely no pin was given in setup()')

		self.pulses_tuple = tuple(self.pulses)

		self.rmt.write_pulses(self.pulses_tuple)
		self.rmt.wait_done()