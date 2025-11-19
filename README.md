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

## Updating the firmware using the official API (ADVANCED)

I have written a script to automate the api calls described below:

`usage: python3 update_checker.py [-h] [-i ID] [-t DEVICE_TYPE] [-v VERSION]`

The official XTEINK API pulls the firmware from:
<http://gotaserver.xteink.com/api/download/ESP32C3/V3.0.[version_number]/V3.0.[version_number]-EN.bin>

For example, V3.0.7 gets the firmware from:
<http://gotaserver.xteink.com/api/download/ESP32C3/V3.0.7/V3.0.7-EN.bin>

One can query the server to see if a firmware update is available via:
<http://gotaserver.xteink.com/api/check-update?current_version=V3.0.1&device_type=ESP32C3&device_id=1111> (either use curl/wget or navigate to this address in web browser)
This will tell the user what the latest version is under the `version:` field in the result, and will also provide the download url to get this version under the `download_url field`.

Technically the `device_id` field should be passing in your specific device's id (can be found by connecting to the devices hotspot: Sync -> More Transfer Options, then clicking "About" on the hotspot webpage).
Firmware updates and file management can also be done here.

\* Credit to u/daveallie on reddit for his post analyzing this behavior: <https://www.reddit.com/r/xteinkereader/comments/1oq2dg1/chinese_to_english_firmware_transition/>

Using the partition table offsets from earlier, if we do: 
`dd if=firmware_pull.bin of=app0.bin bs=1 skip=$((0x10000)) count=$((0x640000))`
(assuming the app0 offset is 0x10000), we can extract the current contents of app0 partition.

Noting that unused memory is filled with 0xFF bytes, we can do:

```
hexdump -C V3.0.7-EN.bin|tail -n 60                                                                                                                                                                                                         
0060d3f0  06 ce ef f0 1f ee 09 e5  b2 47 91 83 91 8b 1c c0  |.........G......|
0060d400  f2 40 62 44 05 61 82 80  c1 81 93 07 20 0c 63 9a  |.@bD.a...... .c.|
0060d410  f5 00 18 49 bd 47 13 05  50 10 63 e6 e7 00 01 45  |...I.G..P.c....E|
0060d420  82 80 13 05 50 10 82 80  01 45 82 80 13 d7 05 01  |....P....E......|
0060d430  93 07 d0 0c 13 05 50 10  63 1a f7 00 c1 67 93 87  |......P.c....g..|
0060d440  07 f0 fd 8d 99 67 63 93  f5 00 01 45 82 80 11 45  |.....gc....E...E|
0060d450  82 80 c1 81 93 07 f0 0e  01 45 63 84 f5 00 13 05  |.........Ec.....|
0060d460  50 10 82 80 03 45 85 01  e1 47 33 b5 a7 00 06 05  |P....E...G3.....|
0060d470  13 65 45 00 82 80 19 71  ce d6 b7 a9 ca 3f 83 a7  |.eE....q.....?..|
0060d480  c9 2d de ce da d0 be c6  5c 41 37 07 00 01 2e 8b  |.-......\A7.....|
0060d490  83 ab c7 04 bc 5f b3 05  d6 00 a2 dc a6 da d2 d4  |....._..........|
0060d4a0  d6 d2 86 de ca d8 e2 cc  e6 ca b3 35 b7 00 aa 8a  |...........5....|
0060d4b0  32 84 b6 84 82 97 93 07  60 10 2a 8a 63 10 f5 0a  |2.......`.*.c...|
0060d4c0  ef e0 3f be b7 65 c9 3f  37 66 c9 3f 13 87 c5 bd  |..?..e.?7f.?....|
0060d4d0  aa 86 13 06 c6 8f 93 85  c5 bd 05 45 97 a0 d2 01  |...........E....|
0060d4e0  e7 80 60 5a 36 47 83 a7  c9 2d 52 85 63 0c f7 06  |..`Z6G...-R.c...|
0060d4f0  ef 00 4f a7 13 06 00 04  93 05 f0 0f 68 00 97 f0  |..O.........h...|
0060d500  c6 ff e7 80 20 b9 03 a5  0a 00 34 00 26 86 1c 41  |.... .....4.&..A|
0060d510  5e 87 a2 85 dc 5b 33 09  94 00 82 97 22 46 aa 86  |^....[3....."F..|
0060d520  b3 07 a6 00 b3 0c c4 40  63 f3 27 01 3e 89 03 a5  |.......@c.'.>...|
0060d530  0a 00 6c 00 33 0c 89 40  18 41 33 04 24 41 a2 94  |..l.3..@.A3.$A..|
0060d540  58 57 4a 84 02 97 7c 00  2a 8a 62 86 5a 85 b3 85  |XWJ...|.*.b.Z...|
0060d550  97 01 97 f0 c6 ff e7 80  20 b4 62 9b e3 14 0a f8  |........ .b.....|
0060d560  d1 f8 49 b7 f6 50 66 54  d6 54 46 59 b6 59 26 5a  |..I..PfT.TFY.Y&Z|
0060d570  96 5a 06 5b f6 4b 66 4c  d6 4c 09 61 82 80 5c 41  |.Z.[.KfL.L.a..\A|
0060d580  39 71 4e d6 d8 43 ae 89  fc 4b 0c 43 22 dc 26 da  |9qN..C...K.C".&.|
0060d590  52 d4 06 de 4a d8 2a 84  b2 84 36 8a 82 97 21 ed  |R...J.*...6...!.|
0060d5a0  71 46 81 45 48 00 03 29  04 00 97 f0 c6 ff e7 80  |qF.EH..)........|
0060d5b0  60 ae 37 07 00 01 a3 02  41 01 93 07 00 02 63 f3  |`.7.....A.....c.|
0060d5c0  e4 00 e1 47 a3 03 f1 00  26 c4 4e c6 37 07 00 01  |...G....&.N.7...|
0060d5d0  c9 47 63 f3 e4 00 89 47  23 1c f1 00 83 27 09 00  |.Gc....G#....'..|
0060d5e0  4c 00 4a 85 dc 43 82 97  19 e5 5c 40 22 85 d8 43  |L.J..C....\@"..C|
0060d5f0  fc 4b 0c 4b 82 97 f2 50  62 54 d2 54 42 59 b2 59  |.K.K...PbT.TBY.Y|
0060d600  22 5a 21 61 82 80 5c 41  79 71 22 d4 dc 57 26 d2  |"Z!a..\Ayq"..W&.|
0060d610  06 d6 4a d0 ae 84 81 45  2a 84 82 97 35 e5 5c 40  |..J....E*...5.\@|
0060d620  22 85 d8 43 fc 4b 0c 43  82 97 39 ed 71 46 81 45  |"..C.K.C..9.qF.E|
0060d630  48 00 03 29 04 00 97 f0  c6 ff e7 80 a0 a5 37 07  |H..)..........7.|
0060d640  00 01 93 07 00 02 63 f3  e4 00 e1 47 a3 03 f1 00  |......c....G....|
0060d650  26 c4 37 07 00 01 93 07  10 02 63 f4 e4 00 93 07  |&.7.......c.....|
0060d660  00 02 23 1c f1 00 83 27  09 00 4c 00 4a 85 dc 43  |..#....'..L.J..C|
0060d670  82 97 19 e9 08 40 1c 41  fc 43 89 ef 5c 40 22 85  |.....@.A.C..\@".|
0060d680  d8 43 fc 4b 4c 47 82 97  b2 50 22 54 92 54 02 59  |.C.KLG...P"T.T.Y|
0060d690  45 61 82 80 58 40 a6 85  10 53 82 97 65 d1 ed b7  |Ea..X@...S..e...|
0060d6a0  5c 41 79 71 22 d4 dc 57  26 d2 06 d6 4a d0 ae 84  |\Ayq"..W&...J...|
0060d6b0  81 45 2a 84 82 97 35 e5  5c 40 22 85 d8 43 fc 4b  |.E*...5.\@"..C.K|
0060d6c0  0c 43 82 97 39 ed 71 46  81 45 48 00 03 29 04 00  |.C..9.qF.EH..)..|
0060d6d0  97 f0 c6 ff e7 80 00 9c  37 07 00 01 93 07 00 02  |........7.......|
0060d6e0  63 f3 e4 00 e1 47 a3 03  f1 00 26 c4 37 07 00 01  |c....G....&.7...|
0060d6f0  93 07 c0 0d 63 f4 e4 00  93 07 80 0d 23 1c f1 00  |....c.......#...|
0060d700  83 27 09 00 4c 00 4a 85  dc 43 82 97 19 e9 08 40  |.'..L.J..C.....@|
0060d710  1c 41 fc 43 89 ef 5c 40  22 85 d8 43 fc 4b 0c 47  |.A.C..\@"..C.K.G|
0060d720  82 97 b2 50 22 54 92 54  02 59 45 61 82 80 58 40  |...P"T.T.YEa..X@|
0060d730  a6 85 50 53 82 97 65 d1  ed b7 00 00 00 00 00 50  |..PS..e........P|
0060d740  34 00 00 00 82 80 00 00  00 00 00 00 00 00 00 00  |4...............|
0060d750  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
0060d770  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 2c  |...............,|
0060d780  d6 3c d4 aa 71 81 97 5a  2f 8c 8a bf a1 af ff 7e  |.<..q..Z/......~|
0060d790  23 a5 58 41 6e 82 2b 01  3d 53 cc 59 f7 83 b9 5e  |#.XAn.+.=S.Y...^|
0060d7a0
```

and 

```
hexdump -C app0.bin|tail -n 60                                                                                                                                                                                                             
0060d410  f5 00 18 49 bd 47 13 05  50 10 63 e6 e7 00 01 45  |...I.G..P.c....E|
0060d420  82 80 13 05 50 10 82 80  01 45 82 80 13 d7 05 01  |....P....E......|
0060d430  93 07 d0 0c 13 05 50 10  63 1a f7 00 c1 67 93 87  |......P.c....g..|
0060d440  07 f0 fd 8d 99 67 63 93  f5 00 01 45 82 80 11 45  |.....gc....E...E|
0060d450  82 80 c1 81 93 07 f0 0e  01 45 63 84 f5 00 13 05  |.........Ec.....|
0060d460  50 10 82 80 03 45 85 01  e1 47 33 b5 a7 00 06 05  |P....E...G3.....|
0060d470  13 65 45 00 82 80 19 71  ce d6 b7 a9 ca 3f 83 a7  |.eE....q.....?..|
0060d480  c9 2d de ce da d0 be c6  5c 41 37 07 00 01 2e 8b  |.-......\A7.....|
0060d490  83 ab c7 04 bc 5f b3 05  d6 00 a2 dc a6 da d2 d4  |....._..........|
0060d4a0  d6 d2 86 de ca d8 e2 cc  e6 ca b3 35 b7 00 aa 8a  |...........5....|
0060d4b0  32 84 b6 84 82 97 93 07  60 10 2a 8a 63 10 f5 0a  |2.......`.*.c...|
0060d4c0  ef e0 3f be b7 65 c9 3f  37 66 c9 3f 13 87 c5 bd  |..?..e.?7f.?....|
0060d4d0  aa 86 13 06 c6 8f 93 85  c5 bd 05 45 97 a0 d2 01  |...........E....|
0060d4e0  e7 80 60 5a 36 47 83 a7  c9 2d 52 85 63 0c f7 06  |..`Z6G...-R.c...|
0060d4f0  ef 00 4f a7 13 06 00 04  93 05 f0 0f 68 00 97 f0  |..O.........h...|
0060d500  c6 ff e7 80 20 b9 03 a5  0a 00 34 00 26 86 1c 41  |.... .....4.&..A|
0060d510  5e 87 a2 85 dc 5b 33 09  94 00 82 97 22 46 aa 86  |^....[3....."F..|
0060d520  b3 07 a6 00 b3 0c c4 40  63 f3 27 01 3e 89 03 a5  |.......@c.'.>...|
0060d530  0a 00 6c 00 33 0c 89 40  18 41 33 04 24 41 a2 94  |..l.3..@.A3.$A..|
0060d540  58 57 4a 84 02 97 7c 00  2a 8a 62 86 5a 85 b3 85  |XWJ...|.*.b.Z...|
0060d550  97 01 97 f0 c6 ff e7 80  20 b4 62 9b e3 14 0a f8  |........ .b.....|
0060d560  d1 f8 49 b7 f6 50 66 54  d6 54 46 59 b6 59 26 5a  |..I..PfT.TFY.Y&Z|
0060d570  96 5a 06 5b f6 4b 66 4c  d6 4c 09 61 82 80 5c 41  |.Z.[.KfL.L.a..\A|
0060d580  39 71 4e d6 d8 43 ae 89  fc 4b 0c 43 22 dc 26 da  |9qN..C...K.C".&.|
0060d590  52 d4 06 de 4a d8 2a 84  b2 84 36 8a 82 97 21 ed  |R...J.*...6...!.|
0060d5a0  71 46 81 45 48 00 03 29  04 00 97 f0 c6 ff e7 80  |qF.EH..)........|
0060d5b0  60 ae 37 07 00 01 a3 02  41 01 93 07 00 02 63 f3  |`.7.....A.....c.|
0060d5c0  e4 00 e1 47 a3 03 f1 00  26 c4 4e c6 37 07 00 01  |...G....&.N.7...|
0060d5d0  c9 47 63 f3 e4 00 89 47  23 1c f1 00 83 27 09 00  |.Gc....G#....'..|
0060d5e0  4c 00 4a 85 dc 43 82 97  19 e5 5c 40 22 85 d8 43  |L.J..C....\@"..C|
0060d5f0  fc 4b 0c 4b 82 97 f2 50  62 54 d2 54 42 59 b2 59  |.K.K...PbT.TBY.Y|
0060d600  22 5a 21 61 82 80 5c 41  79 71 22 d4 dc 57 26 d2  |"Z!a..\Ayq"..W&.|
0060d610  06 d6 4a d0 ae 84 81 45  2a 84 82 97 35 e5 5c 40  |..J....E*...5.\@|
0060d620  22 85 d8 43 fc 4b 0c 43  82 97 39 ed 71 46 81 45  |"..C.K.C..9.qF.E|
0060d630  48 00 03 29 04 00 97 f0  c6 ff e7 80 a0 a5 37 07  |H..)..........7.|
0060d640  00 01 93 07 00 02 63 f3  e4 00 e1 47 a3 03 f1 00  |......c....G....|
0060d650  26 c4 37 07 00 01 93 07  10 02 63 f4 e4 00 93 07  |&.7.......c.....|
0060d660  00 02 23 1c f1 00 83 27  09 00 4c 00 4a 85 dc 43  |..#....'..L.J..C|
0060d670  82 97 19 e9 08 40 1c 41  fc 43 89 ef 5c 40 22 85  |.....@.A.C..\@".|
0060d680  d8 43 fc 4b 4c 47 82 97  b2 50 22 54 92 54 02 59  |.C.KLG...P"T.T.Y|
0060d690  45 61 82 80 58 40 a6 85  10 53 82 97 65 d1 ed b7  |Ea..X@...S..e...|
0060d6a0  5c 41 79 71 22 d4 dc 57  26 d2 06 d6 4a d0 ae 84  |\Ayq"..W&...J...|
0060d6b0  81 45 2a 84 82 97 35 e5  5c 40 22 85 d8 43 fc 4b  |.E*...5.\@"..C.K|
0060d6c0  0c 43 82 97 39 ed 71 46  81 45 48 00 03 29 04 00  |.C..9.qF.EH..)..|
0060d6d0  97 f0 c6 ff e7 80 00 9c  37 07 00 01 93 07 00 02  |........7.......|
0060d6e0  63 f3 e4 00 e1 47 a3 03  f1 00 26 c4 37 07 00 01  |c....G....&.7...|
0060d6f0  93 07 c0 0d 63 f4 e4 00  93 07 80 0d 23 1c f1 00  |....c.......#...|
0060d700  83 27 09 00 4c 00 4a 85  dc 43 82 97 19 e9 08 40  |.'..L.J..C.....@|
0060d710  1c 41 fc 43 89 ef 5c 40  22 85 d8 43 fc 4b 0c 47  |.A.C..\@"..C.K.G|
0060d720  82 97 b2 50 22 54 92 54  02 59 45 61 82 80 58 40  |...P"T.T.YEa..X@|
0060d730  a6 85 50 53 82 97 65 d1  ed b7 00 00 00 00 00 50  |..PS..e........P|
0060d740  34 00 00 00 82 80 00 00  00 00 00 00 00 00 00 00  |4...............|
0060d750  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
0060d770  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 2c  |...............,|
0060d780  d6 3c d4 aa 71 81 97 5a  2f 8c 8a bf a1 af ff 7e  |.<..q..Z/......~|
0060d790  23 a5 58 41 6e 82 2b 01  3d 53 cc 59 f7 83 b9 5e  |#.XAn.+.=S.Y...^|
0060d7a0  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00640000
```

This shows that we have the same bytes in the api firmware download as in the firmware pull, except the version in the firmware pull also includes the unused 0xFF bytes, which don't do anything.
To thoroughly confirm that they are the exact same, we can use dd to copy the bytes up to where the data is unused by the firmware pull:
`dd if=firmware_pull.bin of=app0.bin bs=1 skip=$((0x10000)) count=$((0x60d7a0))`, where 0x60d7a0 is the end of the data from the official api firmware pull, and also where our own firmware pull simply contains unused 0xFF bytes to fill in the unused memory.

Then we can check to see if the files differ using `diff app0.bin V3.0.7-EN.bin`, which should not output anything if they are the same. If they are different, we will see: `Binary files app0.bin and V3.0.7-EN.bin differ`. For our example device, which has our backup partition app0 on version V3.0.7, they are the same.

Doing the same for app1, one can see that it is slightly different. The latest image is flashed to app1, and app0 is the backup firmware image (typically on the previous version) in case something happens to app1. One can check the version string of each partition with:

`strings app0.bin |grep V3` and look for the version number.

Therefore, if we want to simply do an update without overwriting the bootloader or other partitions, we can simply overwrite the firmware at the offset of app0 with the new version fetched from the official API endpoint:
`esptool --port /dev/ttyACM0 write-flash 0x650000 V3.0.8-EN.bin` , where `0x650000` is the offset of app1 from the parsed partition table. 

This is also much faster than a full firmware flash, since less data is being flashed to the device. It is also typically much faster than syncing updates on the device itself. Optionally, to replace the backup image on app0 with a different version, one can do the same command, but using the app0.bin offset instead. For stability, it may make sense to use one version previous than the latest (as the device normally would do), though this can technically be any version. I would recommend downloading a fresh version from the api as demonstrated above, as it won't have the cached data that you would have if you copied your app1 partition to app0.

