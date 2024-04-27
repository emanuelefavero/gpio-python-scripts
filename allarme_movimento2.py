import machine
import utime

sensor_pir = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)
# sensor_pir2 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)
led = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.Pin(14, machine.Pin.OUT)

led.value(0)
buzzer.value(0)


def pir_handler(pin):
    utime.sleep_ms(100)
    if pin.value():
        print("ALARM! Motion Detected!")
        for i in range(50):
            led.toggle()
            buzzer.toggle()
            utime.sleep_ms(100)


sensor_pir.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_handler)
# sensor_pir2.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_handler)

while True:
    led.value(1)
    utime.sleep(0.01)
    led.value(0)
    utime.sleep(2.99)
