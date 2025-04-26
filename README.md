### Pico W Remote Access
By Sawyer Maloney

This code allows you to remotely access your Pico W and send it new code and audio files to execute. You can send messages across the seas, or remotely update any number of Pico's that you may have distributed around your house, school, or the world.

The code comes in a number of parts. There is the flask server, called server.py. There is the userapp.py, which is built to allow a user at a computer terminal to access their Picos. And then there is pico_code.py, which should be renamed code.py and put onto your Pico to be executed. The other files are files I used in testing or example wav files to send over, which should be helpful if you're trying to debug anything.
