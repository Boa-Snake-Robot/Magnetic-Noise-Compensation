import utilities

mynum = -10

print(utilities.twos_comp(mynum, 4))
negnum = (-10).to_bytes(length=1, byteorder='big', signed=True)
print(negnum)
string = bin(-10)
print(string)