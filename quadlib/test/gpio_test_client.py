import RPi.GPIO as GPIO
import time

CAMLED = 32
port_output = 14

GPIO.setmode(GPIO.BCM)   
GPIO.setup(CAMLED, GPIO.OUT, initial=True)
time.sleep(0.5)
GPIO.output(CAMLED,False)

GPIO.setup( port_output , GPIO.IN )

while True:
    print 'waiting'
    GPIO.wait_for_edge(port_output, GPIO.RISING)                     # ____/
    print 'hit'
    GPIO.output(CAMLED,True)

    GPIO.wait_for_edge(port_output, GPIO.FALLING)                     #     \____
    print 'fall'
    GPIO.output(CAMLED,False)