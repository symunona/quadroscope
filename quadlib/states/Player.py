import pygame
from .. import utils
from ..utils import dir 
from ..utils.Scroller import Scroller
from State import State
from ..utils.GIFImage import GIFImage
from ..utils import pygame_utils


lineheight = 40

class Player(State):
    def __init__(self, stack):
        State.__init__(self, stack)        
        self.title  = 'player'
        self.path = utils.settings['outputpath']
        self.image = None
        self.dimensions = (0,0)
         
        self.mode = 'standard'
        
        # self.files = [f for f in listdir(self.path) if isfile(join(self.path, f))]       
        # print      
        self.scroller = Scroller(dir.get_images_sorted(self.path),0, self.load_image)
        
        self.filename = self.scroller.get_value(0)
        
        self.load_image(self.filename)
        
        pygame_event = pygame.event.Event(pygame_utils.CHANGE_DISPLAY_SETTINGS, {'command': 'alpha', 'value': 255})
        pygame.event.post(pygame_event)     
        
    def load_image(self, image, last = None):
        self.filename = self.path + image
        self.mode = 'standard'

        image = pygame.image.load(self.filename)
        self.dimensions = image.get_size()       
        self.image = pygame.transform.scale(image, utils.screen['resolution'])
    
    def draw(self, surface):        
        if self.image != None:
            if self.mode == 'standard':                                        
                surface.blit(self.image,(0,0))
            else:
                if self.mode == 'playing':                        
                    gif = pygame.Surface(self.dimensions, 0, 24)            
                    self.image.render(gif, (0,0))
                    gif = pygame.transform.scale(gif, utils.screen['resolution'])
                    surface.blit(gif,(0,0))            
        State.draw(self, surface)
        
    
    def back(self):
        pygame_event = pygame.event.Event(pygame_utils.CHANGE_DISPLAY_SETTINGS, {'command': 'alpha', 'value': 64})
        pygame.event.post(pygame_event)     
        State.back(self)    
            
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)
        self.title = self.scroller.get_value()                
        
        if event.type == pygame.MOUSEBUTTONDOWN:       
            if event.button == 2:
                self.mode = 'playing'
                self.image = GIFImage(self.filename)                                             
                    
