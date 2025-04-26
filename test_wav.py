wav_file_object = open("wand.wav", "rb")
wav_file = wav_file_object.read()
wav_file_object.close()

byte_count = 0
byte_increment = 8192

while byte_increment + byte_count < len(wav_file):
    with open("new_wav.wav", "ab") as f:
        f.write(wav_file[byte_count:byte_count + byte_increment])

    byte_count += byte_increment

with open("new_wav.wav", "ab") as f:
    f.write(wav_file[byte_count:])
