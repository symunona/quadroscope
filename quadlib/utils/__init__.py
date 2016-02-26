import pygame
import os
import json
import utils

CHANGE_DISPLAY_SETTINGS = pygame.USEREVENT + 2

camera_settings_path = os.path.dirname(os.path.realpath(__file__)) + '/../../config/camerasettings.json'

screen = {
    'resolution': (320, 240),
    'striperesolution': (320, 48),
    'fontsize': 20,
    'lineheight': 24,
    'margin': 2    
}

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

def txt(surface, pos, message, color = (255, 255, 255), fontsize = screen['fontsize']):
    message = str(message)
    fontobject=pygame.font.SysFont('Arial', fontsize)
    if len(message) > 0:
        surface.blit(fontobject.render(message, 1, color), (pos[0], pos[1]))


def load_camera_settings():
    with open(camera_settings_path) as settingsfile:
	   return  json.load(settingsfile)
       
def save_camera_settings(cameraSettings):
    with open(camera_settings_path, 'w') as outfile:
        json.dump(cameraSettings, outfile)

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
    