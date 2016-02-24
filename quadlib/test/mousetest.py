from evdev import InputDevice
from select import select
dev = InputDevice('/dev/input/event0') # This can be any other event number. On my Raspi it turned out to be event0
while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        # The event.code for a scroll wheel event is 8, so I do the following
        if event.code == 8:
            print(event.value)