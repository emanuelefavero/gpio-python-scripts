"""
Simple Timer With Buzzer

Connect the following pins of Raspberry Pi Pico:

- LED: Pin 15
- Button: Pin 14
- Buzzer: Pin 27

How to use it:
1. Press the Pin 14 button to start the timer.
2. The LED will turn on.
3. Press the Pin 14 button again to pause the timer (LED will blink slowly).
4. Press the Pin 14 button again to resume the timer (LED will turn on).
5. Press the Pin 14 button for 1 second to reset the timer.
6. The LED will blink quickly to indicate the timer has finished.
7. The buzzer will sound a series of tones when the timer finishes.
8. Press the Pin 14 button to reset the timer and turn off the LED.
"""

from machine import Pin, Timer, PWM
import utime

# Pin setup
led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(27))
buzzer.duty_u16(0)

# Constants
DURATION = 6 * 60  # 6 minutes
LONG_PRESS_DURATION = 1  # seconds
DEBOUNCE_TIME = 200  # milliseconds

# State variables
state = "stopped"
start_time = 0
elapsed = 0
press_time = None
last_press_time = 0  # for debouncing

# Buzzer state
buzzer_on = False
buzzer_stage = 0
buzzer_next_time = 0
buzzer_duration = 0
buzzer_silence = 0
buzzer_freqs = []
buzzer_current_index = 0

# Blink timer
blink_timer = Timer()


def stop_blinking():
    blink_timer.deinit()
    led.value(0)


def blink_led(frequency):
    def toggle(timer):
        led.toggle()

    blink_timer.init(freq=frequency, mode=Timer.PERIODIC, callback=toggle)


def button_handler(pin):
    global state, start_time, elapsed, last_press_time

    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_press_time) < DEBOUNCE_TIME:
        return  # debounce: ignore quick repeated presses

    last_press_time = current_time

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
        print("Timer reset after finish")


button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)


def check_long_press():
    global state, press_time, elapsed

    elapsed_since_press = (
        utime.ticks_diff(utime.ticks_ms(), press_time) if press_time else 0
    )

    if button.value():
        if press_time is None:
            press_time = utime.ticks_ms()
        elif elapsed_since_press >= LONG_PRESS_DURATION * 1000:
            press_time = None
            state = "stopped"
            elapsed = 0
            stop_blinking()
            print("Timer reset by long press")
            while button.value():
                utime.sleep(0.01)
    else:
        press_time = None


def activate_buzzer(duration=150, silence=150, freqs=[620, 720]):
    global buzzer_on, buzzer_stage, buzzer_next_time
    global buzzer_duration, buzzer_silence
    global buzzer_freqs, buzzer_current_index

    buzzer_on = True
    buzzer_stage = 1
    buzzer_duration = duration
    buzzer_silence = silence
    buzzer_freqs = freqs
    buzzer_current_index = 0

    buzzer.freq(buzzer_freqs[0])
    buzzer.duty_u16(32768)
    buzzer_next_time = utime.ticks_add(utime.ticks_ms(), buzzer_duration)


while True:
    check_long_press()

    freqs = [792, 745, 633, 444, 414, 664, 837, 1060]

    if state == "running":
        total_elapsed = elapsed + (utime.time() - start_time)
        if total_elapsed >= DURATION:
            state = "finished"
            blink_led(5)
            activate_buzzer(duration=1, silence=1, freqs=freqs)
            print("Timer finished")

    if buzzer_on and utime.ticks_diff(utime.ticks_ms(), buzzer_next_time) >= 0:
        if buzzer_stage == 1:
            buzzer.duty_u16(0)  # Silence
            buzzer_stage = 2
            buzzer_next_time = utime.ticks_add(utime.ticks_ms(), buzzer_silence)
        elif buzzer_stage == 2:
            buzzer_current_index += 1
            if buzzer_current_index < len(buzzer_freqs):
                buzzer.freq(buzzer_freqs[buzzer_current_index])
                buzzer.duty_u16(32768)
                buzzer_stage = 1
                ms = utime.ticks_ms()
                buzzer_next_time = utime.ticks_add(ms, buzzer_duration)
            else:
                buzzer.duty_u16(0)
                buzzer_on = False
                buzzer_stage = 0

    utime.sleep(0.085)
