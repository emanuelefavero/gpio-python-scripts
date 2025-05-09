"""
Simple Timer With Buzzer and Display

NOTE: Do not forget to add `tm1637.py` to the Raspberry Pi Pico

Connect the following pins of Raspberry Pi Pico:

- LED: Pin 15
- Button: Pin 14
- Buzzer: Pin 27
- TM1637 Display: CLK=Pin 2, DIO=Pin 3

How to use it:
1. Press the Pin 14 button to start the timer.
2. The LED will turn on and the display will show the countdown.
3. Press the Pin 14 button again to pause the timer
4. The LED will blink slowly and the display will freeze.
5. Press the Pin 14 button again to resume the timer
6. LED will turn on and the display will continue the countdown.
7. Press the Pin 14 button for 1 second to reset the timer.
8. The LED and display will blink quickly to indicate the timer has finished.
9. The buzzer will sound a series of tones when the timer finishes.
10. Press the Pin 14 button to reset the timer and turn off the LED and display.
"""

from machine import Pin, Timer, PWM
import utime
import tm1637

# Pin setup
led = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(27))
buzzer.duty_u16(0)

# TM1637 display setup (CLK=2, DIO=3)
tm = tm1637.TM1637(clk=Pin(2), dio=Pin(3))
tm.brightness(1)
tm.write([0, 0, 0, 0])  # blank display at start

# Constants
DURATION = 6 * 60  # 6 minutes
LONG_PRESS_DURATION = 1  # seconds
DEBOUNCE_TIME = 200  # milliseconds

# State variables
state = "stopped"
start_time = 0
elapsed = 0
press_time = None
last_press_time = 0
ignore_next_release = False  # flag to ignore short press after long press

# Buzzer state
buzzer_on = False
buzzer_stage = 0
buzzer_next_time = 0
buzzer_duration = 0
buzzer_silence = 0
buzzer_freqs = []
buzzer_current_index = 0

# Blink timers
led_blink_timer = Timer()
display_blink_timer = Timer()
display_visible = True


def stop_blinking():
    led_blink_timer.deinit()
    display_blink_timer.deinit()
    led.value(0)


def blink_led(frequency):
    def toggle(timer):
        led.toggle()

    led_blink_timer.init(freq=frequency, mode=Timer.PERIODIC, callback=toggle)


def blink_display(frequency):
    def toggle(timer):
        global display_visible
        display_visible = not display_visible
        if display_visible:
            e = elapsed
            update_display(DURATION if e >= DURATION else DURATION - e)
        else:
            tm.write([0, 0, 0, 0])

    p = Timer.PERIODIC
    display_blink_timer.init(freq=frequency, mode=p, callback=toggle)


def update_display(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    tm.numbers(minutes, secs)


def clear_display():
    tm.write([0, 0, 0, 0])


def button_handler(pin):
    global state, start_time, elapsed, last_press_time, ignore_next_release

    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_press_time) < DEBOUNCE_TIME:
        return
    last_press_time = current_time

    if ignore_next_release:
        ignore_next_release = False
        return

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
        clear_display()
        print("Timer reset after finish")


button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)


def check_long_press():
    global state, press_time, elapsed, ignore_next_release

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
            clear_display()
            ignore_next_release = True  # prevent short press from triggering
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


# Main loop
last_display_update = 0
DISPLAY_REFRESH_MS = 1000

while True:
    check_long_press()

    freqs = [792, 745, 633, 444, 414, 664, 837, 1060]

    now = utime.ticks_ms()

    if state == "running":
        total_elapsed = elapsed + (utime.time() - start_time)
        remaining = max(0, DURATION - total_elapsed)
        if utime.ticks_diff(now, last_display_update) >= DISPLAY_REFRESH_MS:
            update_display(int(remaining))
            last_display_update = now
        if total_elapsed >= DURATION:
            state = "finished"
            blink_led(3)
            blink_display(3)
            activate_buzzer(duration=1, silence=1, freqs=freqs)
            print("Timer finished")

    elif state == "paused":
        remaining = max(0, DURATION - elapsed)
        update_display(int(remaining))

    elif state == "stopped":
        clear_display()

    if buzzer_on and utime.ticks_diff(now, buzzer_next_time) >= 0:
        if buzzer_stage == 1:
            buzzer.duty_u16(0)
            buzzer_stage = 2
            buzzer_next_time = utime.ticks_add(now, buzzer_silence)
        elif buzzer_stage == 2:
            buzzer_current_index += 1
            if buzzer_current_index < len(buzzer_freqs):
                buzzer.freq(buzzer_freqs[buzzer_current_index])
                buzzer.duty_u16(32768)
                buzzer_stage = 1
                buzzer_next_time = utime.ticks_add(now, buzzer_duration)
            else:
                buzzer.duty_u16(0)
                buzzer_on = False
                buzzer_stage = 0

    utime.sleep(0.085)
