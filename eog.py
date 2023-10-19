# IMPORTS

import serial, threading
import numpy as np
import torch
import collections

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

class Headwear:
    """
    A Professor X headwear
    """

    class DongleListener(threading.thread):
        """
        Serial Listener for USB Dongle
        """

        def __init__(self, headwear, *args, **kwargs):
            """
            Set up listener device
            """
            self.headwear = headwear

        def run(self):
            """
            Run the listener thread
            """
            s = self.headwear.dongle
            self.headwear.running = True

            while self.headwear.running:
                payload = s.read()
                self.parse_payload(payload)

            if s and s.isOpen():
                s.close()

            def parse_payload(eog):
                count = 0

                while (eog) != None:
                    val = eog.readline()
                    try:
                        self.raw = val.decode('UTF-8').rstrip()
                        self.raw = float(self.raw)
                        self.raw = self.raw * 10
                    except ValueError:
                        self.raw = 0.00

                    self.queue.append(self.raw)

                    if count < 50:
                        count += 1
                    else:
                        queue_numpy = np.array(self.queue).astype(float)
                        queue_tensor = torch.from_numpy(queue_numpy[:]).unsqueeze(0).unsqueeze(0).to(torch.float32)

                        with torch.inference_mode():
                            output = model(queue_tensor)
                            self.result = output.item()

    def __init__(self, device, open_serial=True):
        """
        Initialize the headwear
        """
        self.dongle = None
        self.listener = None
        self.device = device
        self.length = 50
        self.queue = collections.deque(maxlen=self.length)
        self.result = 0
        self.raw = 0
        self.status = None
        self.running = False

        if open_serial:
            self.serial_open()

    def serial_open(self):
        if not self.dongle or not self.dongle.isOpen():
            self.dongle = serial.Serial(self.device, 9600)
        if not self.listener or not self.listener.isAlive():
            self.listener = self.DongleListener(self)
            self.listener.daemon = True
            self.listener.start()

    def serial_close(self):
        self.dongle.close()

    def stop(self):
        self.running = False


