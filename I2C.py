from pico_i2c_lcd import I2cLcd
import machine
import utime


i2c = machine.I2C(id=1, scl=machine.Pin(27), sda=machine.Pin(26), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # LCD 16x2


while True:
    # lcd.move_to(0, 0)
    lcd.putstr('ciao')
    utime.sleep(1)
    lcd.clear()
    lcd.putstr('scemina')
    utime.sleep(1)
    lcd.clear()
    # lcd.display_on()
