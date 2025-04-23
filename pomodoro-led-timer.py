# TODO Add blue LED for 5 minutes rest time

from machine import Pin, Timer
import utime

# Pin setup
led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

# Constants
POMODORO_DURATION = 25 * 60  # 25 minutes in seconds

# State variables
state = "stopped"  # can be: "stopped", "running", "paused", "finished"
start_time = 0
elapsed = 0

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
        # Start timer
        state = "running"
        start_time = utime.time()
        led.value(1)
        print("Timer started")

    elif state == "running":
        # Pause timer
        state = "paused"
        elapsed += utime.time() - start_time
        blink_led(1)  # slow blink
        print("Timer paused")

    elif state == "paused":
        # Resume timer
        state = "running"
        start_time = utime.time()
        stop_blinking()
        led.value(1)
        print("Timer resumed")

    elif state == "finished":
        # Restart timer
        state = "running"
        start_time = utime.time()
        elapsed = 0
        stop_blinking()
        led.value(1)
        print("Timer restarted after finish")


button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

# Main loop
while True:
    if state == "running":
        total_elapsed = elapsed + (utime.time() - start_time)
        if total_elapsed >= POMODORO_DURATION:
            state = "finished"
            blink_led(5)  # fast blink
            print("Pomodoro finished")
    utime.sleep(0.1)
