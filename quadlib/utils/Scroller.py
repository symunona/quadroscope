import pygame
import math
import mouse

class Scroller:

    def __init__(self, elements, index = 0, on_change = None):
        self.selected   = index
        self.elements = elements
        self.on_change = on_change

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
            
    def set_value(self, value):
        old_value = self.elements[self.selected] 
        self.selected = self.elements.index(value)
        if self.on_change != None:            
            self.on_change(self.elements[self.selected], old_value) 
    
    def event(self, event):
        if event.type == mouse.MOUSEWHEEL:
             
            new_index = self.selected + event.delta
            if new_index >= len(self.elements): new_index = 0
            if new_index < 0: new_index = len(self.elements)-1
            self.set_value(self.elements[new_index])

        # if event.type == pygame.MOUSEBUTTONDOWN:                        
        #     if event.button == 4 : self.selected -= 1
        #     if event.button == 5 : self.selected += 1
