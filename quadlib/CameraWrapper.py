import CameraSettings
import utils

class CameraWrapper:
    
    def __init__(self, camera):        
        self.camera = camera
        self.actual_camera_settings = utils.load_camera_settings()
        
    
    def property_live(self, key):
        return not 'live' in utils.find(CameraSettings.camera_settings, 'key', key).keys()
    
    def get_property(self, key):
        return utils.find(CameraSettings.camera_settings, 'key', key)
        
    def get_property_value(self, key):
        property = self.get_property(key)        
        
        # if the property is comming from the camera, or not
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
        
    
    def set_property(self, key, value):    

        # update settings in preview        
        if self.property_live(key):
            setattr(self.camera, key, value)
            
        self.actual_camera_settings[key] = value
            
    def save_settings(self):
        utils.save_camera_settings(self.actual_camera_settings)