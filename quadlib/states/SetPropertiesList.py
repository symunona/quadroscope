from State import State
import camera_settings
import utils
from Scroller import Scroller

lineheight = 40

class SetPropertiesList(State):
    def __init__(self, stack):
        State.__init__(self, stack)

        self.title  = 'setProperties'
        
        self.settings_menu = []     
        for setting in camera_settings.camera_settings:            
            menuitem = setting['key']        
            self.settings_menu.append(menuitem)
            
        self.scroller = Scroller(self.settings_menu)
        
    def draw(self, surface):
        State.draw(self, surface)
        for i in range (5):
            txt = self.scroller.get_value( self.scroller.get_index() - 2 + i )
            color = (255,255,255)
            if (i == 2):
                color = (0, 255, 255)
            utils.txt(surface, 60, 100 + (i*lineheight), txt, color )
        
    def event(self, event):
        State.event(self, event)
        self.scroller.event(event)                
        
         
        # if event.type == pygame.MOUSEBUTTONDOWN:                        
        #     if event.button == 2 : 
        #         if self.scroller.get_value() == 'setproperty':
        #             print 'setproperty'
                    
