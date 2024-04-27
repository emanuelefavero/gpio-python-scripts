from gpiozero import RGBLED
from time import sleep

# MY FIRST RGB LED IS ANODE
led = RGBLED(17,27,22, active_high=False)

while True:
        led.color = (1,0,0)
        sleep(1)
        led.off()
        led.color = (0.2,0,0.2)
        sleep(1)
        led.off()
        led.color = (0,0,1)
        sleep(1)
        led.off()
        led.color = (1,0,1)
        sleep(1)
        led.off()
        led.color = (1,1,0)
        sleep(1)
        led.off()
        led.color = (1,1,1)
        sleep(1)
        led.off()
