import RPi.GPIO as GPIO
import time

CAMLED = 32

class GPIO:
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
        
        
    def trigger_employees(self,  val ):

        GPIO.setup( employee_trigger_port , GPIO.IN )


    def wait_for_trigger(self):
        if self.boss:
            port = self.boss_trigger_port
        else: 
            port = self.employee_trigger_port
            
        GPIO.wait_for_edge(port, GPIO.RISING)
        
    def wait_for_release(self):
        if self.boss:
            port = self.boss_trigger_port
        else: 
            port = self.employee_trigger_port
            
        GPIO.wait_for_edge(port, GPIO.FALLING)
        
        
    def init_boss(self):
        
        GPIO.setup(self.boss_trigger_port, GPIO.IN, pull_up_down = GPIO.PUD_UPP)
        GPIO.setup( self.employee_trigger_port , GPIO.OUT )		
	    GPIO.output( self.employee_trigger_port, False )
         
        
        	# for i in employees:
	# 	GPIO.setup( employees[i]['gpio'] , GPIO.OUT )
	#         GPIO.output( triggerport, False )		
