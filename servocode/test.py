import utilities

mynum = -6
readwrong=250 

#print(utilities.twos_comp(mynum, 4))
#negnum = (-10).to_bytes(length=1, byteorder='big', signed=True)
#print(negnum)
#string = bin(-10)
#print(string)

bitstr = mynum.to_bytes(length=readwrong.bit_length(), byteorder='big', signed=True)
print(bitstr)

