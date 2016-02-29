

import convert
import time

def make_photos(updater, fileid, filename, camera):

    # if boss, then upload settings to other cameras
            
    camera.take_picture(filename)
            
    # mode 1: it downloads the files 
    # if not isBoss:
    #     print "[listener] i am an employee. Uploading image to boss@" + bossip		
    #     updater.upload_photo(filename, bossip, settings)

    print("[listener] Picture took. Listening.")


def camera_loop(updater, gpio, camera):
    
    while True:

        fileid = updater.get_next_file_id()        
        filename = updater.get_file_name_for_id(fileid)
        
        gpio.wait_for_trigger()                     # ____/
            
        camera.reload_camera_settings()
        camera.make_photos(updater, fileid, filename)       # break break
        
        gpio.wait_for_release()                     #     \____
        