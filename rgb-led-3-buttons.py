import machine
import utime

led_red = machine.Pin(2, machine.Pin.OUT)
led_green = machine.Pin(3, machine.Pin.OUT)
led_blue = machine.Pin(4, machine.Pin.OUT)

button_red = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_green = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_blue = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN)

while True:
    
    if button_red.value() == 1:
        led_red.toggle()
        utime.sleep(0.2)
    
    if button_green.value() == 1:
        led_green.toggle()
        utime.sleep(0.2)
    
    if button_blue.value() == 1:
        led_blue.toggle()
        utime.sleep(0.2)

