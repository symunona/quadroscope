from evdev import InputDevice
from select import select
import pygame
import thread

MOUSEWHEEL = pygame.USEREVENT + 1

def mouse_event_listener():
    print 'started mouse listener'
    
    dev = InputDevice('/dev/input/event0') # This can be any other event number. On my Raspi it turned out to be event0
    while True:
        r,w,x = select([dev], [], [])
        for event in dev.read():
            # The event.code for a scroll wheel event is 8, so I do the following
            if event.code == 8:
                pygame_event = pygame.event.Event(MOUSEWHEEL, {'delta': event.value })
                pygame.event.post(pygame_event)
                # print(event.value)
                
thread.start_new_thread( mouse_event_listener, () )
