# Display Image & text on I2C driven ssd1306 OLED display 
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import machine
import utime
 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
 
WIDTH  = 128                                            # oled display width
HEIGHT = 32                                           # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
# print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
# print("I2C Configuration: "+str(i2c))                   # Display I2C config
 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
 
while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    #print(temperature)
 
    # Clear the oled display in case it has junk on it.
    oled.fill(0)       
    
    # Add some text
    # oled.text("Temp: ",6,8)
    oled.text(f"{str(round(temperature,1))} C",40,15)
    # oled.text("C",80,15)
    utime.sleep(2)
 
 
    # Finally update the oled display so the image & text is displayed
    oled.show()