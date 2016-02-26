from State import State
import CameraSettings
from SetProperty import SetProperty 
import pygame
import utils
from utils.Scroller import Scroller
from utils.Confirm import Confirm

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
            
            fontsize = 22
            color = (200,200,200)
            if (i == 3):
                color = (128, 128, 255)
                fontsize = 30
            utils.txt(surface, 60, 90 + (i*lineheight), txt, color, fontsize)
            utils.txt(surface, 450, 90 + (i*lineheight), value, (0,200,200), fontsize )
        
    def reset_to_default(self):
        print 'resetting'
        pass
        
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)                
        
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 2 :
                SetProperty(self.stack, self.camera, self.scroller.get_value()) 
            if event.button == 3 :
                Confirm(self.stack, 'Are you sure you want to reset to default?', self.reset_to_default) 
                
                    
