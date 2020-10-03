# Notes

Just a collection of important notes and details found along the way.

---

## MicroPython Setup

- Firmware for the Thing is just Generic ESP32 Module
  - Currently using `esp32-idf3-20200805-unstable-v1.12-663-g9883d8e81.bin`
- Need to hold down the 0 button on boot to be able to modify firmware
- Download the MicroPython project source to use the `pyboard.py` file on local

**pyboard commands**
`pyboard.py --device <port> test/blink/main.py`

**Commands to flash firmware**
`esptool.py --port <port> --chip esp32 erase_flash`
`esptool.py --port <port> --chip esp32 write_flash -z 0x1000 <bin>`

**Useful links**
https://github.com/python/cpython/blob/3.8/Lib/colorsys.py

https://github.com/adafruit/Adafruit_NeoPixel/blob/master/Adafruit_NeoPixel.cpp