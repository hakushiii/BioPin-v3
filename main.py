# IMPORTS

import serial
import numpy as np
import json
import torch
import collections
import time

import eeg as eg

from random import randint

# MODEL
class ProfessorXModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_block_1 = torch.nn.Sequential(
            torch.nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3),
            torch.nn.ReLU(),
            torch.nn.Conv1d(in_channels=16, out_channels=16, kernel_size=2),
            torch.nn.ReLU(),
        )
        self.conv_block_2 = torch.nn.Sequential(
            torch.nn.Conv1d(in_channels=16, out_channels=16, kernel_size=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool1d(kernel_size=2),
        )
        self.conv_block_3 = torch.nn.Sequential(
            torch.nn.Conv1d(in_channels=16, out_channels=16, kernel_size=2),
            torch.nn.ReLU(),
            torch.nn.MaxPool1d(kernel_size=2),
        )
        self.classifier = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(in_features=16*11, out_features=128),
            torch.nn.Linear(in_features=128, out_features=1),
            torch.nn.Sigmoid()
        )

    def forward(self, x):
        snr = 1.
        std = torch.std(x)
        x += (2. * torch.rand(x.shape) - 1.) * 2. * std * snr

        result = self.classifier(self.conv_block_3(self.conv_block_2(self.conv_block_1(x))))
        return torch.squeeze(result)


# LOAD TRAINED MODEL
model = torch.load('model_overall.pt')

# EVALUATE MODEL
model.eval()

# COMMANDS
def commandFunction(eog, eeg):

    length = 50
    queue = collections.deque(maxlen=length)
    count,timer = 0, 0
    checker = 0
    tresh_attention = 70
    command = 0
    
    while (eog and eeg) != None:
        val = eog.readline()
        try:
            output = val.decode('UTF-8').rstrip()
            output = float(output)
            output = output * 10
        except ValueError:
            output = 0.00

        queue.append(output)

        if count < 50:
            count += 1
        else:
            queue_numpy = np.array(queue).astype(float)
            queue_tensor = torch.from_numpy(queue_numpy[:]).unsqueeze(0).unsqueeze(0).to(torch.float32)

            with torch.inference_mode():
                result = model(queue_tensor)

            while checker == 0:

                if result.item() >= 0.7:
                    direction = 'Rightward'
                    checker = 1
                    command = 3
                elif result.item() <= 0.3:
                    direction = 'Leftward'
                    checker = 1
                    command = 2
                elif eeg.attention >= tresh_attention:
                    direction = 'Forward'
                    checker = 1
                    command = 1
                elif eeg.meditation >= tresh_attention:
                    direction = 'Backward'
                    checker = 1
                    command = 4
                else:
                    direction = 'Stop'
                    checker = 1
                    command = 0

            while checker == 1:
                timer+=1

                if timer >= 3000:
                    checker = 0
                    timer = 0
                    command = 0
                
                return queue_numpy, result, command, direction

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
                eog = serial.Serial('/dev/rfcomm0', 9600)
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
                eog.read()
            except:
                is_connected = 0
                break

            queue, result, command, direction = commandFunction(eog, eeg)

            command_new = str(command) + ':' + speed

            f = open('data.json')
            data = json.load
            speed = data['speed']
            f.close()

            to_json = {
                'array': queue
            }
            json_object = json.dumps(to_json)

            with open('UI/eog.json', 'w') as f:
                f.write(json_object)
                f.close()

            to_json = {
                'direction': direction
            }
            json_object = json.dumps(to_json)

            with open('UI/direction.json', 'w') as f:
                f.write(json_object)
                f.close()

            print('EOG:', f'{result.item():.2f} | ', 'ATTENTION: ', f'{eeg.attention:2d} | ',f'COMMANND: {command} : {speed}', f'|| {direction}')
            
            try:
                mtr.write(str(command).encode('utf-8'))
            except KeyboardInterrupt:
                mtr.write('0'.encode('utf-8'))