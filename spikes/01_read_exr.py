from collections import defaultdict
from pathlib import Path
import OpenImageIO as oiio
import os
import argparse
from rich.console import Console
from rich.table import Table

parser = argparse.ArgumentParser(description=
                                 "Script for get metadata from exr file") # create argument parser
parser.add_argument("filepath",
                    type=Path,
                    help="Path to needed exr file") # add positional argument for file path
args = parser.parse_args()

filepath = str(args.filepath) #extract file path from arguments

if not os.path.exists(filepath):
    print(f"File {filepath} does not exist.")
    exit(1)

if not os.path.isfile(filepath):
    print(f"{filepath} is not a file.")
    exit(1)

try:
    buffer = oiio.ImageBuf(filepath) # create image buffer from file

    if not buffer.initialized:
        print(f"Failed to read image from {filepath}.")
        exit(1)

    spec = buffer.nativespec() # get image specification (for extract metadata)
    #buffer.read(0, 0, force=True,convert=oiio.TypeDesc('half')) # read image data into buffer

    if spec.width <= 0 or spec.height <= 0:
        print(f"Image {filepath} has invalid dimensions.")
        exit(1)

except Exception as e:
    print(f"Error reading image {filepath}: {e}")
    exit(1)

width = spec.width # get image width
height = spec.height # get image height
data_format = spec.format # get image data format (e.g., 16, 32, float, etc.)
compression = spec.get_string_attribute("compression", "unknown") # get compression type
file_size_bytes = os.path.getsize(filepath) # get file size in bytes
nchannels = spec.nchannels # get count of channels
channels = [channel.replace('ViewLayer.', '') for channel in spec.channelnames] # get channel names

console = Console()
table = Table(title="EXR Image Metadata. Primary parameters", header_style="bold magenta")
table.add_column("Параметр")
table.add_column("Значение")

table.add_row("Разрешение", f"{width} x {height}")
table.add_row("Формат данных", str(data_format))
table.add_row("Сжатие", str(compression))
table.add_row("Размер файла (мб)", f"{file_size_bytes / (1024 * 1024):.2f}")
table.add_row("Количество каналов", str(nchannels))

console.print(table)

print("Список каналов:")
groups = defaultdict(list)
for channel in channels:
    if '.' in channel:
        prefix = channel.split('.')[0]
        groups[prefix].append(channel)
    else:
        groups["Other"].append(channel)

for group, items in groups.items():
    print(f'{group}')
    print('\t', ', '.join(items))
    print()

x_nuke = 976
y_nuke = 338

y_oiio = height - 1 - y_nuke # convert Nuke's y-coordinate to OIIO's coordinate system

print(f"Значение коордитат пикселя в Nuke: ({x_nuke}, {y_nuke})")
print(f"Значение коордитат пикселя в OIIO: ({x_nuke}, {y_oiio})")

red_idx = spec.channelindex("ViewLayer.Combined.R")
green_idx = spec.channelindex("ViewLayer.Combined.G")
blue_idx = spec.channelindex("ViewLayer.Combined.B")
alpha_idx = spec.channelindex("ViewLayer.Combined.A")

x_final = x_nuke
y_final = y_nuke

pixel = buffer.getpixel(x_final, height - 1 - y_final)

r = pixel[red_idx] if red_idx != -1 else None
g = pixel[green_idx] if green_idx != -1 else None
b = pixel[blue_idx] if blue_idx != -1 else None
a = pixel[alpha_idx] if alpha_idx != -1 else None

table = Table(title=f"Значение пикселя ({x_final}, {y_final})", header_style="bold magenta")
table.add_column("Канал")
table.add_column("Значение (с флипом)")
table.add_row("R", f"{r:.6f}" if r is not None else "None")
table.add_row("G", f"{g:.6f}" if g is not None else "None")
table.add_row("B", f"{b:.6f}" if b is not None else "None")
table.add_row("A", f"{a:.6f}" if a is not None else "None")

console.print(table)
