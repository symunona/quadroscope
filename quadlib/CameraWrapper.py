import CameraSettings
import utils

class CameraWrapper:
    
    def __init__(self, camera):        
        self.camera = camera
        self.actual_camera_settings = utils.load_camera_settings()
        self.property_map = []
        for p in CameraSettings.camera_settings:
            self.property_map.insert(0,p['key']) 
        self.apply_camera_settings()
    
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