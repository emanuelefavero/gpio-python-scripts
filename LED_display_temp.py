from pico_i2c_lcd import I2cLcd
import machine
import utime


i2c = machine.I2C(id=1, scl=machine.Pin(27), sda=machine.Pin(26), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # LCD 16x2

# Analog To Digital Converter
# TEMPERATURE SENSOR ON CHANNEL 4
sensor_temp = machine.ADC(4)

# GET THE VOLTAGE VALUE INSTEAD OF 65535
convertion_factor = 3.3 / (65535)

while True:
    # lcd.move_to(0, 0)

    reading = sensor_temp.read_u16() * convertion_factor
    # CONVERT VOLTAGE VALUES TO DEGREE CELCIUS
    # (EACH SENSOR HAS ITS OWN CONVERTION EQUATION)
    temperature = (27 - (reading - 0.706) / 0.001721) * (-0.2)
    # ADD * 0.2 IF USED WITH LED SCREEN
    lcd.putstr(str(round(temperature, 1)) + ' C')
    print(temperature)
    utime.sleep(10)

    lcd.clear()
    # lcd.display_on()
