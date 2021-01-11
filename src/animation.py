from colour import hsv_to_rgb, hls_to_rgb

class Animation:
	def __init__(self, name='animation', pixels=6, frames=60, channels=3):
		self.name = name
		self.pixel_count = pixels
		self.frame_count = frames
		self.channel_count = channels

		self.frame_size = self.pixel_count * self.channel_count

		self.frame_buffer = bytearray(self.frame_size)
		self.file = None
		# self.buffer = bytearray(self.frame_count * self.frame_size)
		# self.buffer_view = memoryview(self.buffer)
		# self.buffer = AnimationBuffer(pixels=self.pixel_count, frames=self.frame_count, channels=self.channel_count)

	def build(self):
		self.open('wb+')
	
	def open(self, mode = 'rb'):
		if self.file:
			self.file.close()
		filename = self.name + '.dat'
		self.file = open(filename, mode)

	# def frame(self, frame_index):
	# 	start = frame_index * self.frame_size
	# 	end = start + self.frame_size
	# 	return self.file_view[start:end]

	# def __setitem__(self, frame_index, frame):
	# 	start = frame_index * self.frame_size
	# 	end = start + len(frame)
	# 	self.buffer[start:end] = frame

	def push(self, frame_buffer):
		if len(frame_buffer) > self.frame_size:
			raise RuntimeError('animation frame buffer must match the expected frame size')
		self.file.write(frame_buffer)

	def __setitem__(self, frame_index, frame_buffer):
		if len(frame_buffer) > self.frame_size:
			raise RuntimeError('animation frame buffer must match the expected frame size')
		start = frame_index * self.frame_size
		self.file.seek(start)
		self.file.write(frame_buffer)
	
	def __getitem__(self, frame_index):
		start = frame_index * self.frame_size
		self.file.seek(start)
		self.frame_buffer[:] = self.file.read(self.frame_size)

		frame = self.frame_buffer
		return list(tuple(frame[pixel:(pixel + self.channel_count)]) for pixel in range(0, len(frame), self.channel_count))

class RainbowAnimation(Animation):
	def __init__(self, pixels=6, frames=60, channels=3):
		super().__init__(name='anim_rainbow', pixels=pixels, frames=frames, channels=channels)

	def build(self):
		super().build()
		velocity = 1 / self.frame_count
		spread = 1 / self.pixel_count
		for frame_number in range(self.frame_count):
			frame = self.frame_buffer
			for pixel_index in range(self.pixel_count):
				hue = ((pixel_index * spread) + (frame_number * velocity))
				rgb = hsv_to_rgb(hue, 1.0, 0.5)
				pixel_offset = pixel_index * self.channel_count
				pixel_bytes = bytes(map(lambda colour: round(colour * 255), rgb))
				frame[pixel_offset:(pixel_offset + len(pixel_bytes))] = pixel_bytes
			self.push(frame)
			# self[frame_number] = frame
		self.open()

class RainbowFadeAnimation(Animation):
	def __init__(self, pixels=6, frames=60, channels=3):
		super().__init__(name='anim_rainbowfade', pixels=pixels, frames=frames, channels=channels)
	
	def build(self):
		super().build()
		velocity = 360 // self.frame_count
		frame = self.frame_buffer
		for frame_number in range(self.frame_count):
			hue = (frame_number * velocity) / 360
			rgb = hsv_to_rgb(hue, 1.0, 0.3)
			value = bytes(map(lambda colour: round(colour * 255), rgb))
			frame[:] = value * self.pixel_count
			self.push(frame)

class CrossFadeAnimation(Animation):
	def __init__(self, a=(0,0,0), b=(0,0,0), pixels=6, frames=60, channels=3):
		super().__init__(name='anim_crossfade', pixels=pixels, frames=frames, channels=channels)
		self.a_colour = a
		self.b_colour = b
	
	def build(self):
		super().build()

		palette = self.palette(self.a_colour, self.b_colour, self.frame_count // 2)
		palette_frames = (palette + palette[::-1])
		for frame_number in range(self.frame_count):
			frame = bytes(palette_frames[frame_number]) * self.pixel_count
			self[frame_number] = frame

	def palette(self, start_colour, end_colour, step_count):
		step_count -= 1
		step = tuple((end_colour[i] - start_colour[i]) / step_count for i in range(len(start_colour)))

		add = lambda x, y: tuple(sum(z) for z in zip(x, y))
		mult = lambda x, y: tuple(int(y * z) for z in x)

		palette = bytearray(step_count * len(start_colour))

		run = [bytes(add(start_colour, mult(step, i))) for i in range(1, step_count)]
		run = [start_colour] + run + [end_colour]
		return run
	
from math import sin, pi

class PulseAnimation(Animation):
	def __init__(self, hue=0.0, saturation=1.0, min=0.1, max=1.0, pixels=6, frames=60, channels=3):
		super().__init__(name='anim_pulse', pixels=pixels, frames=frames, channels=channels)
		self.hue = hue
		self.saturation = saturation
		self.min_volume = min
		self.max_volume = max

	def build(self):
		super().build()
		velocity = pi / self.frame_count
		for frame_number in range(self.frame_count):
			volume = sin(frame_number * velocity) / 2.0
			rgb = hls_to_rgb(self.hue, max(min(volume, self.max_volume), self.min_volume), self.saturation)
			value = bytes(map(lambda colour: round(colour * 255), rgb))
			self[frame_number] = value * self.pixel_count