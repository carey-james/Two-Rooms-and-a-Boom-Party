# --- Imports ---
# - Lib Imports -
import board
import displayio
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix
from adafruit_matrixportal.network import Network
# - Secrets Imports -
from secrets import secrets

# --- Display Setup ---
matrix = Matrix()
display = matrix.display

# --- Graphics Setup ---
group = displayio.Group()
bitmap = displayio.Bitmap(64, 32, 2) # Width, Height, Bit depth
# - Color Palette -
color = displayio.Palette(4)
color[0] = 0x000000 # black
color[1] = 0xFF0000 # red
color[2] = 0xFF8C00 # orange
color[3] = 0x3DEB34 # green
# - TileGrid -
tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
group.append(tile_grid)
display.root_group = group
# - Font -
font = bitmap_font.load_font('/fonts/IBMPlexMono-Medium-24_jep.bdf')
# - Clock Label -
clock_label = Label(font)

# --- Wifi Setup ---
network = Network(status_neopixel=board.NEOPIXEL, debug=True)
