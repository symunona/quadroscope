
camera_settings = [
    
    {
        'key': 'saturation',
        'min': -100,
        'max': 100,
        'step': 5,
        'type': 'numeric'
         
    },
    {
        'key': 'contrast',
        'min': -100,
        'max': 100,
        'step': 5,
        'type': 'numeric'         
    },
    {
        'key': 'brightness',
        'min': 0,
        'max': 100,
        'step': 10,
        'type': 'numeric'         
    },
    {
        'key': 'saturation',
        'min': -100,
        'max': 100,
        'step': 5,
        'type': 'numeric'         
    },
    {
        'key': 'ISO',
        'min': 100,
        'max': 800,
        'step': 50,
        'type': 'numeric'         
    },
    {
        'key': 'exposure_conpensation',
        'min': 100,
        'max': 800,
        'step': 50,
        'type': 'numeric'         
    },
    {
        'key': 'meter_mode',
        'type': 'select',
        'values': 'average spot backlit matrix'.split(' ')
    },
    {
        'key': 'exposure_mode',
        'type': 'select',
        'values': 'off auto night nightpreview backlight spotlight sports snow beach verylong fixedfps antishake fireworks'.split(' ')
    },
    {
        'key': 'awb_mode',
        'type': 'select',
        'values': 'off auto sun cloudshade tungsten fluorescent incandescent flash horizon'.split(' ')
    },
    {
        'key': 'image_effect',
        'type': 'select',
        'values': 'off negative solarise whiteboard blackboard sketch denoise emboss oilpaint hatch gpen pastel watercolour film blur saturation cartoon'.split(' ')
    },
    {
        'key': 'color_effect-1',
        'min': 0,
        'max': 255,
        'step': 3,
        'type': 'numeric'    
    },
    {
        'key': 'color_effect-2',
        'min': 0,
        'max': 255,
        'step': 3,
        'type': 'numeric'    
    },    
    {
        'key': 'resolution',
        'type': 'select',       
        'values': '2592x1944 1296x972 640x480'.split(' ') 
    },
    
    #======================= output
    {
        'key': 'mode',
        'type': 'select',       
        'values': 'standard 4_loop_gif 4_delayed_gif timelapse'.split(' ') 
    },
    {
        'key': 'mode',
        'type': 'select',       
        'values': 'standard 4_loop_gif 4_delayed_gif'.split(' ') 
    },
    {
        'key': 'gif_delay',
        'min': 1,
        'max': 500,
        'step': 2,
        'type': 'numeric'         
    }

]
