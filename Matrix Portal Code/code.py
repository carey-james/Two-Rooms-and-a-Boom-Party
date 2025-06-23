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

########################
test_time = time.time() + 300
########################

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
		time_response = network.fetch_data(f'{timer_server}', json_path=([]))
		remaining_time = time_response['remaining_seconds']
	except RuntimeError as e:
		print(f'A runtime error occured with the time fetch. {e}')
		pass
	except:
		print('An unknown error occured with the time fetch.')
		pass
	return remaining_time

#############################
# --- Test Remaining Time ---
def test_remaining_time():
	now = time.time()
	if (now < test_time):
		return (test_time - now)
	else:
		return 0
#############################

# --- Main Method ---
def main():
	while True:
		text = update_timer(test_remaining_time())
		print(f'{text}')
		time.sleep(0.1)

if __name__ == '__main__':
	main()
