import machine
import utime

sensor_pir = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)
led = machine.Pin(15, machine.Pin.OUT)


# def pir_handler(pin):
#     utime.sleep_ms(100)
#     if pin.value():
#         print("ALARM! Motion Detected!")


# sensor_pir.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_handler)

while True:
    utime.sleep_ms(100)
    led.value(0)
    if sensor_pir.value() == 1:
        print("ALARM! Motion Detected!")
        led.value(1)
        utime.sleep(10)
