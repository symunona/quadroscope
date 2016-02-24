import pygame
from SetPropertiesList import SetPropertiesList
from State import State
# import SetProperies

from Scroller import Scroller

class MainState(State):
    
    def __init__(self, stack):
        State.__init__(self, stack)

        self.title  = 'main'
        self.modes  = 'overview setproperty clean guide player presets'.split(' ')
        self.scroller = Scroller(self.modes, 0)        
        
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)        
        self.title = self.scroller.get_value()
        if (self.title == 'clean'): self.title = ''
        
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 2 : 
                if self.scroller.get_value() == 'setproperty':
                    print 'setproperty'
                    SetPropertiesList(self.stack)
                    
        
    def draw(self, surface):
        if self.scroller.get_value() == 'guide':        
            pygame.draw.rect(surface, (96,96,96), (surface.get_width()/3, surface.get_height()/3, surface.get_width()/3, surface.get_height()/3, ))
        else:
            State.draw(self, surface)
        