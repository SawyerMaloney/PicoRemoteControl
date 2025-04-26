"""
    User app: control various parts of the pico,
    including sending different programs or engaging in servo control
"""

import time, keyboard, os, requests


class UserApp:
    def __init__(self):

        self.SERVER_URL = "http://136.167.196.177:5000/"
        self.example_code = ["code_example.py", "code_example_2.py", "code_example_3.py"]

        self.run()

    def run(self):
        print("Welcome to the Pico W Control server.")

        choose = input("Would you like to send a\
 wav file (w) or send code (c): ")

        if choose == "w":
            self.send_wav()
        elif choose == "c":
            self.send_code()

    def send_code(self):
        print(f"Here are the code examples you can upload: {self.example_code}")
        code_filename = input("Please enter the filename you would like to upload: ")
        data = {"filename": code_filename}
        requests.post(self.SERVER_URL + "code", json=data)

    def send_wav(self):
        current_files = os.listdir()
        wav_files = [files for files in current_files if ".wav" in files]
        print(f"Here are the current wav files accessible for sending: \n{wav_files}")
        wav_file = ""
        while wav_file not in wav_files:
            wav_file = input("Please enter the full name of one of the wav files to send: ")
            if wav_file not in wav_files:
                print(f"It doesn't appear that {wav_file} is a valid wav file")

        print(f"Selected wav file: {wav_file}")

        data = {"filename": wav_file}

        requests.post(self.SERVER_URL + "user", json=data)

user = UserApp()
