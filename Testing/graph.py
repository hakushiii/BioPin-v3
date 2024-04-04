import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv, os

dir = 'Testing/'
dir1 = dir + 'left-right/'


if __name__ == '__main__':

    dir_ext = dir + 'OUTPUT/'  

    count = 0
    for fn in os.listdir(dir1):
        if fn.startswith('testtest'):
            count += 1            
            print(count, fn)
            fp = os.path.join(dir1, fn)

            data = pd.read_csv(fp)
            print(len(data))

            passed_right = len(data[(data['status'] > 0) & (data['command'] == 'right')])
            failed_right = len(data[(data['status'] == 0) & (data['command'] == 'right')])

            passed_left = len(data[(data['status'] > 0) & (data['command'] == 'left')])
            failed_left = len(data[(data['status'] == 0) & (data['command'] == 'left')])

            category = ['Passed', 'Failed']


            percentage_right = passed_right/(passed_right+failed_right) * 100
            percentage_left = passed_left/(passed_left+failed_left) * 100

            plt.bar(category, [passed_right, failed_right])

            plt.ylabel(f'EOG {percentage_right:.2f}%')
            plt.title(f'EOG Right')
            
            plt.savefig(f'{dir}OUTPUT/EOG Right.png')
            plt.close()

            plt.pie([passed_right, failed_right])
            plt.ylabel(f'EOG {percentage_right:.2f}%')
            plt.title(f'EOG Right')
            
            plt.savefig(f'{dir}OUTPUT/EOG Pie Right.png')
            plt.close()

            plt.bar(category, [passed_left, failed_left])

            plt.ylabel(f'EOG {percentage_left:.2f}%')
            plt.title(f'EOG Left')
            
            plt.savefig(f'{dir}OUTPUT/EOG Left.png')
            plt.close()

            plt.pie([passed_left, failed_left])
            plt.ylabel(f'EOG {percentage_left:.2f}%')
            plt.title(f'EOG Left')
            
            plt.savefig(f'{dir}OUTPUT/EOG Pie Left.png')
            plt.close()

