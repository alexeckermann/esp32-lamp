# esp32-lamp

A hobby project for an ESP32 powered LED (NeoPixel/WS2811) lamp.

Please be aware that this project is currently a **work in progress**. So there shouldn't be much worth copying or reusing in other projects at this stage.

---

## Goals

- Typical lighting controls
- Animated lightning
- Control over Bluetooth via iOS app
- Control using HomeKit (WiFi) via third-party bridge

## Build

- [ESP32 Thing](https://www.sparkfun.com/products/13907)
- [NeoPixel (WS2811) strip](https://www.adafruit.com/product/3869)
- Custom prototype board for power and data
- [MicroPython](http://micropython.org) on the ESP32

![A photo of the prototype board](/other/board-v1.jpg)

---

## TODO

- [x] Build a prototype board with power supply
- [ ] Evaluating MicroPython for performance and capability
  - Animation speed, smoothness, complexity
  - Concurrent tasks (animation & control)
- [ ] Testing animations and driving LED strip

### Current Work In Progress

Current tests: `./test/neopixel-test`

- How fast can an animation tick?
- Are there any performance impacts?
- Stable animation?
- Best way to store animations?
  - Precompiling the data and storing in a list

---

Thanks to [@jim_mussared](https://twitter.com/jim_mussared) for helping with MicroPython setup.
