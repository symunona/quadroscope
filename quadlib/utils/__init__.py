import pygame
import os
import json

camera_settings_path = os.path.dirname(os.path.realpath(__file__)) + '/../../config/camerasettings.json'

def txt(surface,x,y, message, color = (255, 255, 255), fontsize = 28):
    message = str(message)
    fontobject=pygame.font.SysFont('Arial', fontsize)
    if len(message) != 0:
        surface.blit(fontobject.render(message, 1, color), (x, y))


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
    