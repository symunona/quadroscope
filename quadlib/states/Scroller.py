import pygame
import math

class Scroller:

    def __init__(self, elements, index = 0):
        self.selected   = index
        self.elements = elements

    def get_index(self):
        return self.selected
        
    def get_value(self, index = None):
        if index == None:
            return self.elements[self.selected]
        else:
            if index < 0:                 
                index = ( index + (len(self.elements) * math.floor( index / len(self.elements) ) ) )
            index = int(index % len(self.elements))
            
            return self.elements[index]
    
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:                        
            if event.button == 4 : self.selected -= 1
            if event.button == 5 : self.selected += 1
            if self.selected >= len(self.elements): self.selected = 0
            if self.selected < 0: self.selected = len(self.elements)-1