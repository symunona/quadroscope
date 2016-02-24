from State import State
import pygame
import utils
from Scroller import Scroller

lineheight = 40
offsety = 340

class SetProperty(State):
    def __init__(self, stack, camera, propertykey):
        State.__init__(self, stack)
        self.camera = camera
        self.title  =  self.propertykey = propertykey
        self.property = camera.get_property( propertykey )
        self.actual_camera_settings = utils.load_camera_settings()
        self.original_value = camera.get_property_value( propertykey ) 
                        
        if self.property['type'] == 'select':
            self.scroller = Scroller(self.property['values'])

    def draw(self, surface):
        if self.property['type'] == 'numeric':
            utils.txt(surface, 50, offsety, self.property['min'])    
            utils.txt(surface, 490, offsety, self.property['max'])    
        
        utils.txt(surface, 270, offsety, self.camera.get_property_value(self.propertykey))
    
    def event(self, event):
        
        if self.property['type'] == 'select':
            self.scroller.event(event)
            self.camera.set_property(self.propertykey, self.scroller.get_value())                
            
        # self.camera.set_property(self.propertykey, )
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.property['type'] == 'numeric':
                delta = 0
                if event.button == 4:
                    delta = self.property['step'];
                else: 
                    if event.button == 5:
                        delta = -self.property['step'];
                        
                if (delta != 0):
                    current_value = self.camera.get_property_value(self.propertykey)
                    current_value += delta
                    current_value = utils.limit(self.property['min'], self.property['max'], current_value)                                          
                    self.camera.set_property(self.propertykey, current_value) 
            # ok
            if event.button == 2 :
                self.camera.save_settings()
                self.back()
                return 
                
            # cancel
            if event.button == 1 :
                self.camera.set_property(self.propertykey, self.original_value)
                self.back()
                return

            # reset to default
            if event.button == 3 :
                if ('default' in self.property.keys()):
                    self.camera.set_property(self.propertykey, self.property.default)
                else:
                    self.camera.set_property(self.propertykey, self.original_value)
            
        State.event(self, event)
                