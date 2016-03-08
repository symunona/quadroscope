import pygame
from .. import utils
import RPi.GPIO as GPIO

screen = utils.screen
boss_trigger_port = 0

CHANGE_DISPLAY_SETTINGS = pygame.USEREVENT + 2
TAKE_PICTURE = pygame.USEREVENT + 3

def take_picture_event():
    pygame_event = pygame.event.Event(TAKE_PICTURE)
    pygame.event.post(pygame_event)         

def change_to_full_screen():
    pygame_event = pygame.event.Event(CHANGE_DISPLAY_SETTINGS, 
                {'command': 'readd', 'screenSize': screen['resolution']})
    pygame.event.post(pygame_event)         
    
def change_to_stripe():
    pygame_event = pygame.event.Event(CHANGE_DISPLAY_SETTINGS, 
                {'command': 'readd', 'screenSize': screen['striperesolution']})
    pygame.event.post(pygame_event)         


fontobject = None
largefontobject = None


background = (128,128,128, 0.5)

class Calc:
    @staticmethod
    def right(x):
        return screen['resolution'][0] - x
    
    @staticmethod
    def centerX(width):
        return (screen['resolution'][0]/2) - (width/2)

    @staticmethod
    def centerY(height):
        return (screen['resolution'][1]/2) - (height/2)


def txt(surface, pos, message, color = (255, 255, 255), underline = False):
    global fontobject
    
    message = str(message)        
    if fontobject == None:
        fontobject = pygame.font.SysFont('Arial', screen['fontsize'])
    
    fontobject.set_underline(underline)
    
    if len(message) > 0:
        try:
            surface.blit(fontobject.render(message, 1, color, background), (pos[0], pos[1]))
            #rendered = 
            # rendered.set_alpha(128)
            # surface.blit(rendered, (0, 0))
        except Exception, e: 
            print '[error] "%s"'% message, e

def txt_large(surface, pos, message, color = (255, 255, 255), underline = False):
    global largefontobject
    message = str(message)    

    if largefontobject == None:
        largefontobject = pygame.font.SysFont('Arial', screen['fontsize']+2*screen['margin'])

    largefontobject.set_underline(underline)

    if len(message) > 0:
        surface.blit(largefontobject.render(message, 1, color), (pos[0], pos[1]))

def splash(surface):
    #utils.splash(screen)
    
    pass


def init_boss_trigger():
    global boss_trigger_port
    boss_trigger_port = utils.settings['gpioBossTriggerPort']
    high = utils.settings['gpioHigh']
    
    GPIO.setup( boss_trigger_port , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # because my setup's display does not have a 3.3V out 
    # I use a pin to give high value
    GPIO.setup( high , GPIO.OUT, initial = GPIO.HIGH)

def wait_for_boss_trigger():
    global boss_trigger_port    
    GPIO.wait_for_edge(boss_trigger_port, GPIO.RISING)
    print '[watchloop] TRIGGERED ', str(boss_trigger_port)

def wait_for_boss_release():
    global boss_trigger_port
    GPIO.wait_for_edge(boss_trigger_port, GPIO.FALLING)

def watch_trigger():
    init_boss_trigger()
    while True:
        wait_for_boss_trigger()
        take_picture_event()
        wait_for_boss_release()
        
        
        

