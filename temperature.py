import machine
import utime

# Analog To Digital Converter
# TEMPERATURE SENSOR ON CHANNEL 4
sensor_temp = machine.ADC(4)

# GET THE VOLTAGE VALUE INSTEAD OF 65535
convertion_factor = 3.3 / (65535)

# READ VALUES
while True:
    reading = sensor_temp.read_u16() * convertion_factor
    # CONVERT VOLTAGE VALUES TO DEGREE CELCIUS
    # (EACH SENSOR HAS ITS OWN CONVERTION EQUATION)
    temperature = (27 - (reading - 0.706) / 0.001721)
    # ADD * 0.2 IF USED WITH LED SCREEN
    print(temperature)
    utime.sleep(2)
