#!/usr/bin/env python

def get_images_sorted(dirpath):
    from stat import S_ISREG, ST_CTIME, ST_MODE
    import os, sys, time

    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries if path.lower().endswith(('.jpg','.gif')))

    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
            for stat, path in entries if S_ISREG(stat[ST_MODE]))
    #NOTE: on Windows `ST_CTIME` is a creation date 
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date
    result = []
    for cdate, path in sorted(entries):
        result.insert(0,os.path.basename(path))
        # print time.ctime(cdate), os.path.basename(path)
        
    return result