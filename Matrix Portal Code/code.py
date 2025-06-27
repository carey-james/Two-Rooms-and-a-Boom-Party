# --- Imports ---
# - Lib Imports -
import audiocore
import audioio
import board
import digitalio
import displayio
import os
import rtc
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix
from adafruit_matrixportal.network import Network

# --- Env Variables Imports ---
timer_server = os.getenv('TIMER_SERVER')
colon_blink = os.getenv('COLON_BLINK') == 'true'
beep_audio = os.getenv('BEEP_AUDIO') == 'true'
beep_file = os.getenv('BEEP_FILE')
room_name = os.getenv('ROOM_NAME')

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
color[2] = 0x00AAFF # blue
color[3] = 0x3DEB34 # green
# - TileGrid -
tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
group.append(tile_grid)
display.root_group = group
# - Font -
font = bitmap_font.load_font('/fonts/IBMPlexMono-Medium-24_jep.bdf')
# - Clock Label -
clock_label = Label(font)
clock_label.color = color[1]
clock_label.text = '00:00'
group.append(clock_label)
# - Label Bounding Box, center the label -
bbx, bby, bbw, bbh = clock_label.bounding_box
clock_label.x = round((display.width / 2) - (bbw / 2))
clock_label.y = display.height // 2

# --- Speaker Setup ---
# Use A0 for audio output (PWM)
audio = audioio.AudioOut(board.A0)
# Open the WAV file
beep = audiocore.WaveFile(open(f'{beep_file}', 'rb'))

# --- Wifi Setup ---
network = Network(status_neopixel=board.NEOPIXEL, debug=True)
#network.get_local_time()

# --- Speaker Beep Method ---
def speaker_beep():
	audio.play(beep)

# --- Timer Update Method ---
def update_timer(remaining_time):
	now = time.localtime()
	colon = ':'

	# Convert remaining time to secs and mins
	secs = remaining_time % 60
	mins = remaining_time // 60

	# Colon Blink and Beep
	millisec = int(f'{time.monotonic():.1f}'[-1])
	if colon_blink and (millisec > 4):
		colon = ' '
	if beep_audio and (millisec == 0):
		speaker_beep()


	# Update Clock
	text = f'{mins:02d}{colon}{secs:02d}'
	clock_label.text = text
	return text

# --- Time Get Method ---
def get_remaining_time():
	remaining_time = 0
	try:
		# Fetch data from the timer server
		time_response = network.fetch_data(f'{timer_server}', json_path=([]))
		# Extract the remaining time in seconds
		remaining_time = time_response['remaining_seconds']
	except RuntimeError as e:
		print(f'A runtime error occurred with the time fetch. {e}')
	except Exception as e:
		print(f'An unknown error occurred with the time fetch: {e}')
	return remaining_time

# --- Room Name Method ---
def get_room_name():
	if room_name == 'WEST':
		clock_label.color = color[2]
	else:
		clock_label.color = color[1]
	text = f'{room_name}'
	clock_label.text = text
	return text

# --- Main Method ---
def main():
	# Loading...
	clock_label.color = color[3]
	clock_label.text = 'Setup'
	network.get_local_time()
	print(time.monotonic())

	while True:
		remaining_time = get_remaining_time()
        if remaining_time > 0:
            update_timer(remaining_time)
        else:
            display_text("00:00")

if __name__ == '__main__':
	main()
