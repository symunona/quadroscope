from State import State
import CameraSettings
from SetProperty import SetProperty 
import pygame
import utils
from utils.Scroller import Scroller

lineheight = 40

class Player(State):
    def __init__(self, stack, camera):
        State.__init__(self, stack)        
        self.title  = 'player'
        
        self.settings_menu = []     
        for setting in CameraSettings.camera_settings:            
            menuitem = setting['key']        
            self.settings_menu.append(menuitem)
            
        self.scroller = Scroller(self.settings_menu)
        
    def draw(self, surface):
        State.draw(self, surface)
            
        
    def reset_to_default():
        print 'resetting'
        pass
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)                
        
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 2 :
                SetProperty(self.stack, self.camera, self.scroller.get_value()) 
            if event.button == 3 :
                Confirm(self.stack, 'Are you sure you want to reset to default?', reset) 
                
                    
