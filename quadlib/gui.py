import sys
import pygame
import picamera
from menu import Menu
from pygame import time
from CameraWrapper import CameraWrapper

from states import MainState


#from PIL import Image, ImageDraw, ImageFont

def main():

    def txt(surface,x,y, message, color = (255, 255, 255)):
        fontobject=pygame.font.SysFont('Arial', 28)
        if len(message) != 0:
            surface.blit(fontobject.render(message, 1, color), (x, y))

    def fps(surface):
        milliseconds = clock.tick(fpslimit)        
        txt(surface, 600, 5, str(clock.get_fps()))
        

    #pygame init
    pygame.init()
    pygame.mouse.set_visible(False)
    
    # screen resolution: http://www.purdyelectronics.com/pdf/AND-TFT-25PA.pdf
    #screenSize = (234,160)
    captureSize =   (320,240)
    #captureSize =   (160,120)
    fpslimit    =   15
    screenSize  =   (pygame.display.Info().current_w,pygame.display.Info().current_h)
    # screenSize  = (((screenSize[0] + 31) // 32) * 32,((screenSize[1] + 15) // 16) * 16,)
    mode  = 'overview'
    modes = 'overview setproperty clean guide player presets'.split(' ')

    
        # [ {'label': 'First option!'},
        #         {'label': 'Second option!'},
        #         {'label': 'Third option!'},
        #         {'label': 'Fouth option!'},
        #         {'label': 'Fifth option!'},
        #         {'label': 'Sixth option!'},
        #         {'label': 'Seventh option!'},
        #         {'label': 'Eight option!'},
        #         {'label': 'Ninth option!'},
                
        #          ]
    
    
    # menu.screen_topleft_offset = (50,50)
    # menu.color = (255,255,255,100)
    # menu.focus_color = (255,255,0)

    clock = time.Clock()

    # settin up camera
    camera = picamera.PiCamera()
    camera.resolution = captureSize
    camera.rotation   = 180
    
    camera.start_preview()
    
    state_stack = []    
    MainState.MainState(state_stack, CameraWrapper(camera))
    
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
        
        surface_top = pygame.Surface(overlaySize, 0, 24)
        # pygame.draw.rect(surface_top, (32,32,32), (0,0,overlaySize[0], overlaySize[1] ))
        
        fps(surface_top)    

        state_stack[0].draw(surface_top)

        # x = 32
        # for i in range(8):
        #     pygame.draw.rect(surface_top, (256/8*i,256/8*i,256/8*i), (i*x, 10, x, 128, ))

        # for i in range(8):
        #     pygame.draw.rect(surface_top, (256/8*i,256/8*i,256/8*i, 128), (i*x, 128, x, 128, ))

        # menu.draw(surface_top)   

                
        # pygame.draw.rect(surface_top, (255,255,255), (10, 10, 20, 20))
        # pygame.draw.rect(surface_top, (128, 128, 128), (50, 50, 100, 100))
        
        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(surface_top.get_buffer().raw, layer = 3, size = overlaySize, alpha = 64);
        else:     
            try:       
                overlay_renderer.update(surface_top.get_buffer().raw)
            except:
                print '.'

        # if not overlay_renderer2:
        #     overlay_renderer2 = camera.add_overlay(surface_bottom.get_buffer().raw, layer = 3, size = overlaySize, alpha = 16);
        # else:     
        #     try:       
        #         overlay_renderer2.update(surface_bottom.get_buffer().raw)
        #     except:
        #         print '.'
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    cam.stop()
                    pygame.quit()
                    sys.exit()
                
                state_stack[0].event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print event.button, " -- mousebutton"
                
                
                    

    
if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except:
    #     print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]