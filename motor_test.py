import serial

mtr = serial.Serial('/dev/tty.usbmodem11101', 9600, timeout=.1)

print('connected to', mtr)

while True:

        command = input() # <command>:<speed>

        try:
            print('sent', command)
            mtr.write(command.encode('utf-8'))
        except KeyboardInterrupt:
            print('no sent')
            mtr.write('0'.encode('utf-8'))
        
        val = mtr.readline()
        print(val)