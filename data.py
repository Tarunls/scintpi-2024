import os
import pandas as pd
import matplotlib.pyplot as plt
import time

# File path for bin2asc.exe
bin2asc_path = r"bin/sbf2asc/sbf2asc"

# Runs command to convert the binary to ascii and extract measurement.txt files. 
# Takes the file that you want to convert as a parameter

def svid_to_satellite(svid):
    if 1 <= svid <= 37:
        return f"G{str(svid).zfill(2)}"  # GPS
    elif 38 <= svid <= 61:
        return f"R{str(svid - 37).zfill(2)}"  # GLONASS with offset 37
    elif svid == 62:
        return "NA"  # GLONASS with unknown slot number
    elif 63 <= svid <= 68:
        return f"R{str(svid - 38).zfill(2)}"  # GLONASS with offset 38
    elif 71 <= svid <= 106:
        return f"E{str(svid - 70).zfill(2)}"  # GALILEO with offset 70
    elif 107 <= svid <= 119:
        return "NA"  # L-Band (MSS), no specific name given
    elif 120 <= svid <= 140:
        return f"S{str(svid - 100).zfill(2)}"  # SBAS with offset 100
    elif 141 <= svid <= 180:
        return f"C{str(svid - 140).zfill(2)}"  # BeiDou with offset 140
    elif 181 <= svid <= 187:
        return f"J{str(svid - 180).zfill(2)}"  # QZSS with offset 180
    elif 191 <= svid <= 197:
        return f"I{str(svid - 190).zfill(2)}"  # NavIC/IRNSS with offset 190
    elif 198 <= svid <= 215:
        return f"S{str(svid - 157).zfill(2)}"  # SBAS with offset 157
    elif 216 <= svid <= 222:
        return f"I{str(svid - 208).zfill(2)}"  # NavIC/IRNSS with offset 208
    elif 223 <= svid <= 245:
        return f"C{str(svid - 182).zfill(2)}"  # BeiDou with offset 182
    else:
        return "Unknown SVID"

def convert(bin_file):

    start = time.time()
    #os.system(f'cd {bin2asc_path}')
    os.system(f'{bin2asc_path} -f files/{bin_file} -m -o files/{bin_file[:-4]}')
    #os.system(f'{bin2asc_path} -f {bin_file} -m')
    print(f'Time taken is {time.time() - start}')
    

# Reads file and puts data into pandas dataframe.
def read(file):
    
    start = time.time()
    global df
    gps_epoch = pd.to_datetime('1980-01-06') #gps start time
    s4=pd.DataFrame()


   
    cols=[0,1,4] #columns of file we want
    names=['SVID','TOW','SNR']#dataframe namers
    rows=2 #in case of header skip some vals
    chunksize = 10 ** 7
    df=pd.DataFrame()
    buffer=pd.DataFrame()

    
    with pd.read_csv(file,header=None,delim_whitespace = True, skiprows=rows, usecols=cols, names=names, chunksize=chunksize) as reader:
        for chunk in reader:
            
            chunk['datetime'] = gps_epoch + pd.to_timedelta(chunk['TOW'], unit='s')
            chunk.set_index('datetime', inplace=True)
            chunk.sort_values(by='datetime')

            chunk['linSNR']= 10 ** (chunk['SNR'] / 10) #convert SNR from dB to linear
            chunk.drop(['TOW', 'SNR'],inplace=True,axis=1)    #remove fields we dont need anymore
            
            chunk=pd.concat([chunk,buffer])
            first_minute = chunk.index.floor('T').min() 
            last_minute = chunk.index.floor('T').max()
            buffer=chunk[((chunk.index.floor('T') == last_minute) | (chunk.index.floor('T') == first_minute))]
            
            chunk=chunk.groupby(['SVID']).resample('1min')
            
            
            
            
            s4=chunk['linSNR'].std()/chunk['linSNR'].mean() #calculate S4
            df = pd.concat([df, s4])
            
            print(f'Time taken is {time.time() - start}')
            start = time.time()
            
    df.reset_index(inplace=True)
    df[['Satellite', 'Datetime']] = df['index'].apply(pd.Series)
    df['S4']=df[0]
    df.set_index('Datetime',inplace=True)
    df.drop(['index',0],axis=1,inplace=True)
    
    df['Satellite'] = df['Satellite'].apply(svid_to_satellite)
        
    return df
# Function to delete all the .txt files at the end
def clear():

    for file in os.listdir('files/'):

        if file.endswith("txt"):

            os.remove(f'files/{file}')

# plots all .24_ binary files

convert('sept311v15.24_')

data = read('files/sept311v15')

data.to_csv(path_or_buf='test.csv')

'''
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
'''
