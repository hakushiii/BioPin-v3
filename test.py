import serial

og = serial.Serial('COM4')

while True:
    print(og.readline())