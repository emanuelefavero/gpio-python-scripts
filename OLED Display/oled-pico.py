from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# PUT HERE THE SIZE OF YOUR SSD1306 OLED DISPLAY (128,32)
oled = SSD1306_I2C(128, 32, i2c)

# FILL WITH BLACK (0), WHITE (1)
oled.fill(0)
# HERE YOU CAN PUT TEXT AND THE POSITION (0,0)
oled.text("Ciao Scemina", 0, 0)
oled.show()
