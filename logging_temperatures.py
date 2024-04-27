# LOGGING TEMPERATURES TO A TEXT FILE
import machine
import utime

sensor_temp = machine.ADC(4)

convertion_factor = 3.3 / (65535)
# reading = sensor_temp.read_u16() * convertion_factor
# temperature = (27 - (reading - 0.706) / 0.001721)

file = open("temps.txt", "w")

while True:
    reading = sensor_temp.read_u16() * convertion_factor
    temperature = (27 - (reading - 0.706) / 0.001721)
    file.write(str(temperature) + "\n")
    file.flush()  # USE THIS INSTEAD OF file.close()
    utime.sleep(10)  # LOGS TEMPERATURES EACH 10 SECONDS

# TO READ FILE:
# USE file = open("filename.txt", "r"), file.read()

# TO READ THE FILE:
# file = open("temps.txt", "r")
# print(file.read())
# file.close()
