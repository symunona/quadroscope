#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import io
import pygame
import picamera

def main():
    """
    Displays preview on PiTFT with pygame module. It rapidly captures unencoded
    images from video port, add stats information to this images, and then
    display them on PiTFT. Because it uses pygame rpi-fbcp, a software that is
    required to run picamera_overlay.py, is no longer required. This process is
    slower because it captures images continuously and go through a process
    before refreshing the display device.
    """
    # os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
    # os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
    captureSize = (160,120)
    # setup pygame
    pygame.init()
    screenInfo = pygame.display.Info()
    screenSize = (screenInfo.current_w, screenInfo.current_h)
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode(screenSize,0)
    # setup picamera
    camera = picamera.PiCamera()
    camera.resolution = captureSize
    

    # prep a byte array to store captured image
    rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

    while True:
        stream = io.BytesIO()
        camera.capture(stream, use_video_port=True, format='rgb')
        stream.seek(0)
        stream.readinto(rgb)
        stream.close()

        img = pygame.image.frombuffer(rgb[0:(captureSize[0] * captureSize[1] * 3)], captureSize, 'RGB')
        
        screen.blit(img, (0,0))

        font = pygame.font.SysFont('freeserif', 18, bold=1)
        text = time.strftime('%H:%M:%S', time.gmtime())
        
        textSurface = font.render(text, 1, pygame.Color(255, 255, 255))
        screen.blit(textSurface, (10, 10))

        # finally update and display the image
        pygame.display.update()

if __name__ == "__main__":
    import sys
    try:
        main()
    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]