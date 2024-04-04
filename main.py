# MODULES
import serial, json, time

import eeg as eg

# SETTIGNS
treshold = None

# COMMANDS
def commandFunction(eog, eeg):

    while eeg != None:

        if eeg.attention >= treshold:
            direction = 'Forward'
            command = 1
        else:
            direction = 'Stop'
            command = 0
                
        return command, direction

if __name__ == '__main__':

    is_connected = 0
    while True:

        to_json = {
                'is_connected': is_connected
        }
        json_object = json.dumps(to_json)

        with open('UI/bt.json', 'w') as f:
            f.write(json_object)
            f.close()

        if is_connected == 0:
            try:
                eeg = eg.Headwear('/dev/rfcomm1')
                mtr = serial.Serial('/dev/ttyACM0', 9600)
                print('Devices Connected')
                is_connected = 1
                time.sleep(1)
            except:
                is_connected = 0
                print('Devices not Connected')
                time.sleep(1)

        elif is_connected == 1:
            try:
                command, direction = commandFunction(eeg)
            except:
                is_connected = 0
                break

            to_json = {
                'direction': direction
            }
            json_object = json.dumps(to_json)

            with open('UI/direction.json', 'w') as f:
                f.write(json_object)
                f.close()

            f = open('UI/data.json')
            data = json.load(f)
            speed = data['combinedValues']
            f.close()

            command_new = str(command) + ':' + str(speed)


            print(f'ATTENTION: {eeg.attention:2d} |', 
                  f'POOR_SIGNAL: {eeg.poor_signal} ||',
                  f'COMMANND: {command_new}',
                  f'|| {direction}')
            
            try:
                if command != 0:
                    mtr.write(str(command_new).encode('utf-8'))
            except KeyboardInterrupt:
                mtr.write('0'.encode('utf-8'))
