import machine
import utime
# IMPORT MULTI THREAD LIBRARY
# to run 2 loops at the same time
import _thread

led_red = machine.Pin(2, machine.Pin.OUT)
led_yellow = machine.Pin(3, machine.Pin.OUT)
led_green = machine.Pin(4, machine.Pin.OUT)

button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(12, machine.Pin.OUT)

# DEFINE GLOBAL VARIABLE
global button_pressed
button_pressed = False


def button_reader_thread():
    global button_pressed
    while True:
        if button.value() == 1:
            button_pressed = True
        utime.sleep(0.01)


# START NEW THREAD
_thread.start_new_thread(button_reader_thread, ())

# MAIN LOOP
while True:

    # THIS CODE CHECKS IF BUTTON IS PRESSED AT ANY TIME DURING LAST LOOP
    if button_pressed is True:
        led_red.value(1)
        for i in range(8):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        global button_pressed
        button_pressed = False

    led_red.value(1)
    utime.sleep(5)
    led_yellow.value(1)
    utime.sleep(2)
    led_red.value(0)
    led_yellow.value(0)
    led_green.value(1)
    utime.sleep(5)
    led_green.value(0)
    led_yellow.value(1)
    utime.sleep(5)
    led_yellow.value(0)
