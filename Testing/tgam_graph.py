import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv, os

dir = 'Testing/'
dir1 = dir + 'forward-reverse/FORWARD/'
dir2 = dir + 'forward-reverse/REVERSE/'

if __name__ == '__main__':

    dir_ext = dir + 'OUTPUT/'

    if not os.path.exists(dir_ext):
        os.mkdir(dir_ext)
    if not os.path.exists(dir_ext+'FORWARD/'):
        os.mkdir(dir_ext+'FORWARD/')
    if not os.path.exists(dir_ext+'REVERSE/'):
        os.mkdir(dir_ext+'REVERSE/')    

    count = 0
    for fn in os.listdir(dir1):
        if fn.endswith('.csv'):
            count += 1            
            print(count, fn)
            fp = os.path.join(dir1, fn)

            data = pd.read_csv(fp)
            
            data.plot(y='ATTENTION', kind='line', linestyle='-', color='blue')
            
            if data.shape[0] == 180:            
                plt.axhline(y=70, color='red', linestyle='--', label='Threshold at 70')
                plt.ylabel('Attention Value')
                plt.title(f'Attention Trial {count}')

                plt.savefig(f'{dir}OUTPUT/FORWARD/Attention Trial {count}.png')
                plt.close()
            else:
                print('Skipped')

    count = 0
    for fn in os.listdir(dir2):
        if fn.endswith('.csv'):
            count += 1
            print(count, fn)
            fp = os.path.join(dir2, fn)

            data = pd.read_csv(fp)
            data = data.rename(columns={'MEDITATIOn':'MEDITATION'})
            
            data.plot(y='MEDITATION', kind='line', linestyle='-', color='blue')

            if data.shape[0] == 180:
                plt.axhline(y=70, color='red', linestyle='--', label='Threshold at 70')
                plt.ylabel('Meditation Value')
                plt.title(f'Meditation Trial {count}')

                plt.savefig(f'{dir}OUTPUT/REVERSE/Meditation Trial {count}.png')
                plt.close()
            else:
                print('Skipped')