import serial

#Hvis dette fungerer kan jeg lagre data direkte til fil istedenfor å holde på arduino ide </3

ARDUNIO_PORT        = '/dev/ttyUSB0' #check port
ARDUINO_BAUDRATE    = 9600

ser = serial.Serial(ARDUNIO_PORT, ARDUINO_BAUDRATE, timeout=1)
str_from_arduino = ser.readline()
print(str_from_arduino)