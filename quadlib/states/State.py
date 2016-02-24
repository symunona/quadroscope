import pygame

class State:  
    title = 'dummy'  
    def __init__(self, stack):       
        self.stack = stack         
        stack.insert(0, self)
        self.fontobject=pygame.font.SysFont('Arial', 28)    
         
    def back(self):
        print self.stack
        if len(self.stack) > 1 :
            self.stack.pop(0)
            
    def draw(self, surface): 
        if len(self.title) > 0:                         
            surface.blit(self.fontobject.render(self.title, 1, (0,255,0) ) , (40, 10))        

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 1: 
                self.back()
