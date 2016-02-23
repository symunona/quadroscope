import sys
import pygame
import picamera
from pygame import time
#from PIL import Image, ImageDraw, ImageFont

def main():

    def menu(): 
        print 'asdf'   

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
    modes = 'overview setproperty clean guide player presets'

    #menu.options = [ {'label': 'First option!', 'callable': option1},{'label': 'Second option!', 'callable': option2} ]
    # menu.screen_topleft_offset = (50,50)
    # menu.color = (255,255,255,100)
    # menu.focus_color = (255,255,0)

    clock = time.Clock()

    # settin up camera
    camera = picamera.PiCamera()
    camera.resolution = captureSize
    camera.rotation   = 180
    
    camera.start_preview()
    

    #screen = pygame.display.set_mode(screenSize,0)

    camera.start_preview()
    overlay_renderer = None
    overlay_renderer2 = None
    
    # overlaySize =  (((screenSize[0] + 31) // 32) * 32,((screenSize[1] + 15) // 16) * 16,)
    overlaySize =  (((screenSize[0] + 31) // 32) * 32,((screenSize[1] + 16) // 16) * 16,)
    
#    print 'screenSize ',screenSize, (((screenSize[0] + 31) // 32) * 32, ((screenSize[1] + 15) // 16) * 16,)
    surface_top = pygame.Surface(overlaySize, 0, 24)
    surface_bottom = pygame.Surface(overlaySize, 0, 24)
    
    while True:
        
        surface_top = pygame.Surface(overlaySize, 0, 24)
        
        #menu()   
        fps(surface_top)    

        x = 32
        for i in range(8):
            pygame.draw.rect(surface_top, (256/8*i,256/8*i,256/8*i), (i*x, 10, x, 128, ))

        for i in range(8):
            pygame.draw.rect(surface_top, (256/8*i,256/8*i,256/8*i, 128), (i*x, 128, x, 128, ))
                
        # pygame.draw.rect(surface_top, (255,255,255), (10, 10, 20, 20))
        # pygame.draw.rect(surface_top, (128, 128, 128), (50, 50, 100, 100))
        
        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(surface_top.get_buffer().raw, layer = 3, size = overlaySize, alpha = 48);
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print event.button, " -- expecting 4 or 5 here"
                    
                
                    

    
if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except:
    #     print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]