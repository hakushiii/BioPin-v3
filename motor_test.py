import serial

mtr = serial.Serial('/dev/ttyACM0', 9600)

print('connected to', mtr)

while True:

        command = input() # <command>:<speed>

        try:
            print('sent', command)
            mtr.write(command.encode('utf-8'))
        except KeyboardInterrupt:
            print('no sent')
            mtr.write('0:0'.encode('utf-8'))
        
        val = mtr.readline()
        print(val)
