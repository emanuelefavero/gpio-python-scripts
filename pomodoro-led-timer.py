"""
Pomodoro LED Timer

Connect the following pins of Raspberry Pi Pico:

- LED: Pin 15
- Button: Pin 14

How to use it:
1. Press the Pin 14 button to start the Pomodoro timer.
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
POMODORO_DURATION = 25 * 60  # 25 minutes in seconds
LONG_PRESS_DURATION = 1  # seconds

# State variables
state = "stopped"  # "stopped", "running", "paused", "finished"
start_time = 0
elapsed = 0
press_time = None

# Blinking timers
blink_timer = Timer()


def stop_blinking():
    blink_timer.deinit()
    led.value(0)


def blink_led(frequency):
    def toggle(timer):
        led.toggle()

    blink_timer.init(freq=frequency, mode=Timer.PERIODIC, callback=toggle)


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
        blink_led(1)
        print("Timer paused")

    elif state == "paused":
        state = "running"
        start_time = utime.time()
        stop_blinking()
        led.value(1)
        print("Timer resumed")

    elif state == "finished":
        # Reset timer and LED, return to 'stopped' state
        stop_blinking()
        state = "stopped"
        elapsed = 0
        print("Timer reset after finish, ready to start again")


# Attach interrupt for rising edge
button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)


def check_long_press():
    global state, start_time, elapsed, press_time

    elapsed_ms = utime.ticks_diff(utime.ticks_ms(), press_time)

    if button.value():
        if press_time is None:
            press_time = utime.ticks_ms()
        elif elapsed_ms >= LONG_PRESS_DURATION * 1000:
            # Long press detected
            press_time = None
            state = "stopped"
            elapsed = 0
            stop_blinking()
            print("Timer reset by long press")
            # Wait until button is released to avoid re-triggering
            while button.value():
                utime.sleep(0.01)
    else:
        press_time = None


# Main loop
while True:
    check_long_press()

    if state == "running":
        total_elapsed = elapsed + (utime.time() - start_time)
        if total_elapsed >= POMODORO_DURATION:
            state = "finished"
            blink_led(5)
            print("Pomodoro finished")

    utime.sleep(0.1)
