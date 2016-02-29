import RPi.GPIO as GPIO
import time

CAMLED = 32

class Gpio:
    def __init__(self, settings, boss):
        self.settings = settings
        self.boss = boss
        self.boss_trigger_port = settings['gpioBossTriggerPort']
        self.employee_trigger_port = settings['gpioEmployeeTriggerPort']
        
        GPIO.setmode(GPIO.BCM)        
        self.initCameraLED()
        
        if boss: 
            self.init_boss()
            self.port = self.boss_trigger_port
        else:
            self.port = self.init_employee()
            self.port = self.employee_trigger_port()

    def initCameraLED(self):
        GPIO.setup(CAMLED, GPIO.OUT, initial=False) 

    def camled(self, val):
        GPIO.output(CAMLED, val)

    def blinkCamera(self, n, wait = 0.3):
        for i in range(n):
            GPIO.output(CAMLED,True) # On
            time.sleep(wait)
            GPIO.output(CAMLED,False) # Off
            time.sleep(0.5)
        
        GPIO.output(CAMLED,True)
        time.sleep(wait * 3)
        GPIO.output(CAMLED,False)
        
    def init_employee(self):    
        GPIO.setup( employee_trigger_port , GPIO.IN )
        
    def trigger_employees(self,  val ):
        GPIO.output( self.employee_trigger_port, val )


    def wait_for_trigger(self):
        if self.boss:
            port = self.boss_trigger_port
        else: 
            port = self.employee_trigger_port
        print '[main_loop] waiting for trigger on ', str(port)
        GPIO.wait_for_edge(port, GPIO.RISING)
        print '[main_loop] TRIGGERED ', str(port)
        
    def wait_for_release(self):
        if self.boss:
            port = self.boss_trigger_port
        else: 
            port = self.employee_trigger_port
            
        GPIO.wait_for_edge(port, GPIO.FALLING)
        
        
    def init_boss(self):
    
        GPIO.setup( self.boss_trigger_port, GPIO.IN, pull_up_down = GPIO.PUD_UP )
        GPIO.setup( self.employee_trigger_port , GPIO.OUT )
        GPIO.output( self.employee_trigger_port, False )
        
        