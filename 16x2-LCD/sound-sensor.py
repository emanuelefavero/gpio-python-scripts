from LQ_i2c import I2cLcd
from machine import Pin, I2C
from time import sleep


vu = Pin(15, Pin.OUT)
di = Pin(16, Pin.IN)
i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=100000)
lcd = I2cLcd(i2c, 0x3F, 2, 16)  # LCD 16x2
lcd.clear()
lcd.move_to(2, 0)
lcd.putstr("Sound Sensor")

while True:
    try:
        if di.value():
            vu.value(True)
        else:
            vu.value(False)
    except KeyboardInterrupt:
        break

