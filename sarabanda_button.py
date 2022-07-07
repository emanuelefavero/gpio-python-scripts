import machine
import utime

led_red = machine.Pin(15, machine.Pin.OUT)

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(13, machine.Pin.OUT)

button.value(0)
led_red.value(0)
buzzer.value(0)

while True:
    if button.value() == 1:
        led_red.value(1)
        buzzer.value(1)
        utime.sleep(0.5)
    elif button.value() == 0:
        led_red.value(0)
        buzzer.value(0)
        utime.sleep(0.2)
    utime.sleep(0.02)
