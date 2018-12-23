import time, os
import utils

# from utils import log

def create_gif(id, employees, settings, camerasettings):	

    cmd = 'convert -delay '+str(camerasettings['delay'])+' -size '
    cmd += camerasettings['gifresolution'] + ' -loop 0 '
    foundpics = 0
    pictureCnt = len(employees.keys())+1
    log('[number of images we are looking for]', str(pictureCnt))
    for i in range(pictureCnt):
        filename = utils.get_file_name_for_id(id, i)        
        if os.path.exists(filename):
            foundpics += 1;
            cmd += filename +' '
            log(filename)
    
    for i in range(foundpics-2):
        filename = utils.get_file_name_for_id(id, foundpics-i-2)            
        if os.path.exists(filename):
                cmd += filename +' '
                log(filename)

    cmd += settings['outputpath'] + '%04d' % id +'.gif'
    if foundpics > 1:
        starttime = time.time()
        log('[convert] start ', str(id), cmd)
        os.system(cmd)
        log('[convert] ended ', str(id), ' time: ', str((time.time() - starttime)) )
    else:
        # utils.trace()
        log('[convert] Only one pic!')
        os.system('mv '+utils.get_file_name_for_id(id, 1) + ' ' + settings['outputpath'] )

