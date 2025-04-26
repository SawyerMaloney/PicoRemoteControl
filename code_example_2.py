import board, digitalio, time
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT

while True and (time.monotonic() - __start_time) < __max_time:
    led.value = not led.value
    time.sleep(.1)

led.deinit()
