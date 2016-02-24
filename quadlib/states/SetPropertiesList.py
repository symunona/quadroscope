from State import State
import CameraSettings
from SetProperty import SetProperty 
import pygame
import utils
from Scroller import Scroller

lineheight = 40

class SetPropertiesList(State):
    def __init__(self, stack, camera):
        State.__init__(self, stack)
        self.camera = camera
        self.title  = 'setproperties'
        
        self.settings_menu = []     
        for setting in CameraSettings.camera_settings:            
            menuitem = setting['key']        
            self.settings_menu.append(menuitem)
            
        self.scroller = Scroller(self.settings_menu)
        
    def draw(self, surface):
        State.draw(self, surface)
        for i in range (7):
            txt = self.scroller.get_value( self.scroller.get_index() - 3 + i )
            value = self.camera.get_property_value(txt)
            
            color = (200,200,200)
            if (i == 3):
                color = (128, 128, 255)
            utils.txt(surface, 60, 90 + (i*lineheight), txt, color )
            utils.txt(surface, 450, 90 + (i*lineheight), value, (0,200,200), )
        
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)                
        
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 2 :
                SetProperty(self.stack, self.camera, self.scroller.get_value()) 
                
                    
