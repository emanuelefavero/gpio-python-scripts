"""
Pomodoro LED Timer with Break Functionality

Connect the following pins of Raspberry Pi Pico:
- LED: Pin 15
- Button: Pin 14
- Break LED: Pin 16
- Break Button: Pin 17

How to use it:
1. Press the Pin 14 button to start the Pomodoro timer.
2. The LED will turn on.
3. Press the Pin 14 button again to pause the timer (LED will blink slowly).
4. Press the Pin 14 button again to resume the timer (LED will turn on).
5. Press the Pin 17 button to start the break timer.
6. The Break LED will turn on.
7. Press the Pin 17 button again to pause the break timer
8. Press the Pin 17 button again to resume the break timer
9. Press both buttons simultaneously to reset all timers.
"""

from machine import Pin, Timer
import utime


# Pin setup
pomodoro_led = Pin(15, Pin.OUT)
pomodoro_button = Pin(14, Pin.IN, Pin.PULL_DOWN)

break_led = Pin(16, Pin.OUT)
break_button = Pin(17, Pin.IN, Pin.PULL_DOWN)

# Constants
POMODORO_DURATION = 25 * 60  # * 25 minutes
BREAK_DURATION = 5 * 60  # * 5 minutes

# Timer states
state = "stopped"  # "stopped", "running", "paused", "finished"
mode = "pomodoro"  # or "break"

start_time = 0
elapsed = 0

# Blinking
blink_timer = Timer()


def stop_blinking():
    blink_timer.deinit()
    pomodoro_led.value(0)
    break_led.value(0)


def blink_led(led, frequency):
    def toggle(timer):
        led.toggle()

    blink_timer.init(freq=frequency, mode=Timer.PERIODIC, callback=toggle)


def reset_all():
    global state, start_time, elapsed
    state = "stopped"
    elapsed = 0
    stop_blinking()
    print("Timers reset")


def start_timer(selected_mode):
    global state, mode, start_time, elapsed

    reset_all()
    mode = selected_mode
    state = "running"
    start_time = utime.time()

    if mode == "pomodoro":
        pomodoro_led.value(1)
        print("Pomodoro started")
    else:
        break_led.value(1)
        print("Break started")


def pause_timer():
    global state, elapsed

    if mode == "pomodoro":
        pomodoro_led.value(0)
        blink_led(pomodoro_led, 2)
    else:
        break_led.value(0)
        blink_led(break_led, 2)

    elapsed += utime.time() - start_time
    state = "paused"
    print("Timer paused")


def resume_timer():
    global state, start_time

    stop_blinking()
    state = "running"
    start_time = utime.time()

    if mode == "pomodoro":
        pomodoro_led.value(1)
    else:
        break_led.value(1)

    print("Timer resumed")


def finish_timer():
    global state
    state = "finished"

    if mode == "pomodoro":
        blink_led(pomodoro_led, 5)
        print("Pomodoro finished")
    else:
        blink_led(break_led, 5)
        print("Break finished")


def handle_button(button_mode):
    global state, mode

    if mode != button_mode and state == "running":
        reset_all()

    if mode != button_mode or state == "stopped":
        start_timer(button_mode)
    elif state == "running":
        pause_timer()
    elif state == "paused":
        resume_timer()
    elif state == "finished":
        start_timer(button_mode)


# Interrupts
def pomodoro_button_handler(pin):
    handle_button("pomodoro")


def break_button_handler(pin):
    handle_button("break")


pomodoro_button.irq(trigger=Pin.IRQ_RISING, handler=pomodoro_button_handler)
break_button.irq(trigger=Pin.IRQ_RISING, handler=break_button_handler)


# Check for both buttons being pressed simultaneously
def check_for_dual_button_press():
    if pomodoro_button.value() and break_button.value():
        reset_all()
        print("Both buttons pressed: Full reset")
        utime.sleep(0.5)  # debounce / prevent re-trigger


# Main loop
while True:
    check_for_dual_button_press()

    if state == "running":
        duration = POMODORO_DURATION if mode == "pomodoro" else BREAK_DURATION
        total_elapsed = elapsed + (utime.time() - start_time)
        if total_elapsed >= duration:
            finish_timer()

    utime.sleep(0.1)
