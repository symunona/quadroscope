import datetime, thread, time
from . import utils
from . import CameraSettings
from .utils import gpio


class CameraWrapper:
    
    def __init__(self, camera, updater, gpio, boss, camerano):        
        self.camera = camera
        self.actual_camera_settings = utils.load_camera_settings()
        self.property_map = []
        self.boss = boss
        self.camerano = camerano
        self.gpio = gpio
        for p in CameraSettings.camera_settings:
            self.property_map.insert(0,p['key']) 
        self.apply_camera_settings()
        self.updater = updater
        if updater != None:
            self.fileid = self.updater.get_next_file_id()        
            self.filename = utils.get_file_name_for_id(self.fileid, self.camerano)
    
    def reload_camera_settings(self):
        self.actual_camera_settings = utils.load_camera_settings()
    
    def property_live(self, key):
        return not 'live' in utils.find(CameraSettings.camera_settings, 'key', key).keys()
    
    def get_property(self, key):
        return utils.find(CameraSettings.camera_settings, 'key', key)
        
    def get_property_value(self, key):        
        property = self.get_property(key)        
        
        # if the property is comming from the camera, or not
        if property == None:            
            return '[warn] no such key ', key 
        if 'live' in property.keys():
            
            # if it is set in the JSON, retriev it, else return with default
            actual_value = None
            if key in self.actual_camera_settings.keys():
                # print 'in', key, self.actual_camera_settings.keys()
                return self.actual_camera_settings[key]
            else:
                # print 'not in' , key, self.actual_camera_settings.keys()
                return property['default']
        try:
            actual_value = getattr(self.camera, key)
            return actual_value 
        except: 
            return '[error]'

    def reset_camera_settings(self):
        for p in CameraSettings.camera_settings:
            self.set_property(p['key'],p['default'])
        
        self.save_settings()
        
    def apply_camera_settings(self):
        for key in self.actual_camera_settings.keys():    
            if key in self.property_map:        
                self.set_property(key,self.actual_camera_settings[key])
    
    def set_property(self, key, value):    
        
        if key not in self.property_map:
            print '[warn] ', key, ' is not in property map'         
            return
        
        # update settings in preview        
        if self.property_live(key):
            setattr(self.camera, key, value)
            
        self.actual_camera_settings[key] = value
            
    def save_settings(self):
        utils.save_camera_settings(self.actual_camera_settings)
        
    def take_picture(self, filename):
        
        self.apply_camera_settings()
        res = self.actual_camera_settings['resolution'].split('x')
        self.camera.resolution = (int(res[0]), int(res[1])) 
        self.camera.capture(filename)
        self.camera.resolution = utils.screen['captureresolution']        
        self.camled_blink()
                
    def generate_file_id(self):
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
    def camled_blink(self):
        def blinker(): time.sleep(0.1); self.gpio.camled(False)  
        self.gpio.camled(True)
        thread.start_new_thread(blinker, ())        
        
    def make_photos(self):

        self.fileid = self.updater.get_next_file_id()        
        self.filename = utils.get_file_name_for_id(self.fileid, self.camerano)

        if self.boss and self.updater != None:
            self.gpio.trigger_employees(True)
                        
        self.take_picture(self.filename)
        
        if self.updater != None:

            if self.boss:         
                self.gpio.trigger_employees(False)
                thread.start_new_thread(self.updater.wait_for_files_from_clients, (self.fileid, self.actual_camera_settings))

        self.updater.step_file_id()