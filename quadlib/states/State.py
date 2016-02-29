import pygame
from .. import utils

class State:  
    title = 'dummy'  
    def __init__(self, stack):       
        self.stack = stack         
        stack.insert(0, self)            
         
    def back(self):
        if len(self.stack) > 1 :
            self.stack.pop(0)
            
    def draw(self, surface): 
        utils.txt(surface, (utils.screen['margin'], utils.screen['margin']), self.title, (255,255,0),  )

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 1: 
                self.back()
