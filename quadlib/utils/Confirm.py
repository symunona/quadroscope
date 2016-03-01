import pygame
from .. import utils
from ..states.State import State
from ..utils.Scroller import Scroller
from ..utils import pygame_utils

offsety = pygame_utils.Calc.centerY(utils.screen['fontsize'])
offsetx = pygame_utils.Calc.centerX(10)

class Confirm(State):
    def __init__(self, stack, question, success_callback):
        State.__init__(self, stack)
        
        self.title  =  question
        self.success_callback = success_callback
        self.scroller = Scroller(['no','yes'])
         
    def draw(self, surface): 
        State.draw(self, surface)       
        pygame_utils.txt_large(surface, (offsetx, offsety), self.scroller.get_value(), (0,255,255))
        pygame_utils.txt(surface, (offsetx, offsety+30), self.scroller.get_value(self.scroller.get_index()+1), (128,128,128))
    
    def event(self, event):
        
        self.scroller.event(event)
                            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ok
            if event.button == 2 :
                if self.scroller.get_value() == 'yes':
                    self.success_callback()                
                self.back()
                return 
                
            # cancel
            if event.button == 1 :                
                self.back()
                return

        State.event(self, event)
                