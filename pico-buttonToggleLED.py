import machine
from time import sleep

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_external = machine.Pin(15, machine.Pin.OUT)

while True:
    if button.value() == 1:
        #print("Button pressed!")
        led_external.toggle()
        sleep(0.2)
