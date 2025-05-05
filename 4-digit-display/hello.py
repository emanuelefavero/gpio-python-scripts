"""
4-Digit Display Example

- Make sure to add the TM1637 library to the Raspberry Pi Pico (tm1637.py file)
- Connect the following pins of Raspberry Pi Pico:
    - CLK: Pin 2
    - DIO: Pin 3
- Also VCC and GND pins to the power supply
"""

import tm1637
from machine import Pin
import time

tm = tm1637.TM1637(clk=Pin(2), dio=Pin(3))

tm.brightness(1)  # Brightness: 0 (dim) to 7 (bright)
# tm.write([0, 0, 0, 0]) # all off
# tm.show("1234")  # Show numbers
# tm.number(1234)  # Alternative way to show a number
# tm.show("TAGO ")  # Show text
# tm.write([127, 255, 127, 127]) # 88:88
# tm.write([63, 6, 91, 79]) # 0123
# tm.write([0b00111001, 0b00111111, 0b00111111, 0b00111000]) # COOL
# tm.numbers(21, 15) # 18:59
# tm.number(-123) # -123
# tm.temperature(24) # 24*C
# tm.scroll("Hello ")  # Scroll text

while True:
    tm.scroll("Hello ")
    time.sleep(0.1)
