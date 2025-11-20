#!/usr/bin/env python3
"""
Render binary/hex data as an 8-pixel wide image with unlimited height.
Each byte becomes one row of 8 pixels.
"""

from PIL import Image
import argparse
import sys


def bytes_to_image(data, output_filename, scale=1, invert=False, add_grid=False, rotate=True):
    """
    Convert bytes to an 8-pixel wide image.

    Args:
        data: Bytes to render
        output_filename: Output image filename
        scale: Pixel scale factor
        invert: Invert colors (white on black)
        add_grid: Add grid lines between pixels
        rotate: Rotate image 90 degrees (default: True)
    """
    row_width = 8
    num_rows = len(data)

    # Image dimensions
    width = row_width * scale
    height = num_rows * scale

    bg_color = (0, 0, 0) if invert else (255, 255, 255)
    fg_color = (255, 255, 255) if invert else (0, 0, 0)

    img = Image.new('RGB', (width, height), color=bg_color)
    pixels = img.load()

    # Render each byte as a row
    for row_idx, byte_val in enumerate(data):
        for bit_idx in range(8):
            is_set = byte_val & (0x80 >> bit_idx)
            color = fg_color if is_set else bg_color

            # Draw scaled pixel
            x_start = bit_idx * scale
            y_start = row_idx * scale

            for dy in range(scale):
                for dx in range(scale):
                    x = x_start + dx
                    y = y_start + dy
                    if x < width and y < height:
                        pixels[x, y] = color

    # Add grid if requested
    if add_grid:
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        grid_color = (128, 128, 128)

        # Vertical lines
        for x in range(0, width + 1, scale):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)

        # Horizontal lines
        for y in range(0, height + 1, scale):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Rotate 90 degrees (clockwise)
    if rotate:
        img = img.transpose(Image.ROTATE_90)
        final_width, final_height = img.size
    else:
        final_width, final_height = width, height

    img.save(output_filename)
    print(f" Created {output_filename}")
    print(f"  Size: {final_width}x{final_height} pixels" + (" (rotated 90 degrees)" if rotate else ""))
    print(f"  Rows: {num_rows}")
    return img


def main():
    parser = argparse.ArgumentParser(
        description='Render binary data as 8-pixel wide image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From binary file
  %(prog)s -f font.bin -o output.png

  # From hex string
  %(prog)s -x "00 18 24 42 7E 42 42 00 FF AA 55" -o output.png

  # With scaling and grid
  %(prog)s -f data.bin -o output.png -s 10 --grid

  # From specific offset in file
  %(prog)s -f app0.bin --offset 0x483e20 --count 760 -o font.png -s 8
        """)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='Binary file input')
    group.add_argument('-x', '--hex', help='Hex string input')

    parser.add_argument('-o', '--output', required=True, help='Output image filename')
    parser.add_argument('--offset', help='Byte offset to start reading (hex or decimal)')
    parser.add_argument('--count', type=int, help='Number of bytes to read')
    parser.add_argument('-s', '--scale', type=int, default=1,
                       help='Pixel scale factor (default: 1)')
    parser.add_argument('--grid', action='store_true',
                       help='Add grid lines between pixels')
    parser.add_argument('--invert', action='store_true',
                       help='Invert colors (white on black)')
    parser.add_argument('--no-rotate', action='store_true',
                       help='Do not rotate image 90 degrees')

    args = parser.parse_args()

    # Read data
    if args.file:
        with open(args.file, 'rb') as f:
            if args.offset:
                # Parse offset (support hex like 0x1234 or decimal)
                offset = int(args.offset, 0)
                f.seek(offset)

            if args.count:
                data = f.read(args.count)
            else:
                data = f.read()
    else:
        # Parse hex string
        hex_clean = args.hex.replace(' ', '').replace('\n', '').replace('\t', '')
        data = bytes.fromhex(hex_clean)

    if len(data) == 0:
        print("Error: No data to render")
        return 1

    bytes_to_image(data, args.output, scale=args.scale,
                   invert=args.invert, add_grid=args.grid,
                   rotate=not args.no_rotate)
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Interactive mode
        print("Alpha - 8-pixel wide renderer")
        print("=" * 50)

        choice = input("Read from [f]ile or [h]ex string? ").strip().lower()

        if choice == 'f':
            filename = input("Input file: ").strip()
            offset_str = input("Offset (leave empty for start): ").strip()
            count_str = input("Byte count (leave empty for all): ").strip()

            with open(filename, 'rb') as f:
                if offset_str:
                    offset = int(offset_str, 0)
                    f.seek(offset)

                if count_str:
                    data = f.read(int(count_str))
                else:
                    data = f.read()
        else:
            hex_input = input("Enter hex data: ").strip()
            hex_clean = hex_input.replace(' ', '').replace('\n', '')
            data = bytes.fromhex(hex_clean)

        output = input("Output filename (default: output.png): ").strip()
        if not output:
            output = "output.png"

        scale = input("Scale factor (default: 1): ").strip()
        scale = int(scale) if scale else 1

        bytes_to_image(data, output, scale=scale)
    else:
        sys.exit(main())
