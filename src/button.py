import time
from machine import Pin

class Button():
	def __init__(self, pin, callback, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, wait_ms=220):
		self.callback = callback
		self.wait_ms = wait_ms

		self._entry_value = None

		pin.irq(trigger=trigger, handler=self._handler)
	
	def _invoke_callback(self, pin):
		self.callback(pin)

	def _lower_semaphore(self):
		self._semaphore_raise_at = time.ticks_ms() + self.wait_ms
	
	def _semaphore_raised(self):
		return time.ticks_ms() > self._semaphore_raise_at

	def _handler(self, pin):
		if self._entry_value == None:
			if pin.value() == 0:
				self._entry_value = pin.value()
				self._lower_semaphore()
			return

		if self._entry_value != pin.value():
			if self._semaphore_raised():
				self._invoke_callback(pin)
				self._entry_value = None