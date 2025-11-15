# xteink_x4-english
You may need to run these commands as sudo/admin depending on user privelages.
## Erase Old Firmware

`esptool.py --chip esp32-c3 erase_flash`

## Write New Firmware to Flash Memory

`esptool.py --chip esp32-c3 --port [usbport] write_flash 0x00000 firmware_3.0.2_en.bin`
