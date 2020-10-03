#!/bin/zsh

../../pyboard.py --device /dev/tty.usbserial-D3070UPO -f cp button.py :
../../pyboard.py --device /dev/tty.usbserial-D3070UPO -f cp colour.py :
../../pyboard.py --device /dev/tty.usbserial-D3070UPO -f cp ntp.py :
../../pyboard.py --device /dev/tty.usbserial-D3070UPO -f cp main.py :
../../pyboard.py --device /dev/tty.usbserial-D3070UPO -f cp config.json :
../../pyboard.py --device /dev/tty.usbserial-D3070UPO -f cp boot.py :