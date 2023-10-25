# IMPORTS

import serial
import numpy as np
import json
import torch
import collections

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
                    checker = 1
                    command = 3
                if result.item() <= 0.3:
                    checker = 1
                    command = 2
                if eeg.attention >= tresh_attention:
                    checker = 1
                    command = 1
                if eeg.attention < tresh_attention:
                    checker = 1

            while checker == 1:
                timer+=1

                if timer >= 3000:
                    checker = 0
                    timer = 0
                    command = 0
                
                return result, command

if __name__ == '__main__':
    eog = serial.Serial('/dev/tty.usbserial-1110', 9600, timeout=1)
    eeg = eg.Headwear('/dev/tty.usbmodem2017_2_251')
    #mtr = serial.Serial('/dev/tty.usbmodem11201', 9600, timeout=1)

    while True:

        f = open('data.json')
        data = json.load
        speed = data['speed']

        result, command = commandFunction(eog, eeg)

        command_new = str(command) + ':' + speed

        print('EOG:', f'{result.item():.2f} | ', 'ATTENTION: ', f'{eeg.attention:2d} | ','COMMANND: ', command, f'|| {command_new}')
        #try:
        #    mtr.write(str(command).encode('utf-8'))
        #except KeyboardInterrupt:
        #    mtr.write('0'.encode('utf-8'))