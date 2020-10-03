# Board

## Photos

![A photo of the prototype board](/other/board-v1.jpg)

![A photo of the bare prototype board](/other/board-bare-v1.jpg)

![A photo of the underside of the prototype board](/other/board-underside-v1.jpg)

_The temporary wire was used in testing if using a different GPIO pin would resolve the flickering issue._

## Notes

### Power:

- 12V 2A wall power supply
  - 12V supply to:
    - LED strip
    - L7805 5V linear power regulator

- L7805 5V linear power regulator
  - 5V supply to:
    - VUSB on ESP32
    - Logic level converter for LED strip logic

### Components:

- 1000uF/25V capacitor on 12V supply
- 10uF/50V capacitor on 5V supply
- BSS138LT N-Mosfet logic level converter
  - Handle ESP32 3.3V logic going to LED strip 5V logic
- 330ohm resistor on 5V LED strip logic
