# import lines needed to play sound files
import board, time
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

# set up the speaker
audio = AudioOut(board.GP15) # Assuming you've got tip of speaker plug wired to GP16

# set path where sound files can be found CHANGE if different folder name
path = "sounds/"

# play_sound function - pass in the FULL NAME of file to play
def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass
play_sound("wand.wav")

audio.deinit()
