

camera_settings = [
    
    {
        'key': 'saturation',
        'min': -100,
        'max': 100,
        'step': 5,
        'type': 'numeric',
        'default': 0
         
    },
    {
        'key': 'contrast',
        'min': -100,
        'max': 100,
        'step': 5,
        'type': 'numeric',
        'default': 0         
    },
    {
        'key': 'brightness',
        'min': 0,
        'max': 100,
        'step': 5,
        'type': 'numeric',
        'default': 50         
    },
    {
        'key': 'saturation',
        'min': -100,
        'max': 100,
        'step': 5,
        'type': 'numeric',
        'default': 0         
    },
    {
        'key': 'ISO',
        'min': 0,
        'max': 1600,
        'step': 100,
        'type': 'numeric',
        'default': 0         
    },
    {
        'key': 'exposure_compensation',
        'min': -25,
        'max': 25,
        'step': 5,
        'default': 0,
        'type': 'numeric'         
    },
    {
        'key': 'meter_mode',
        'type': 'select',
        'default': 'average',
        'values': 'average spot backlit matrix'.split(' ')
    },
    {
        'key': 'exposure_mode',
        'type': 'select',
        'default': 'off',
        'values': 'off auto night nightpreview backlight spotlight sports snow beach verylong fixedfps antishake fireworks'.split(' ')
    },
    {
        'key': 'awb_gain',
        'type': 'numeric',
        'info': 'only when awb is off',
        'min': 0,
        'max': 8,
        'step': 1,
        'default': 1
        
    },
    {
        'key': 'awb_mode',
        'type': 'select',
        'values': 'off auto sunlight cloudy shade tungsten fluorescent incandescent flash horizon'.split(' '),
        'default': 'off'
    },
    {
        'key': 'image_effect',
        'type': 'select',
        'default': 'none',
        'values': 'none negative solarize sketch denoise emboss oilpaint hatch gpen pastel watercolor film blur saturation colorswap washedout posterise colorpoint colorbalance cartoon deinterlace1 deinterlace2'.split(' ')
    },
    # {
    #     'key': 'color_effect-1',
    #     'min': 0,
    #     'max': 255,
    #     'step': 3,
    #     'type': 'numeric'    
    # },
    # {
    #     'key': 'color_effect-2',
    #     'min': 0,
    #     'max': 255,
    #     'step': 3,
    #     'type': 'numeric'    
    # },    
    {
        'key': 'resolution',
        'type': 'select',       
        'values': '2592x1944 1296x972 640x480'.split(' '),
        'default': '1296x972',
        'live': False 
    },
    
    #======================= output
    {
        'key': 'mode',
        'type': 'select',       
        'default': '4_loop_gif',
        'values': 'standard 4_loop_gif 4_delayed_gif timelapse'.split(' '), 
        'live': False
    },
    {
        'key': 'gif_delay',
        'default': 16,
        'min': 1,
        'max': 500,
        'step': 2,
        'type': 'numeric',
        'live': False         
    }

]


