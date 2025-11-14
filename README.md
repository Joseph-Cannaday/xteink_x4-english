# xteink_x4-english

## Erase Old Firmware

`sudo esptool.py --chip esp32-c3 erase_flash`

## Write New Firmware to Flash Memory

`sudo esptool.py --chip esp32-c3 --port [usbport] write_flash 0x00000 firmware_3.0.2_en.bin`
