import network
import machine
import ujson as json

import ntp

# Disable this module being an Access Point
access_point = network.WLAN(network.AP_IF)
access_point.active(False)

# Configure the WiFi station interface
station = network.WLAN(network.STA_IF)

f = open('config.json', 'r')
cfg = None
wifi_cfg = None

try:
	cfg = json.load(f)
	wifi_cfg = cfg["wifi"]
except:
	print("[boot] config not readable")

# wifi_cfg = None
# machine.freq(240000000)

if wifi_cfg:
	station.active(True)
	if not station.isconnected():
		station.connect(wifi_cfg["ssid"], wifi_cfg["psk"])
		while not station.isconnected():
			pass
		try:
			ntp.set_time_from_ntp()
			print("[boot] ntp sync ok")
		except:
			print("[boot] ntp failed to sync")
else:
	station.active(False)