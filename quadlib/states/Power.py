import pygame

from State import State
from SetProperty import SetProperty 

from .. import utils
from ..utils import pygame_utils
from .. import CameraSettings
from ..utils.Scroller import Scroller
from ..utils.Confirm import Confirm
from ..updater import Updater 

class Power(State):
    def __init__(self, stack, updater):
        State.__init__(self, stack)
        
        self.title  = 'power'
        self.modes  = 'shutdown reboot restart'.split(' ')
        self.updater = updater    
        self.scroller = Scroller(self.modes)
                    
        
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)                        
        self.title = self.scroller.get_value()
        
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 2 :
                if self.scroller.get_value() == 'shutdown':
                    self.updater.shutdown()
                    
                if self.scroller.get_value() == 'reboot':
                    self.updater.reboot()
                    
                if self.scroller.get_value() == 'restart':
                    self.updater.restart_employees()
                
                    
