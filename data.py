import os
import pandas as pd
import matplotlib.pyplot as plt

# File path for bin2asc.exe
bin2asc_path = r"Septentrio\RxTools\bin\bin2asc.exe"

# Runs command to convert the binary to ascii and extract measurement.txt files. 
# Takes the file that you want to convert as a parameter
def convert(bin_file):

    os.system(f'{bin2asc_path} -f {bin_file} -i 1 -E --extractGenMeas')

# Reads file and puts data into pandas dataframe.
def read(measurement_file):

    # Lines to parse at a time
    chunk_size = 1000

    # List that will have data added to it
    full_data = []

    # Placeholder column names
    column_names=['1','2','3','4','5','6','7','8','9','10']

    # Goes through data in the csv file, and ads it to the list chunk by chunk
    for chunk in pd.read_csv(measurement_file,chunksize=chunk_size, names=column_names):

        full_data.append(chunk)

    # Concatenates final values into the dataframe
    df = pd.concat(full_data)

    # Returns dataframe for later use
    return df

# Function to delete all the .txt files at the end
def clear():

    for file in os.listdir('files/'):

        if file.endswith("txt"):

            os.remove(f'files/{file}')

# plots all .24_ binary files
def plot_all():

    for file in os.listdir('files/'):

            if file.endswith(".24_"):
                
                current_file = f'files/{file}'
                measurement_file = f'{current_file}_measurements.txt'

                convert(current_file)
                x = read(measurement_file)

                print(x)

                gps1 = x[x['3']=='G01']

                # List of the types of GPS Frequencies
                type_list = ['L1','L2','L5']

                # Creates 3 subplots
                fig, ax = plt.subplots(3)

                for i in range(len(type_list)):

                    plotter=gps1[gps1['4'].str.contains(type_list[i])]

                    ax[i].plot(plotter['1'],plotter['9'],label=f'GPS {type_list[i]}')

                    ax[i].legend(loc=1)

                plt.show()

                clear()

plot_all()
