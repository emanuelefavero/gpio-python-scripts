import machine
from time import sleep

led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_external = machine.Pin(15, machine.Pin.OUT)

while True:
    led.value(1)
    if button.value() == 1:
        led_external.value(1)
        sleep(0.4)
        led_external.value(0)
        sleep(0.2)
    led_external.value(0)
