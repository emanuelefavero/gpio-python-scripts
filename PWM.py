# DIM LED USING PWM (FAKING AN ANALOG SIGNAL)
# WE WILL STILL USE A POTENTIOMETER BUT THE LED WILL BE DIMMED DIGITALLY

import machine
import utime

# ADC, Analog To Digital
potentiometer = machine.ADC(26)
# PWM
led = machine.PWM(machine.Pin(15))
led.freq(1000)  # 1kHz, use 10Hz to see the effect

# u16 means that instead of reading 1 and 0, it will read 16bit values
# to read digital input use .read()

while True:
    led.duty_u16(potentiometer.read_u16())
    utime.sleep(0.01)
