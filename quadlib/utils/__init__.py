import pygame
import os, json
import traceback

from ..updater import Updater 

CHANGE_DISPLAY_SETTINGS = pygame.USEREVENT + 2

rootpath = os.path.dirname(os.path.realpath(__file__)) + '/../../'

camera_settings_path = rootpath + 'config/camerasettings.json'
settings = json.load(open(rootpath + 'config/settings.json'))

def get_file_name_for_id(id, no = None):
    global settings
    if no == None:
        return settings['uploadpath'] +'img-'+ '%04d' % id +'.jpg'
    else: 
        return settings['uploadpath'] +'img-'+ '%04d' % id +'-'+ str(no) +'.jpg'


screen = {
    'resolution': (320, 240),
    'striperesolution': (320, 48),
    'fontsize': 18,
    'lineheight': 24,
    'margin': 2    
}

fontobject = None
largefontobject = None


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


def change_to_full_screen():
    pygame_event = pygame.event.Event(utils.CHANGE_DISPLAY_SETTINGS, 
                {'command': 'readd', 'screenSize': screen['resolution']})
    pygame.event.post(pygame_event)         
    
def change_to_stripe():
    pygame_event = pygame.event.Event(utils.CHANGE_DISPLAY_SETTINGS, 
                {'command': 'readd', 'screenSize': screen['striperesolution']})
    pygame.event.post(pygame_event)         

def txt(surface, pos, message, color = (255, 255, 255), underline = False):
    global fontobject
    
    message = str(message)        
    if fontobject == None:
        fontobject = pygame.font.SysFont('Arial', screen['fontsize'])
    
    fontobject.set_underline(underline)
    
    if len(message) > 0:
        try:
            surface.blit(fontobject.render(message, 1, color), (pos[0], pos[1]))
        except Exception, e: 
            print '[error] "%s"'% message, e

def txt_large(surface, pos, message, color = (255, 255, 255), underline = False):
    global largefontobject
    message = str(message)    

    if utils.largefontobject == None:
        utils.largefontobject = pygame.font.SysFont('Arial', screen['fontsize']+2*screen['margin'])

    utils.largefontobject.set_underline(underline)

    if len(message) > 0:
        surface.blit(utils.largefontobject.render(message, 1, color), (pos[0], pos[1]))


def load_camera_settings():
    with open(camera_settings_path) as settingsfile:
	   return  json.load(settingsfile)
       
def save_camera_settings(cameraSettings):    
    with open(camera_settings_path, 'w') as outfile:
        json.dump(cameraSettings, outfile)
        
    if Updater.instance != None:
        Updater.instance.sync_camera_settings()
    

def find(array, key, value):
    for o in array:
        if (o[key] == value): return o
    return None
    
    
def limit(min, max, value):
    if (value < min):
        return min
    else: 
        if (value > max):
            return max
    return value
    
    
    
def trace():
    for line in traceback.format_stack():
        print(line.strip())
    