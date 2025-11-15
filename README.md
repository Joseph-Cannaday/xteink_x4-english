# xteink_x4-english

You may need to run these commands as sudo/admin depending on user privileges.

## Erase Old Firmware

`esptool --chip esp32-c3 erase_flash`

## Write New Firmware to Flash Memory

`esptool --chip esp32-c3 --port [usbport] write_flash 0x00000 firmware_3.0.2_en.bin`

## Create Backup of Firmware Currently On Device

To create a backup of currently running firmware to restore in the future, do the following:

Dump the partition table using:
`esptool --port [usbport] read-flash 0x8000 0x1000 partition_table.bin`

This will give you the mapping of where all the partitions are in memory and can therefore be used to find out how big the firmware pull will be.

Run `python3 parse_partition_table.py partition_table.bin`

This will output the parsed partition table, as well as the command need to extract the entire firmware i.e.

`esptool --port [usbport] read-flash 0x00000 16777216 firmware_pull.bin`
