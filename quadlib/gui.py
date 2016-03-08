import sys, io, yuv2rgb, os, thread
import pygame

from pygame import time
from CameraWrapper import CameraWrapper
from states import MainState
import utils
from utils import mouse
from utils import pygame_utils


#from PIL import Image, ImageDraw, ImageFont

def main(settings = None, boss = True, updater = None, camera_wrapper = None):

    pitft = True
    
    if pitft:
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv('SDL_FBDEV'      , '/dev/fb1')

    def fps(surface):
        milliseconds = clock.tick(fpslimit)        
        pygame_utils.txt(surface, (utils.screen['resolution'][0] - 30, utils.screen['margin']), str(round(clock.get_fps())))
        
       
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

    if camera_wrapper == None: 
        print '[error] no camera object'

    # settin up camera   
    camera_wrapper.camera.resolution = captureSize
    camera_wrapper.camera.rotation   = 180
    
    if not pitft:
        camera_wrapper.camera.start_preview()
    
    # Buffers for viewfinder data
    rgb = bytearray(320 * 240 * 3)
    yuv = bytearray(320 * 240 * 3 / 2)
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    
    state_stack = []    
         
    
    
    #screen = pygame.display.set_mode(screenSize,0)
    
    
    overlay_renderer = None
    overlay_renderer2 = None
    
    # menu = Menu(root_options)
    
    overlaySize =  (((screenSize[0] + 31) // 32) * 32,((screenSize[1] + 15) // 16) * 16,)
    # overlaySize =  (128,((screenSize[1] + 16) // 16) * 16,)
    
#    print 'screenSize ',screenSize, (((screenSize[0] + 31) // 32) * 32, ((screenSize[1] + 15) // 16) * 16,)
        
    
    # GUI State handler
    main_state = MainState.MainState(state_stack, updater, camera_wrapper)
    
    thread.start_new_thread(pygame_utils.watch_trigger, ())
    
    preview = True
    splash = None
    
    while True:
        
        stream = io.BytesIO()        
        camera_wrapper.camera.capture(stream, use_video_port=True, format='raw')
        stream.seek(0)
        stream.readinto(yuv)  # stream -> YUV buffer
        stream.close()
        yuv2rgb.convert(yuv, rgb, captureSize[0], captureSize[1])
        
        img = pygame.image.frombuffer(rgb[0:
            (captureSize[0]* captureSize[1] * 3)],
            captureSize, 'RGB')
        
        # surface_top = pygame.Surface(overlaySize, 0, 24)
        
        screen.blit(img,
            ((320 - img.get_width() ) / 2,
            (240 - img.get_height()) / 2))

        pygame_utils.splash(screen)

        for event in pygame.event.get():             
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                camera_wrapper.camera.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame_utils.TAKE_PICTURE:
                preview = False
                state_stack[0].draw(screen)                
                camera_wrapper.make_photos()                
                updater.sync_camera_settings()
                
            state_stack[0].event(event)
            # if event.type == pygame_utils.CHANGE_DISPLAY_SETTINGS:
                # if event.command == 'alpha':
                #     overlay_renderer.alpha = event.value
                # if event.command == 'readd':
                #     camera_wrapper.camera.remove_overlay(overlay_renderer)
                #     overlaySize = event.screenSize
                #     surface_top = pygame.Surface(overlaySize, 0, 24)                    
                #     overlay_renderer = camera_wrapper.camera.add_overlay(surface_top.get_buffer().raw, layer = 3, size = overlaySize, alpha = 64);
                    
        fps(screen)
        
        state_stack[0].draw(screen)
                           
        if pitft:
            pygame.display.update()
        
        else:
            # if not overlay_renderer:
            #     overlay_renderer = camera_wrapper.camera.add_overlay(surface_top.get_buffer().raw, layer = 3, size = overlaySize, alpha = 0);            
            # else:     
            #     try:    
            #         if overlay_renderer.alpha > 0:                       
            #             overlay_renderer.update(surface_top.get_buffer().raw)
            #     except:
            #         pass
            pass
            
    
                
                    

    
if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except:
    #     print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
