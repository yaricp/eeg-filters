#!/usr/bin/env python3

import pyqtgraph as pg

from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, 
                            QTextEdit,
                            QAction, 
                            QFileDialog, 
                            QApplication)

from eeg_filters.upload import prepare_data
from eeg_filters.filters import make_filter, search_max_min, get_tick_times
from eeg_filters.export import create_head_output_file
from settings import *


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('pyqtgraph.ui', self)
        self.source_filepath = SOURCE_FILEPATH
        self.target_filepath = TARGET_FILEPATH
        self.time_measuring = TIME_MEASUGING
        self.order = ORDER
        self.start_search = START_SEARCH
        self.end_search = END_SEARCH
        self.dict_bandwidth_data = {}
        self.__start_calc()
        #self.graph = pg.GraphicsLayoutWidget(parent=self)
        #self.make_graphics('[1, 100]')
        #self.grid.addWidget(self.graph, 0, 0)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        
    def make_graphics(self, bandwidth):
        iter = 0
        last_max_value = 0
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        plt = self.graph.addPlot()
        for time_stamp, row in dict_data.items():
            ext_dict = row['ext']
            iter -= ITER_VALUE + last_max_value
            y = row['data'] + iter
            plt.plot(y,symbolPen='w')
            last_max_value = max(row['data'])
            
        
    def __start_calc(self):
        fs, list_times, list_data = prepare_data(self.source_filepath)
        tick_times = get_tick_times(fs, self.time_measuring)
        
        for bandwidth in BANDWIDTHS:
            create_head_output_file(self.source_filepath, self.target_filepath, bandwidth)
            dict_curves_filtred = {}
            for key_curv, row in zip (list_times, list_data):
                filtred_data = make_filter(row, bandwidth, fs, self.order)
                ext_dict = search_max_min(
                                        tick_times, 
                                        filtred_data, 
                                        (self.start_search, self.end_search))
                dict_curves_filtred.update({key_curv:{'data':filtred_data, 
                                                        'ext': ext_dict, 
                                                    }
                                            })
            self.dict_bandwidth_data.update({'%s' % bandwidth:dict_curves_filtred})

    def showDialog(self):

        self.source_filepath = QFileDialog.getOpenFileName(
                                                    self, 
                                                    'Open file', 
                                                    './')[0]
        self.dict_bandwidth_data = {}
        self.__start_calc()
        print(self.dict_bandwidth_data)


if __name__=='__main__':
    from sys import argv,exit
    app = QApplication(argv)
    win = MyWindow()
    win.show()
    exit(app.exec_())
