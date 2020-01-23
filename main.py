#!/usr/bin/env python3

import pyqtgraph as pg

from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, 
                            QTextEdit,
                            QAction, 
                            QFileDialog, 
                            QApplication)
                            
import ui

from eeg_filters.upload import prepare_data
from eeg_filters.filters import make_filter, search_max_min, get_tick_times
from eeg_filters.export import create_head_output_file
from settings import *


class MyWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #uic.loadUi('pyqtgraph.ui', self)
        self.source_filepath = SOURCE_FILEPATH
        self.target_filepath = TARGET_FILEPATH
        self.time_measuring = TIME_MEASUGING
        self.order = ORDER
        self.start_search = START_SEARCH
        self.end_search = END_SEARCH
        self.bandwidths = BANDWIDTHS
        self.dict_bandwidth_data = {}
        
        self.fs, self.list_times, self.list_data = prepare_data(self.source_filepath)
        self.tick_times = get_tick_times(self.fs, self.time_measuring)
        #self.comboBox.addItems(['%s'%b for b in self.bandwidths])
        #self.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.listWidget.addItems(['%s'%b for b in self.bandwidths])
        self.listWidget.currentItemChanged.connect(self.selectionchange)
        
        self.__start_calc()
        #self.graph = pg.GraphicsLayoutWidget(self.graphicsView)
        self.graph = pg.PlotWidget(self.graphicsView)
        self.graph.setGeometry(QtCore.QRect(20, 40, 480, 380))
        self.graph.setBackground('w')
        #print(dir(self.graph))
        #parent=self.graphicsView
        self.show_graphic('[1, 100]')
        #self.grid.addWidget(self.graph, 0, 0)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        self.pushButton_2.clicked.connect(self.start_search_ext)
        
        

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        
    def selectionchange(self,i):
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.show_graphic(bandwidth)
        print('hsghjsfghjsdf')
        
    def start_search_ext(self):
        print('fghqweqwe')
        return 'ok'
        
    def show_graphic(self, bandwidth):
        iter = 0
        last_max_value = 0
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        #plt = self.graph.addPlot()
        for time_stamp, row in dict_data.items():
            ext_dict = row['ext']
            iter -= ITER_VALUE + last_max_value
            y = row['data'] + iter
            self.graph.plot(self.tick_times,  y)
            #plt.plot(y,symbolPen='w')
            last_max_value = max(row['data'])
            
        
    def __start_calc(self):
        
        for bandwidth in BANDWIDTHS:
            create_head_output_file(self.source_filepath, self.target_filepath, bandwidth)
            dict_curves_filtred = {}
            for key_curv, row in zip (self.list_times, self.list_data):
                filtred_data = make_filter(row, bandwidth, self.fs, self.order)
                ext_dict = search_max_min(
                                        self.tick_times, 
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
                                                    'Open ource sfile', 
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
