import time, os
import utils


def create_gif(id, employees, settings, camerasettings):	


    cmd = 'convert -delay '+str(camerasettings['delay'])+' -size '
    cmd += camerasettings['resolution'] + ' -loop 0 '
    foundpics = 0
    pictureCnt = len(employees.keys())
    for i in range(pictureCnt):
        filename = utils.get_file_name_for_id(id, i+1)        
        if os.path.exists(filename):
            foundpics += 1;
            cmd += filename +' '
            
        for i in range(foundpics-2):
            filename = utils.get_file_name_for_id(id, foundpics-i-1)            
            if os.path.exists(filename):
                    cmd += filename +' '

    cmd += settings['outputpath'] + '%04d' % id + '-'+camerasettings['resolution']+'.gif'
    if foundpics > 1:
        starttime = time.time()
        print '[convert] start ', str(id), cmd
        os.system(cmd)
        print '[convert] ended ', str(id), ' time: ', str((time.time() - starttime)) 
    else:
        # utils.trace()
        print '[convert] Only one pic!'
        os.system('mv '+utils.get_file_name_for_id(id, 1) + ' ' + settings['outputpath'] )

