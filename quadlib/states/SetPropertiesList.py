from State import State
import CameraSettings
from SetProperty import SetProperty 
import pygame
import utils
from utils.Scroller import Scroller
from utils.Confirm import Confirm

lineheight = utils.screen['lineheight'] + 4
offsetx = utils.screen['margin']
offsety = 4 * utils.screen['margin'] + utils.screen['lineheight']
valueoffsetx = utils.screen['resolution'][0] - 120

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
            
            fontsize = utils.screen['fontsize']-4
            color = (200,200,200)
            if (i == 3):
                color = (128, 128, 255)
                fontsize = utils.screen['fontsize']
            utils.txt(surface, (offsetx, offsety + (i*lineheight)), txt, color)
            utils.txt(surface, (valueoffsetx, offsety + (i*lineheight)), value, (0,200,200), fontsize )
        
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
                Confirm(self.stack, 'Sure reset to default?', self.reset_to_default) 
                
                    
