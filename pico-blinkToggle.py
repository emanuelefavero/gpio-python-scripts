from machine import Pin, Timer

led = Pin(25, Pin.OUT)
time = Timer()
def tick(timer):
    global led
    led.toggle()

time.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

