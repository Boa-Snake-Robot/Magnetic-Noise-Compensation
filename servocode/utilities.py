import time

def writeToFile(filename, data, withTimestamps = False):
    f = open(filename, 'a')
    if withTimestamps:
        f.write('%s' % (time.time()))
        f.write(', ')
    f.write('%s' % (data))
    f.write('\n')
    f.close()
    return

def writeDataArrayToFile(filename, data, withTimestamps = False):
    f = open(filename, 'a')
    if withTimestamps:
        f.write('%s' % (time.time()))
    for element in data:
        f.write(', ')
        f.write('%03d ' % (element))
    f.write('\n')
    f.close()
    return