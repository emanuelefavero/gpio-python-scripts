"""
Simple Timer

Connect the following pins of Raspberry Pi Pico:

- LED: Pin 15
- Button: Pin 14

How to use it:
1. Press the Pin 14 button to start the timer.
2. The LED will turn on.
3. Press the Pin 14 button again to pause the timer (LED will blink slowly).
4. Press the Pin 14 button again to resume the timer (LED will turn on).
5. Press the Pin 14 button for 1 second to reset the timer.
6. The LED will blink quickly to indicate the timer has finished.
7. Press the Pin 14 button to reset the timer and turn off the LED.
"""

from machine import Pin, Timer
import utime

# Pin setup
led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

# Constants
DURATION = 6 * 60  # 6 minutes in seconds
LONG_PRESS_DURATION = 1  # seconds
DEBOUNCE_TIME = 200  # milliseconds

# State variables
state = "stopped"  # "stopped", "running", "paused", "finished"
start_time = 0
elapsed = 0
press_time = None
last_button_press = 0  # for debounce

# Blinking timer
blink_timer = Timer()


def stop_blinking():
    blink_timer.deinit()
    led.value(0)


def blink_led(frequency):
    def toggle(timer):
        led.toggle()

    blink_timer.init(freq=frequency, mode=Timer.PERIODIC, callback=toggle)


def debounced_button_handler(pin):
    global last_button_press
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_button_press) >= DEBOUNCE_TIME:
        last_button_press = now
        button_handler(pin)


def button_handler(pin):
    global state, start_time, elapsed

    if state == "stopped":
        state = "running"
        start_time = utime.time()
        led.value(1)
        print("Timer started")

    elif state == "running":
        state = "paused"
        elapsed += utime.time() - start_time
        blink_led(2)
        print("Timer paused")

    elif state == "paused":
        state = "running"
        start_time = utime.time()
        stop_blinking()
        led.value(1)
        print("Timer resumed")

    elif state == "finished":
        stop_blinking()
        state = "stopped"
        elapsed = 0
        print("Timer reset after finish, ready to start again")


# Attach debounced interrupt
button.irq(trigger=Pin.IRQ_RISING, handler=debounced_button_handler)


def check_long_press():
    global state, start_time, elapsed, press_time

    if button.value():
        if press_time is None:
            press_time = utime.ticks_ms()
        else:
            elapsed_ms = utime.ticks_diff(utime.ticks_ms(), press_time)
            if elapsed_ms >= LONG_PRESS_DURATION * 1000:
                press_time = None
                state = "stopped"
                elapsed = 0
                stop_blinking()
                print("Timer reset by long press")
                while button.value():
                    utime.sleep(0.01)
    else:
        press_time = None


# Main loop
while True:
    check_long_press()

    if state == "running":
        total_elapsed = elapsed + (utime.time() - start_time)
        if total_elapsed >= DURATION:
            state = "finished"
            blink_led(5)
            print("Timer finished")

    utime.sleep(0.1)
