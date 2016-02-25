from State import State

offsety = 240
offsetx = 300

class SetProperty(State):
    def __init__(self, stack, question, success_callback):
        State.__init__(self, stack)
        
        self.title  =  question
        self.success_callback = success_callback
        self.scroller = Scroller(['no','yes'])
         
    def draw(self, surface):        
        utils.txt(surface, offsetx, offsety, self.scroller.get_value())
    
    def event(self, event):
        
        self.scroller.event(event)
                            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ok
            if event.button == 2 :
                self.success_callback()                
                self.back()
                return 
                
            # cancel
            if event.button == 1 :                
                self.back()
                return

        State.event(self, event)
                