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

def twos_comp(val, bitlen):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bitlen - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bitlen)        # compute negative value
    return val 

def convertVel(num):
    velbitstring = num.to_bytes(length=5, byteorder='big')
    velbitman = velbitstring[-4:]
    return int.from_bytes(velbitman, byteorder='big', signed=True)