from flask import Flask, request

app = Flask(__name__)


@app.route('/code', methods=['GET', 'POST'])
def handle_code():
    return picoServer.handle_code()


@app.route("/check_update", methods=['GET', 'POST'])
def check_update():
    return picoServer.check_update()


@app.route("/error", methods=['GET', 'POST'])
def error():
    return picoServer.error()


@app.route("/wav_file_info", methods=['GET'])
def wav_file_info():
    return picoServer.wav_file_info()


@app.route("/wav_file", methods=['GET'])
def send_wav_file():
    return picoServer.send_wav_file()


@app.route("/new", methods=['GET'])
def make_new_user():
    return picoServer.make_new_user()


@app.route("/update", methods=['GET'])
def update():
    return picoServer.update()


@app.route("/user", methods=['POST'])
def user_sending_information():
    try:
        user_ret = picoServer.user_sending_information(request.json)
        return user_ret
    except Exception as e:
        print(f"exception in flask: {e}")
        return


class UserState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.byte_count = 0


class PicoServer:
    def __init__(self):
        self.current_code = "print('Hello from Pico W!')"  # Default code
        self.filename = "code_example.py"
        self.new_code_available = "1"
        self.errors = []

        # read in raw wav file
        self.wav_filename = "wand.wav"
        self.wav_file = None
        self.byte_count = 0
        self.byte_increment = 8192
        self.users = []
        self.current_id = 0

        self.load_wav_file()  # loads wav_filename file into wav_file

        self.queued_commands = ["say_hi"]

    def load_wav_file(self):
        wav_file_object = open(self.wav_filename, "rb")
        self.wav_file = wav_file_object.read()
        wav_file_object.close()

    def make_new_user(self):
        self.users.append(UserState(self.current_id))
        self.current_id += 1

    def send_wav_file(self):
        if self.byte_count + self.byte_increment <= len(self.wav_file):
            ret_val = self.wav_file[self.byte_count:self.byte_count
                                    + self.byte_increment]
            self.byte_count += self.byte_increment
            print(f"in send_wav_file, returning response of length:\
                    {len(ret_val)}")
            return ret_val
        else:
            return self.wav_file[self.byte_count:]
        return self.wav_file

    def wav_file_info(self):
        # temporarily, reset all values
        # to be changed when handling multiple ids
        self.byte_count = 0
        return f"{self.wav_filename},{self.byte_increment}"

    def error(self):
        if request.method == 'POST':
            error_message = request.data.decode('utf-8')
            self.errors.append(error_message)
            print(f"received error message: {error_message}")
        return "error logged"

    def get_code_from_file(self, filename):
        with open(filename, "r") as f:
            return f.read()

    def handle_code(self):
        if request.method == 'GET':
            self.new_code_available = "0"
            return self.get_code_from_file(self.filename)
        elif request.method == 'POST':
            self.filename = request.json["filename"]
            self.new_code_available = "1"
            return "200"

    def check_update(self):
        return self.new_code_available

    def update(self):
        if len(self.queued_commands) != 0:
            commands = ""
            for command in self.queued_commands[1:]:
                commands += f"{command},"
            commands += self.queued_commands[0]
            print(f"returning commands {commands} from queued_commands {self.queued_commands}")
            self.queued_commands = []
            return commands
        else:
            return ""

    def user_sending_information(self, data):
        try:
            self.wav_filename = data["filename"]
            # queue adding wav
            self.queued_commands.append("update_wavs")
            self.queued_commands.append("delete_wavs")

            # update wav file object
            self.load_wav_file()
            return "200"
        except Exception as e:
            print(f"exception {e}")


picoServer = PicoServer()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
