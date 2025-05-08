"""
Pomodoro LED Timer with Break, Buzzer and Display

NOTE: Do not forget to add `tm1637.py` to the Raspberry Pi Pico

Connect the following pins of Raspberry Pi Pico:
- LED: Pin 15
- Button: Pin 14
- Break LED: Pin 16
- Break Button: Pin 17
- Buzzer: Pin 27
- TM1637 Display: CLK=Pin 2, DIO=Pin 3

How to use it:
1. Press the Pin 14 button to start the Pomodoro timer.
2. The LED will turn on and the display will show the countdown.
3. Press the Pin 14 button again to pause the timer
4. LED will blink slowly and the display will freeze.
5. Press the Pin 14 button again to resume the timer
6. LED will turn on and the display will continue the countdown.
7. Press the Pin 17 button to start the break timer.
8. The Break LED will turn on and the display will show the break countdown.
9. Press the Pin 17 button again to pause the break timer
10. Press the Pin 17 button again to resume the break timer
11. Press both buttons simultaneously to reset all timers
12. The LED and display will turn off
"""

from machine import Pin, Timer, PWM
import utime
import tm1637

# Pin setup
pomodoro_led = Pin(15, Pin.OUT)
pomodoro_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
break_led = Pin(16, Pin.OUT)
break_button = Pin(17, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(27))
buzzer.duty_u16(0)

# TM1637 setup
tm = tm1637.TM1637(clk=Pin(2), dio=Pin(3))
tm.brightness(1)
tm.write([0, 0, 0, 0])

# Constants
POMODORO_DURATION = 25 * 60  # 25 minutes
BREAK_DURATION = 5 * 60  # 5 minutes
DEBOUNCE_TIME = 200  # milliseconds
DUAL_PRESS_IGNORE_TIME = 500  # ms to ignore accidental presses after reset

# State
state = "stopped"
mode = "pomodoro"
start_time = 0
elapsed = 0

# Display
display_visible = True
display_timer = Timer()
last_display_update = 0
DISPLAY_REFRESH_MS = 1000

# Blinking
blink_timer = Timer()

# Buzzer
buzzer_on = False
buzzer_stage = 0
buzzer_next_time = 0
buzzer_duration = 0
buzzer_silence = 0
buzzer_freqs = []
buzzer_current_index = 0

# Debounce tracking
last_pomodoro_press = 0
last_break_press = 0
last_reset_time = 0


def stop_blinking():
    blink_timer.deinit()
    display_timer.deinit()
    pomodoro_led.value(0)
    break_led.value(0)


def blink_led_and_display(frequency):
    def toggle(timer):
        global display_visible
        display_visible = not display_visible
        if display_visible:
            remaining = POMODORO_DURATION if mode == "pomodoro" else BREAK_DURATION
            update_display(remaining - elapsed)
        else:
            clear_display()

        if mode == "pomodoro":
            pomodoro_led.toggle()
        else:
            break_led.toggle()

    blink_timer.init(freq=frequency, mode=Timer.PERIODIC, callback=toggle)


def clear_display():
    tm.write([0, 0, 0, 0])


def update_display(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    tm.numbers(minutes, secs)


def reset_all():
    global state, start_time, elapsed, display_visible, last_reset_time
    state = "stopped"
    elapsed = 0
    stop_blinking()
    display_visible = False
    clear_display()
    last_reset_time = utime.ticks_ms()
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
    elapsed += utime.time() - start_time
    state = "paused"
    blink_led_and_display(2)
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
    blink_led_and_display(2)
    print("Pomodoro finished" if mode == "pomodoro" else "Break finished")
    freqs = [792, 745, 633, 444, 414, 664, 837, 1060]
    activate_buzzer(duration=1, silence=1, freqs=freqs)


def handle_button(button_mode):
    global state, mode
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_reset_time) < DUAL_PRESS_IGNORE_TIME:
        return  # Ignore accidental presses after reset
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


def pomodoro_button_handler(pin):
    global last_pomodoro_press
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_pomodoro_press) >= DEBOUNCE_TIME:
        last_pomodoro_press = now
        handle_button("pomodoro")


def break_button_handler(pin):
    global last_break_press
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_break_press) >= DEBOUNCE_TIME:
        last_break_press = now
        handle_button("break")


def check_for_dual_button_press():
    if pomodoro_button.value() and break_button.value():
        reset_all()
        print("Both buttons pressed: Full reset")
        utime.sleep_ms(DUAL_PRESS_IGNORE_TIME)


def activate_buzzer(duration=1, silence=1, freqs=[620, 720]):
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


pomodoro_button.irq(trigger=Pin.IRQ_RISING, handler=pomodoro_button_handler)
break_button.irq(trigger=Pin.IRQ_RISING, handler=break_button_handler)

# Main loop
while True:
    check_for_dual_button_press()
    now = utime.ticks_ms()

    if state == "running":
        duration = POMODORO_DURATION if mode == "pomodoro" else BREAK_DURATION
        total_elapsed = elapsed + (utime.time() - start_time)
        remaining = max(0, duration - total_elapsed)
        if utime.ticks_diff(now, last_display_update) >= DISPLAY_REFRESH_MS:
            update_display(int(remaining))
            last_display_update = now
        if total_elapsed >= duration:
            finish_timer()

    elif state == "paused":
        duration = POMODORO_DURATION if mode == "pomodoro" else BREAK_DURATION
        update_display(int(duration - elapsed))

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
