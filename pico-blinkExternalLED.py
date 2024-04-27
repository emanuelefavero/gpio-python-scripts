import machine
from time import sleep

led =  machine.Pin(25, machine.Pin.OUT)
led_external = machine.Pin(15, machine.Pin.OUT)

while True:
    led_external.toggle()
    sleep(0.2)
    
    #led.value(0)
    #led_external.value(0)
