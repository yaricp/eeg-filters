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


class MainWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.source_filepath = ''   #SOURCE_FILEPATH
        self.target_filepath = ''   #TARGET_FILEPATH
        self.time_measuring = TIME_MEASUGING
        self.order = ORDER
        self.start_search = START_SEARCH
        self.end_search = END_SEARCH
        self.bandwidths = BANDWIDTHS
        self.dict_bandwidth_data = {}
        self.dict_extremums_data = {}
        self.dict_max_for_iter = {}
        
        self.fs = None
        self.list_times = []
        self.list_data = []
        self.tick_times = 0
        
        self.listWidget.addItems(['%s'%b for b in self.bandwidths])
        self.listWidget.currentItemChanged.connect(self.show_graphic_filtered)
        
        self.graph = pg.PlotWidget(self.widget)
        self.graph.setGeometry(QtCore.QRect(5, 5, 860, 460))
        self.graph.setBackground('w')
        self.range_search_extremums = pg.LinearRegionItem(
                [self.start_search, self.end_search])
        self.range_search_extremums.setBrush(
                QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
                )
        self.graph.addItem(self.range_search_extremums)
        self.range_search_extremums.sigRegionChangeFinished.connect(
                self.change_range_search_extremums
                )
        
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open Source File')
        openFile.triggered.connect(self.showDialogOpen)
        
        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save Filtered Data')
        saveFile.triggered.connect(self.showDialogSave)
        
        self.pushButton.clicked.connect(self.showDialogOpen)
        self.pushButton_2.clicked.connect(self.show_graphic_filtered)
        self.pushButton_3.clicked.connect(self.add_new_bandwidth)
        self.pushButton_4.clicked.connect(self.showDialogSave)
        self.pushButton_5.clicked.connect(self.show_graphic_source)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)  
        
    def show_graphic_filtered(self):
        
        if len(self.list_data) == 0:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        iter = 0
        last_max_value = 0
        if not '%s' % bandwidth in self.dict_bandwidth_data:
            self.calc_add_bandwidth(bandwidth)
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        self.graph.clear()
        self.dict_max_for_iter = {}
        for time_stamp, row in dict_data.items():
            iter -= ITER_VALUE + last_max_value
            y = row + iter
            self.graph.plot(self.tick_times,  y)
            #plt.plot(y,symbolPen='w')
            last_max_value = max(row)
            self.dict_max_for_iter.update({time_stamp:iter})
        self.show_graphic_extremums()
        print(self.dict_bandwidth_data)
        
    def show_graphic_extremums(self):
        
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        iter_max = 0
        iter_min = 0
        if not '%s' % bandwidth in self.dict_extremums_data:
            self.calc_add_extremums(bandwidth)
        dict_data = self.dict_extremums_data['%s' % bandwidth]
        for time_stamp, row in dict_data.items():
            iter_max = self.dict_max_for_iter[time_stamp]
            iter_min = self.dict_max_for_iter[time_stamp]
            max_x = row['max'][0]
            max_y = row['max'][1] + iter_max
            min_x = row['min'][0]
            min_y = row['min'][0] + iter_min
            pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
            self.graph.plot([max_x, ],[max_y, ], symbol='o', pen=pen, 
                    symbolSize=5, symbolBrush=('r'))
            self.graph.plot([min_x,], [min_y,],  symbol='o', pen=pen, 
                    symbolSize=5, symbolBrush=('b'))
            #plt.plot(y,symbolPen='w')
            
        self.graph.addItem(self.range_search_extremums)
        
    def change_range_search_extremums(self):
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.calc_add_extremums(bandwidth)
        self.show_graphic_extremums()
        
    def show_graphic_source(self):
        iter = 0
        last_max_value = 0
        self.graph.clear()
        for key_curv, row in zip (self.list_times, self.list_data):
            iter -= ITER_VALUE + last_max_value
            y = row + iter
            self.graph.plot(self.tick_times,  y)
            last_max_value = max(row)
            
    def calc_add_extremums(self, bandwidth):
        where_find = self.range_search_extremums.getRegion()
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = {}
        for time_stamp, row in dict_data.items():
            dict_extremums.update({
                time_stamp: search_max_min(
                        self.tick_times, 
                        row, 
                        where_find
                        )
                })
        self.dict_extremums_data.update({'%s' % bandwidth:dict_extremums})
        return True
        
        
    def calc_add_bandwidth(self, bandwidth):
        
        dict_curves_filtred = {}
        for key_curv, row in zip (self.list_times, self.list_data):
            filtred_data = make_filter(row, bandwidth, self.fs, self.order)
            dict_curves_filtred.update({key_curv:filtred_data})
        self.dict_bandwidth_data.update({'%s' % bandwidth:dict_curves_filtred})
        return True
        
    def add_new_bandwidth(self):
        text = self.lineEdit_3.text()
        self.listWidget.addItem(text)
        splitted_text = text.split(',').replace('[', '').replace(']', '').replace(' ', '')
        value =[int(splitted_text)[0], int(splitted_text)[1]] 
        self.bandwidths.append(value)
        

    def showDialogOpen(self):

        self.source_filepath = QFileDialog.getOpenFileName(
                                                    self, 
                                                    'Open source file', 
                                                    './')[0]
        
        self.dict_bandwidth_data = {}
        (self.fs, 
        self.list_times, 
        self.list_data) = prepare_data(self.source_filepath)
        self.tick_times = get_tick_times(self.fs, self.time_measuring)
        self.show_graphic_source()
        print(self.dict_bandwidth_data)
        
    def showDialogSave(self):

        filepath = QFileDialog.getSaveFileName(
                                    self, 
                                    'Save filtered data', 
                                    './')[0]
        print(filepath)


if __name__=='__main__':
    from sys import argv,exit
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
