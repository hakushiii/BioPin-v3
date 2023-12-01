import serial
import eeg

og = serial.Serial('/dev/rfcomm0')
eg = eeg.Headwear('/dev/rfcomm1')
while True:
    print(og.readline(), eg.poor_signal)
