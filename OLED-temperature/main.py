from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import utime

# OLED SETTINGS
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# PUT HERE THE SIZE OF YOUR SSD1306 OLED DISPLAY (128,32)
oled = SSD1306_I2C(128, 32, i2c)

# TEMPERATURE SENSOR SETTINGS
# Analog To Digital Converter
# TEMPERATURE SENSOR ON CHANNEL 4
sensor_temp = ADC(4)

# GET THE VOLTAGE VALUE INSTEAD OF 65535
convertion_factor = 3.3 / (65535)


def show_temps(position):
    reading = sensor_temp.read_u16() * convertion_factor
    # CONVERT VOLTAGE VALUES TO DEGREE CELCIUS
    # (EACH SENSOR HAS ITS OWN CONVERTION EQUATION)
    temperature = (27 - (reading - 0.706) / 0.001721)
    # ADD * 0.2 IF USED WITH LED SCREEN
    # position can be 0-20 int
    oled.fill(0)
    oled.text(str(round(temperature, 1)) + " C", 36, position)
    oled.show()
    utime.sleep(10)


while True:
    show_temps(0)
    show_temps(10)
    show_temps(20)
