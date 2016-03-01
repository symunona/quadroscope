import RPi.GPIO as GPIO
import time

def blink(n, port, wait = 0.1):
    for i in range(n):
        GPIO.output(port,True) # On
        print '%d 1' % port
        time.sleep(wait)
        GPIO.output(port,False) # Off
        print '%d 0' % port        
        time.sleep(0.5)
    
    # GPIO.output(port,True)
    # time.sleep(wait * 3)
    # GPIO.output(port,False)


CAMLED = 32
port_output = 14

GPIO.setmode(GPIO.BCM)   
GPIO.setup(CAMLED, GPIO.OUT, initial=False)
# GPIO.setup( port_output, GPIO.IN ) #, pull_up_down = GPIO.PUD_UP
GPIO.setup( port_output , GPIO.OUT, initial=False)

blink( 2, CAMLED)
print 'desmond the moonbear'
blink( 5, port_output)
print 'the end'
blink( 2, CAMLED)

