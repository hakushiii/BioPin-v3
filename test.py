import eeg, eog

tresh_attention = 70
speed = 155

def getCommands(eg,og):

    checker, timer = 0, 0

    while checker == 0:

        if og.result >= 0.7:
            checker = 1
            command = 3
        if og.result <= 0.3:
            checker = 1
            command = 2
        if eeg.attention >= tresh_attention:
            checker = 1
            command = 1
        if eeg.attention < tresh_attention:
            checker = 1

    while checker == 1:
        timer += 1 
        if timer >= 3000:
            checker = 0
            timer = 0
            command = 0

        return command

if __name__ == '__main__':

    speed = '100'

    og = eog.Headwear('/dev/tty.usbserial-1110', 9600, timeout=1)
    eg = eeg.Headwear('/dev/tty.usbmodem2017_2_251')
    #mtr = serial.Serial('/dev/tty.usbmodem11201', 9600, timeout=1)

    while True:

        command = getCommands(og, eg)

        command_new = str(command) + ':' + speed

        print('EOG:', f'{og.result:.2f} | ', 'ATTENTION: ', f'{eg.attention:2d} | ','COMMANND: ', command, f'|| {command_new}')
        #try:
        #    mtr.write(str(command).encode('utf-8'))
        #except KeyboardInterrupt:
        #    mtr.write('0'.encode('utf-8'))