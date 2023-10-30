# IMPORTS

import serial
import numpy as np
import json
import torch
import collections
from datetime import datetime
import time, csv, os

from random import randint

import eeg as eg

speed = 100

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
model = torch.load('Model/model_overall.pt')

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
        #val = eog.readline()
        #try:
        #    output = val.decode('UTF-8').rstrip()
        #    output = float(output)
        #    output = output * 10
        #except ValueError:
        #    output = 0.00

        #queue.append(output)

        #if count < 50:
        #    count += 1
        #else:
        #    queue_numpy = np.array(queue).astype(float)
        #    queue_tensor = torch.from_numpy(queue_numpy[:]).unsqueeze(0).unsqueeze(0).to(torch.float32)

        #    with torch.inference_mode():
        #        result = model(queue_tensor)

            if checker == 0:
                #if result.item() >= 0.7:
                #    checker = 1
                #    command = 3
                #if result.item() <= 0.3:
                #    checker = 1
                #    command = 2
                if eeg.attention >= tresh_attention:
                    checker = 1
                    command = 1
                if eeg.attention < tresh_attention:
                    checker = 1
                else:
                    command = 0
            timer=0
            if checker == 1:
                timer+=1
                if timer >= 3000:
                    command = 0
                    checker = 0
                    timer = 0


            return result, command

def get_time_HM():

    now = datetime.now()
    return now.strftime('%H.%M')

def get_time_HMS():

    now = datetime.now()
    return now.strftime('%H:%M:%S')


if __name__ == '__main__':
    #eog = serial.Serial('/dev/rfcomm0', 9600)
    eeg = eg.Headwear('/dev/rfcomm1')

    eog = 1

    start_time = get_time_HM()

    with open(f'{start_time}.csv','w') as f:
        header = ['ITERATION','TIME','ARRAY','OUTPUT COMMAND']
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(header)

        count = 1
        while True:
            data = []

            result, command = commandFunction(eog, eeg)

            if command == 1:
                direction = 'Forward'
            elif command == 2:
                direction = 'Rightward'
            elif command == 3:
                direction = 'Leftward'
            elif command == 4:
                direction = 'Backward'
            else:
                direction = 'No Command'

            if direction != 'No Command':
                data.append(count)
                data.append(get_time_HMS())
                data.append(eeg.attention)
                data.append(direction)
                writer.writerow(data)
                print(data)
                count+=1

            #print('EOG:', f'{result.item():.2f} | ', 'ATTENTION: ', f'{eeg.attention:2d} | ', f'|| {direction}')