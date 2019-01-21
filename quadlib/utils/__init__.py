
import os, json
import traceback
from datetime import datetime

from ..updater import Updater 


rootpath = os.path.dirname(os.path.realpath(__file__)) + '/../../'

camerano = open(rootpath + 'percamconfig/camerano', 'r').read().strip('\n')


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
    'margin': 2,
    'captureresolution': (320, 240)    
}


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
    


def log( *args ):
    global camerano    
    timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]    
    print '['+ camerano+ '][' + timestamp + '] ' + (' '.join(map(str, args)))
    