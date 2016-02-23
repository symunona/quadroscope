import sys
import pygame
import pygame.camera
from pygame import time

menu = 

fpslimit = 15

clock = time.Clock()

pygame.init()
pygame.camera.init()

# screen resolution: http://www.purdyelectronics.com/pdf/AND-TFT-25PA.pdf

#screenSize = (234,160)

captureSize = (320,240)

screenInfo = pygame.display.Info()
screenSize = (screenInfo.current_w, screenInfo.current_h)

screen = pygame.display.set_mode(screenSize,0)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],captureSize)
cam.start()

pygame.mouse.set_visible(False)

print '///////////////////////////'
print screenSize, ' ', captureSize
print screen.get_size()



background = pygame.Surface(screen.get_size())


option_selected = None

def option1():
    global option_selected     
    option_selected = 1
def option2():
    global option_selected     
    option_selected = 1

menu.options = ( {'label': 'First option!', 'callable': option1},{'label': 'Second option!', 'callable': option2}, )
menu.screen_topleft_offset = (50,50)



menu.color = (255,255,255,100)
menu.focus_color = (255,255,0)
     
def menu():
    global background
    txt(5, 5, 'hello world')
    menu.draw(background)


def txt(x,y, message, color = (255, 255, 255)):
    fontobject=pygame.font.SysFont('Arial', 28)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, color), (x, y))

def fps():
    milliseconds = clock.tick(fpslimit)
    
    txt(600, 5, str(clock.get_fps()))
    

pygame.display.set_caption("TEST")

while True:
   image1 = cam.get_image()
   image1 = pygame.transform.scale(image1,screenSize)
     
   screen.blit(image1,(0,0))
   
   menu()
   
   fps()
   
   pygame.display.update()
   
   for event in pygame.event.get():
          if event.type == pygame.QUIT or event.type == KEYDOWN:
            cam.stop()
            pygame.quit()
            sys.exit()
            