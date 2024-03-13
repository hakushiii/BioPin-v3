from datetime import datetime, timedelta
import serial, csv, time
import eeg as eg

eeg = eg.Headwear('/dev/rfcomm1')

trial_count = 0
while True:
    trial_count += 1
    count = 0

    # Get the current time
    current_time = datetime.now()
    with open(f'EEG {current_time}.csv','w') as f:
        header = ['ITERATION','TIME','ATTENTION','MEDITATIOn','OUTPUT COMMAND']
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(header)

        data = []
        while True:
            count += 1

            if eeg.attention >= 70:
                direction = 'Forward'
            elif eeg.meditation >= 70:
                direction = 'Reverse'
            else:
                direction = 'Stop'
            
            data.append(count)
            data.append(str(datetime.now()))
            data.append(eeg.attention)
            data.append(eeg.meditation)
            data.append(direction)
            writer.writerow(data)
            print(data)
            time.sleep(1)
            data = []

            if datetime.now() >= current_time + timedelta(minutes=5):
                print("5 minutes have passed.")
                break
        f.close()