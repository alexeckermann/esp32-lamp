from micropython import const

class NeuePixelTiming:
	ZeroHigh = ZeroLow = 0
	OneHigh = OneLow = 0
	Reset = 0

	PulseLength = const(2)

	def value(cls, value: int):
		return None

	def pulse(cls, bit: int):
		if bit == 0:
			return (cls.ZeroHigh, cls.ZeroLow)
		elif bit == 1:
			return (cls.OneHigh, cls.OneLow)
		elif bit == -1:
			return (0,cls.Reset)
		else:
			raise NotImplemented

class NeuePixelTiming_400Hz(NeuePixelTiming):
	ZeroHigh = const(50 // 5)
	ZeroLow = const(200 // 5)
	OneHigh = const(120 // 5)
	OneLow = const(130 // 5)
	Reset = const(520 // 5)

def pulse_value(value, timing=NeuePixelTiming(), bit_count=8):
	pulse_length = timing.PulseLength
	pulses = bytearray(pulse_length * bit_count)
	bit_arrangement = list(range(bit_count - 1, -1, -1))
	for bit_index in range(bit_count):
		bit = bit_arrangement[bit_index]
		bit_offset = bit_index * pulse_length
		if ((value >> bit) & 1):
			pulses[bit_offset:(bit_offset + pulse_length)] = bytes(timing.pulse(1))
		else:
			pulses[bit_offset:(bit_offset + pulse_length)] = bytes(timing.pulse(0))
	return pulses

def generate_pulse_value_dictionary(timing=NeuePixelTiming(), bit_count=8, value_range=range(256)):
	values = [None] * len(value_range)
	for value in value_range:
		values[value] = pulse_value(value, timing=timing, bit_count=bit_count)
	return values

class NeuePixelTimingPulseCache:
	def __init__(self, timing=NeuePixelTiming(), max_value=255, bit_count=8):
		self.timing = timing
		self.bit_count = bit_count
		self.value_range = range(max_value + 1)

		self.pulse_width = len(bytes(timing.pulse(0)))
		self.value_width = self.pulse_width * self.bit_count
		
		cache_length = self.value_width * len(self.value_range)

		self.cache = bytearray(cache_length)
		self.cache_view = memoryview(self.cache)
	
	def build(self):
		for value in self.value_range:
			value_offset = self.value_width * value
			end = value_offset + self.value_width
			self.cache_view[value_offset:end] = pulse_value(value, timing=self.timing, bit_count=self.bit_count)

	def __getitem__(self, value):
		value_offset = self.value_width * value
		end = value_offset + self.value_width
		return self.cache_view[value_offset:end]