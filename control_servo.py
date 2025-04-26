import keyboard, time

while True:
    if keyboard.is_pressed("q"):
        print("Quitting servo control...")
        break
    elif keyboard.is_pressed("left"):
        print("Moving servo left...")
    elif keyboard.is_pressed("right"):
        print("Moving servo right...")
    print("sleeping...")
    time.sleep(.1)
