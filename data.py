import os
import pandas as pd
import matplotlib.pyplot as plt

path = r"Septentrio\RxTools\bin\bin2asc.exe"

def convert():

    for file in os.listdir('files/'):

        if file.endswith(".24_"):

            if os.path.isfile(f'files/{file}.measurements.txt'):
                
                None

            else:

                bin_file = f'files/{file}'

                os.system(f'{path} -f {bin_file} -i 1 -E --extractGenMeas')

                read(f'{bin_file}_measurements.txt')


def read(file):

    column_names=['1','2','3','4','5','6','7','8','9','10']

    for chunk in pd.read_csv(f'{file}',chunksize=chunk_size, names=column_names):

        full_data = []

        chunk_size = 1000

        full_data.append(chunk)

        df = pd.concat(full_data)
    
    return df


def clear():

    for file in os.listdir('files/'):

        if file.endswith("txt"):

            os.remove(f'files/{file}')

x=convert()
#clear()
gps1 = x[x['3']=='G01']

gps1l1=gps1[gps1['4'].str.contains('L1')]

plt.plot(gps1l1['1'],gps1l1['9'])
plt.show()


