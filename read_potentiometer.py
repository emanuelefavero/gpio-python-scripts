import machine
import utime

# ADC, Analog To Digital
potentiometer = machine.ADC(26)

convertion_factor = 3.3 / (65535)

# u16 means that instead of reading 1 and 0, it will read 16bit values
# to read digital input use .read()
while True:
    # READ ACCURATE VOLTAGE VALUES INSTEAD OF 0-65535
    voltage = round(potentiometer.read_u16() * convertion_factor, 2)
    print(voltage)
    # READ 0-100 VALUES INSTEAD OF 0-65535, (10k POTENTIOMETER)
    zero_100 = int((potentiometer.read_u16() / 1000) * 1.53)
    print(zero_100)
    utime.sleep(2)
