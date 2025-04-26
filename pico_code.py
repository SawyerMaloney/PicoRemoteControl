import os
import time
import wifi
import socketpool
import adafruit_requests
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile
import board

# play_sound function - pass in the FULL NAME of file to play
def play_sound(filename):
    audio = AudioOut(board.GP15)  # Assuming you've got tip of speaker plug wired to GP16
    print(f"playing sound {filename}")
    with open(filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass
    audio.deinit()


SSID = os.getenv("CIRCUITPY_WIFI_SSID")
PASSWORD = os.getenv("CIRCUITPY_WIFI_PASSWORD")
SERVER_URL = "http://136.167.196.177:5000/"  # Update this!


# Set up WiFi connection
def connect_wifi():
    print("Connecting to", SSID)
    wifi.radio.connect(SSID, PASSWORD)
    print("Connected! IP:", wifi.radio.ipv4_address)


# Initialize network components
pool = socketpool.SocketPool(wifi.radio)
session = adafruit_requests.Session(pool)

def grab_remote_code(code, has_code):
    try:
        print("Fetching code from server...")
        # check to see if we need to get new code
        check_update = session.get(SERVER_URL + "check_update").text
        if check_update == "1" or not has_code: # if there is new code or if we don't have anything to run yet
            has_code = True
            response = session.get(SERVER_URL + "code")
            code = response.text
            response.close()
            print("code fetched")
            return code, has_code
        else:
            print("did not return new code")
            return code, has_code
    except Exception as e:
        print("Error:", e)


def execute_remote_code(code):
    try:
        print("Executing remote code...")
        start_time = time.monotonic()
        # enforced in sent code that it only runs for max time seconds
        env = {"__start_time": start_time, "__max_time": 5}
        exec(code, env)
        print("code finished executing")
    except Exception as e:
        print(f"Error in executing: {e}")
        session.post(SERVER_URL + "error", data=str(e))

def write_bytes(filename, bytes, mode):
    with open(filename, mode) as f:
        f.write(bytes)

def next_bytes():
    response = session.get(SERVER_URL + "wav_file").content
    print(f"in next_bytes, got response size: {len(response)}")
    return response

def get_wav_file_info():
    response = session.get(SERVER_URL + "wav_file_info")
    filename, chunk_size = response.text.split(",")
    return filename, int(chunk_size)

def get_wav_files():
    filename, chunk_size = get_wav_file_info()
    wav_file_bytes = next_bytes()
    write_bytes(filename, wav_file_bytes, "wb")
    wav_file_bytes = next_bytes()
    while len(wav_file_bytes) == chunk_size:  # standard length for information
        write_bytes(filename, wav_file_bytes, "ab")
        wav_file_bytes = next_bytes()
    # one last piece to write
    write_bytes(filename, wav_file_bytes, "ab")
    sounds.append(filename)
    return filename

def delete_wavs():
    if os.getcwd != "/sounds":
        print("changing directories to delete")
        os.chdir("/sounds")

    for sound in sounds:
        try:
            os.remove(sound)
            print(f"removed sound {sound}")
        except:
            print(f"tried to remove {sound}. failed.")

# update function that will allows us to handle any
# commands the server needs us to do
def update():
    response = session.get(SERVER_URL + "update")
    commands = response.text.split(",")
    print(f"received commands: {commands}")
    for command in commands:
        if command == "say_hi":
            print("Saying hi to the operator!")
        elif command == "delete_wavs":
            delete_wavs()
        elif command == "update_wavs":
            print("planning to update wavs...")
            return True


# Main execution flow
connect_wifi()

remote_code = ""
has_code = False
wants_wav = False
filename = ""
sounds = []
path = "sounds/"


while True:
    wants_wav = update()
    remote_code, has_code = grab_remote_code(remote_code, has_code)
    if wants_wav:
        wants_wav = not wants_wav
        filename = get_wav_files()
        play_sound(filename)
    execute_remote_code(remote_code)