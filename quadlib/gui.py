import sys
import pygame
import picamera

from pygame import time
from CameraWrapper import CameraWrapper
from states import MainState
from utils import mouse
import utils



#from PIL import Image, ImageDraw, ImageFont

def main():

    def fps(surface):
        milliseconds = clock.tick(fpslimit)        
        utils.txt(surface, (utils.screen['resolution'][0] - 30, utils.screen['margin']), str(round(clock.get_fps())))
        

    #pygame init
    pygame.init()    
    pygame.mouse.set_visible(False)    
    
    # screen resolution: http://www.purdyelectronics.com/pdf/AND-TFT-25PA.pdf
    #screenSize = (234,160)
    captureSize =   (320,240)
    #captureSize =   (160,120)
    fpslimit    =   24
    # screenSize  =   (pygame.display.Info().current_w,pygame.display.Info().current_h)
    # screenSize  = (((screenSize[0] + 31) // 32) * 32,((screenSize[1] + 15) // 16) * 16,)
    screenSize = utils.screen['resolution']
    
    clock = time.Clock()

    # settin up camera
    camera = picamera.PiCamera()
    camera.resolution = captureSize
    camera.rotation   = 180
    
    camera.start_preview()
    
    state_stack = []    
    main_state = MainState.MainState(state_stack, CameraWrapper(camera))
    
    #screen = pygame.display.set_mode(screenSize,0)
    camera.start_preview()
    overlay_renderer = None
    overlay_renderer2 = None
    
    # menu = Menu(root_options)
    
    overlaySize =  (((screenSize[0] + 31) // 32) * 32,((screenSize[1] + 15) // 16) * 16,)
    # overlaySize =  (128,((screenSize[1] + 16) // 16) * 16,)
    
#    print 'screenSize ',screenSize, (((screenSize[0] + 31) // 32) * 32, ((screenSize[1] + 15) // 16) * 16,)
    surface_top = pygame.Surface(overlaySize, 0, 24)
    surface_bottom = pygame.Surface(overlaySize, 0, 24)
    
   
    while True:
        ú
        surface_top = pygame.Surface(overlaySize, 0, 24)


        for event in pygame.event.get():             
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                cam.stop()
                pygame.quit()
                sys.exit()
            
            state_stack[0].event(event)
            if event.type == utils.CHANGE_DISPLAY_SETTINGS:
                if event.command == 'alpha':
                    overlay_renderer.alpha = event.value
                if event.command == 'readd':
                    camera.remove_overlay(overlay_renderer)
                    overlaySize = event.screenSize
                    surface_top = pygame.Surface(overlaySize, 0, 24)                    
                    overlay_renderer = camera.add_overlay(surface_top.get_buffer().raw, layer = 3, size = overlaySize, alpha = 64);
                    
        fps(surface_top)
            
        state_stack[0].draw(surface_top)
                           
        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(surface_top.get_buffer().raw, layer = 3, size = overlaySize, alpha = 0);            
        else:     
            try:    
                if overlay_renderer.alpha > 0:                       
                    overlay_renderer.update(surface_top.get_buffer().raw)
            except:
                pass
    
                
                    

    
if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except:
    #     print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]