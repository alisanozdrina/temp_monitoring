# usage: on cobalt execute 
# $python makeReport.py STATION1B 7 
# to get ara1 data for the last 7 days and
# $python makeReport.py STATION3 7
# for ara3

import os
import sys
import time
import json
import gzip
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_pdf import PdfPages

stationNum = sys.argv[1]

data_folder = '/data/exp/ARA/2013/monitoring/aware/output/' + str(stationNum) +'/2022/'
DaysOld = float(sys.argv[2])

print('data_folder:', data_folder)

def getList_of_Filtred_runs(DaysOld, data_folder):

    olderThanDays = DaysOld
    olderThanDays *= 86400
    present = time.time()
    filtred_data_list = []

    for subdir, dirs, files in os.walk(data_folder):
        #files.sort(key=os.path.getctime)
        for files in files:
            if (str(files) == 'headerTime.json.gz' ): 
                root_file_name = str(subdir)+ '/' + str(files)
                if (present - os.path.getmtime(root_file_name)) < olderThanDays:
                    filtred_data_list.append(root_file_name)
                    print(str(subdir[:]) + '/' + str(files), ' has been found' )
    return filtred_data_list


file_list = getList_of_Filtred_runs(7, data_folder)
file_list.sort()
with PdfPages('ev_rates.pdf') as pdf:

    for pathToFile in file_list:
        print('processing:', pathToFile)

        with gzip.open(pathToFile, "rb") as f:
            d = json.loads(f.read().decode('UTF-8'))

            runnumber = str(d['timeSum']['run'])
            instrument = str(d['timeSum']['instrument'])

            timeStamps = np.zeros(len(d['timeSum']['timeList']))

            for t in range(0, len(d['timeSum']['timeList'])):
                timeStamps[t] = d['timeSum']['timeList'][t]['startTime']

            duration = str( (timeStamps[len(d['timeSum']['timeList'])-1] - timeStamps[0]) / 60 ) 

            dataTime = [datetime.fromtimestamp(t) for t in timeStamps]

            calEventRate = np.zeros(len(d['timeSum']['varList'][0]['timeList']))
            eventRate = np.zeros(len(d['timeSum']['varList'][1]['timeList']))
            rfEventRate = np.zeros(len(d['timeSum']['varList'][4]['timeList']))
            sfEventRate = np.zeros(len(d['timeSum']['varList'][25]['timeList']))

            for i in range(0, len(d['timeSum']['varList'][0]['timeList'])):
                calEventRate[i] = d['timeSum']['varList'][0]['timeList'][i]['mean']
                eventRate[i] = d['timeSum']['varList'][1]['timeList'][i]['mean']
                rfEventRate[i] = d['timeSum']['varList'][4]['timeList'][i]['mean']
                sfEventRate[i] = d['timeSum']['varList'][25]['timeList'][i]['mean']


            plt.rcParams["figure.figsize"] = (20,8)

            myFmt = DateFormatter("%b-%d %H:%M")
            fig, ax = plt.subplots()
            ax.plot(dataTime, calEventRate, label = 'cal pulser event rate')
            ax.plot(dataTime, eventRate, label = 'total event rate')
            ax.plot(dataTime, rfEventRate, label = 'RF trigger event rate')
            ax.plot(dataTime, sfEventRate, label = 'Software trigger event rate')


            ax.xaxis.set_major_formatter(myFmt)
            fig.autofmt_xdate()
            plt.title(instrument + ' Run ' + runnumber + ' Duration ' + duration + ' Min',fontsize = 16)
            plt.ylabel('Rate, [Hz]',fontsize = 16)
            plt.yticks()
            plt.legend(fontsize = 16)
            #plt.show()
            
            pdf.savefig(fig)
            plt.close()

            d = pdf.infodict()
            d['Title'] = 'station 1, filtred data from the south for the last 7 days' 
            d['Author'] = 'Alisa Nozdrina, KU'
            d['CreationDate'] = datetime.fromtimestamp( time.time() )

print('ev_rates.pdf', 'has been created')