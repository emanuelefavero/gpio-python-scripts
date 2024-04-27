import machine
from time import sleep

led = machine.Pin(25, machine.Pin.OUT)

while True:
    led.toggle()
    sleep(0.2)
