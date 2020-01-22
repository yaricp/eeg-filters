#!/usr/bin/env python3

from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtWidgets import *
import sys
import pyqtgraph as pg
import numpy as np
from scipy.signal import butter, lfilter, freqz

from settings import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('pyqtgraph.ui', self)
        self.filepath = filepath
        self.dict_bandwidth_data = {}
        self.__start_calc()
        self.graph = pg.GraphicsLayoutWidget(parent=self)
        self.make_graphics('[1, 100]')
        self.grid.addWidget(self.graph, 0, 0)
        
        
    def prepare_data_from_file(self):
        '''function get rows from input file and append data to dictionary of data'''
        #dict_curves = {}
        list_times = []
        position = ''
        tmp_count = 0
        target_list = []
        with open(self.filepath,'r') as file:
            for row in file.readlines():
                if row.find('Sampling rate: ') != -1:
                    simple_rate = float(row.split('Sampling rate: ')[1].replace('Hz',''))
                    continue
                elif row.find('Measure times:') !=-1:
                    position = 'times'
                    tmp_count = 0
                    continue
                elif row.find('Data:') !=-1:
                    position = 'curves'
                    tmp_count = 0
                    continue
                elif position == '':
                    continue
                elif tmp_count == 0:
                   tmp_count += 1
                   continue
                if position == 'times':
                    list_times = [row.split('   ')[i].replace(' ','') for i in range(1,len(row.split('   '))-1)]
                    tmp_count = 0
                else:
                    target_list = self.append_data_to_list(target_list,row)
                    
        list_out = np.array(target_list).transpose()
        #print(list_out)
                    
        return simple_rate, list_times, list_out


    def append_data_to_list(self, target_list,row):
        ''' Append data from row of file to dict of data'''
        row = row.replace('\n','')
        row_splitted = row.split(':')[1].split('   ')
        rowlist = []
        for i in range(1,len(row_splitted)):
            value = float(row_splitted[i].replace(' ',''))
            rowlist.append(value)
        target_list.append(rowlist)
        return target_list
        
    def butter_filter(self, data, cutoff, fs, btype, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype=btype, analog=False)
        y = lfilter(b, a, data)
        return y

    def make_filter(self, row, bandwidth, fs):
        data  = np.array(row)
        cutted_low_data = self.butter_filter(data, bandwidth[1], fs, 'low', ORDER)
        cutted_high_data = self.butter_filter(cutted_low_data, bandwidth[0], fs, 'high', ORDER)
        filtred_data = cutted_high_data
        return filtred_data
    
    def search_max_min(self, list_ticks, data):
        search_slice = data[START_SEARCH:END_SEARCH]
        local_max = np.amax(search_slice)
        local_min = np.amin(search_slice)
        time_max = np.where(search_slice == np.amax(search_slice))[0][0]
        time_min = np.where(search_slice == np.amin(search_slice))[0][0]
        return {'max':(list_ticks[START_SEARCH+time_max], local_max), 
                'min':(list_ticks[START_SEARCH+time_min], local_min)}
                
    def make_graphics(self, bandwidth):
        iter = 0
        last_max_value = 0
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        plt = self.graph.addPlot()
        for time_stamp, row in dict_data.items():
            ext_dict = row['ext']
            iter -= ITER + last_max_value
            y = row['data'] + iter
            plt.plot(y,symbolPen='w')
            last_max_value = max(row['data'])
            
    def create_head_output_file(self, bandwidth):
        '''create header of output files'''
        with open(filepath,'r') as file:
            textfile = file.read()
            header = textfile.split('Data:')[0]+'\n Data: \n'
            #sys.exit(0)
            with open('output/filter%s.dat' % bandwidth,'a') as outfile:
                outfile.write(header)


    def write_out_data(self, bandwidth, out_dict):
        '''
        Write data to putput
        '''
        
        #print(out_dict)
        with open('output/filter%s.dat' % bandwidth,'a') as outfile:
            for i in range(1, len(out_dict)+1):
                outfile.write('     '+str(i))
            outfile.write('\n')
            for row in range(0,3000):
                outfile.write('   %s:   ' % str(row+1))
                for col in range(0, len(out_dict)):
                    outfile.write('%s    '% out_dict[col][row])
                outfile.write('\n')

        
    def __start_calc(self):
        fs, list_times, list_data = self.prepare_data_from_file()
        T = TIME_GAUGING
        n = int(T * fs)     # total number of samples
        t = np.linspace(0, T, n, endpoint=False)    #tick of measuring
        
        for bandwidth in BANDWIDTHS:
            self.create_head_output_file(bandwidth)
            dict_curves_filtred = {}
            for key_curv, row in zip (list_times, list_data):
                filtred_data = self.make_filter(row, bandwidth, fs)
                ext_dict = self.search_max_min(t, filtred_data)
                dict_curves_filtred.update({key_curv:{'data':filtred_data, 
                                                        'ext': ext_dict, 
                                                    }
                                            })
            self.dict_bandwidth_data.update({'%s' % bandwidth:dict_curves_filtred})


if __name__=='__main__':
    from sys import argv,exit
    app = QApplication(argv)
    win = MyWindow()
    win.show()
    exit(app.exec_())
