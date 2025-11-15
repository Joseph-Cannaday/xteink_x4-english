#!/usr/bin/env python3
import struct
import sys

ENTRY_SIZE = 32       # 32 bytes per partition entry
STRUCT_SIZE = 28      # First 28 bytes are the actual structure
MAGIC = 0x50AA

def parse_entry(entry):
    # First 28 bytes match <HBBII16s
    fields = entry[:STRUCT_SIZE]

    magic, ptype, subtype, offset, size, name = struct.unpack("<HBBII16s", fields)

    name = name.split(b'\x00', 1)[0].decode('ascii', errors='ignore')
    return magic, ptype, subtype, offset, size, name


def main():
    if len(sys.argv) != 2:
        print("Usage: parse_partition_table.py partition_table.bin")
        sys.exit(1)

    data = open(sys.argv[1], "rb").read()

    print("Partition Table:")
    print("--------------------------------------------------------------")
    print("Name           Type  Subtype      Offset       Size")
    print("--------------------------------------------------------------")

    for i in range(0, len(data), ENTRY_SIZE):
        entry = data[i:i+ENTRY_SIZE]
        if len(entry) < ENTRY_SIZE:
            break

        magic, ptype, subtype, offset, size, name = parse_entry(entry)

        if magic != MAGIC:
            continue
        if name == "":
            continue

        print(
            f"{name:<14}  0x{ptype:02X}    0x{subtype:02X}    "
            f"0x{offset:08X}  0x{size:08X}"
        )
        last_offset = offset
        last_size = size
        
    print(f"Command to pull entire firmware dump:\nesptool --port [usbport] read-flash 0x00000 {last_offset + last_size} firmware_pull.bin")

if __name__ == "__main__":
    main()

