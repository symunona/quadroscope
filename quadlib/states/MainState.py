import pygame
from SetPropertiesList import SetPropertiesList
from State import State
from Player import Player

from .. import utils
from ..utils.Scroller import Scroller
from .. import camera_loop

class MainState(State):
    
    def on_mode_change(self, new_mode, old_mode):
        
        alpha = 64       
        if (new_mode == 'clean'): alpha = 0            
        # if (new_mode == 'player'): alpha = 255
        
        pygame_event = pygame.event.Event(utils.CHANGE_DISPLAY_SETTINGS, 
                {'command': 'alpha', 'value': alpha})
        pygame.event.post(pygame_event)     

    
    def __init__(self, stack, updater, camera):
        State.__init__(self, stack)
        self.updater = updater
        self.camera = camera
        self.title  = 'main'
        self.modes  = 'clean overview setproperty guide player'.split(' ')
        self.scroller = Scroller(self.modes, 0, self.on_mode_change)
        self.overview = False        
        
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)        
        self.title = self.scroller.get_value()
        if (self.title == 'clean'): self.title = ''
        
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 2 : 
                if self.scroller.get_value() == 'setproperty':
                    SetPropertiesList(self.stack, self.camera)
                if self.scroller.get_value() == 'player':
                    Player(self.stack)
            
            if event.button == 1 :
                self.scroller.set_value('overview')                 
            
            # see main parameters
            if event.button == 3 : 
                self.camera.make_photos()
                
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 :                 
                self.scroller.set_value('clean')                                
                    
        
    def draw(self, surface):
    
        if self.scroller.get_value() == 'overview':
            pygame.draw.rect(surface, (0,0,255), (10,10,30,30))

        if self.scroller.get_value() == 'guide':        
            pygame.draw.rect(surface, (96,96,96), (
                    utils.screen['resolution'][0]/3,
                    utils.screen['resolution'][1]/3,
                    utils.screen['resolution'][0]/3,
                    utils.screen['resolution'][1]/3))
        else:
            State.draw(self, surface)
        