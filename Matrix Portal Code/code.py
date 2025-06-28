# --- Imports ---
# - Lib Imports -
import audiocore
import audioio
import board
import digitalio
import displayio
import gc
import os
import rtc
import time
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_matrixportal.matrix import Matrix
from adafruit_matrixportal.matrixportal import MatrixPortal
import adafruit_requests

# --- Env Variables Imports ---
timer_server = os.getenv('TIMER_SERVER')
colon_blink = os.getenv('COLON_BLINK') == 'true'
beep_audio = os.getenv('BEEP_AUDIO') == 'true'
beep_file = os.getenv('BEEP_FILE')
blip_file = os.getenv('BLIP_FILE')
room_name = os.getenv('ROOM_NAME')

# --- Display Setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)
display = matrixportal.display

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
# Open the WAV files
beep = audiocore.WaveFile(open(f'{beep_file}', 'rb'))
blip = audiocore.WaveFile(open(f'{blip_file}', 'rb'))

# --- Speaker Beep Method ---
def speaker_beep():
	audio.play(beep)
# --- Speaker Beep Method ---
def speaker_blip():
	audio.play(blip)

# --- Timer Update Method ---
def update_timer(remaining_time):
	colon = ':'

	# Convert remaining time to secs and mins
	secs = remaining_time % 60
	mins = remaining_time // 60

	# Colon Blink, Time Update, and Beep
	millisec = int(f'{time.monotonic():.1f}'[-1])
	if colon_blink and (millisec > 4):
		colon = ' '

	# Update Clock
	clock_label.text = f'{mins:02d}{colon}{secs:02d}'
	return remaining_time

# --- Time Get Method ---
def get_remaining_time():
    remaining_time = 0
    response = None

    try:
        # Use the existing, built-in requests session
        response = matrixportal.network.requests.get(timer_server)
        data = response.json()
        remaining_time = data.get('remaining_seconds', 0)
    except Exception as e:
        print(f"A runtime error occurred with the time fetch. {e}")
    finally:
        if response:
            try:
                response.close()  # 🔑 Critical: close socket
            except Exception as close_err:
                print("Error closing response:", close_err)
        gc.collect()  # 🔄 Free up memory and sockets

    return remaining_time

# --- Main Method ---
def main():
	# Loading...
	clock_label.color = color[2]
	clock_label.text = f'{room_name}.'
	matrixportal.get_local_time()
	clock_label.color = color[1]

	remaining_time = 0
	last_fetch_time = 0
	last_sec_time = 0

	while True:
		if ((remaining_time == 0) and ((time.monotonic() - last_fetch_time) > 1)) or ((time.monotonic() - last_fetch_time) > 59):
			remaining_time = update_timer(get_remaining_time())
			last_fetch_time = time.monotonic()
			last_sec_time = time.monotonic()
		elif remaining_time > 0:
			if ((time.monotonic() - last_sec_time) > 1):
				remaining_time = remaining_time - 1
				last_sec_time = time.monotonic()
				if (remaining_time < 30) and (remaining_time > 1):
					speaker_blip()
				elif (remaining_time == 1):
					speaker_beep()
			remaining_time = update_timer(remaining_time)
		else:
			clock_label.text = ("00:00")

if __name__ == '__main__':
	main()
