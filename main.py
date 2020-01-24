#!/usr/bin/env python3

import time, datetime
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
        
        self.progressBar.setMaximum(100)
#        self.progressBar.progressChanged.connect(progressBar.setValue, QtCore.Qt.QueuedConnection)
        self.listWidget.addItems(['%s'%b for b in self.bandwidths])
        self.listWidget.currentItemChanged.connect(self.show_graphic_filtered)
        
        self.graph = pg.PlotWidget(self.widget)
        self.graph.setGeometry(QtCore.QRect(0, 0, 830, 475))
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
        
        openFileButton = QAction(QIcon('open.png'), 'Open', self)
        openFileButton.setShortcut('Ctrl+O')
        openFileButton.setStatusTip('Open Source File')
        openFileButton.triggered.connect(self.showDialogOpen)
        
        saveFileButton = QAction(QIcon('save.png'), 'Save', self)
        saveFileButton.setShortcut('Ctrl+S')
        saveFileButton.setStatusTip('Save Filtered Data')
        saveFileButton.triggered.connect(self.showDialogSave)
        
        self.fileDialogOpen = QFileDialog()
        self.fileDialogOpen.setFileMode(1)
        self.fileDialogOpen.accepted.connect(self.prepare_data)
        
        self.fileDialogSave = QFileDialog()
        self.fileDialogSave.open(self.export_data)
        
        self.pushButton.clicked.connect(self.showDialogOpen)
        self.pushButton_2.clicked.connect(self.show_graphic_filtered)
        self.pushButton_3.clicked.connect(self.add_new_bandwidth)
        self.pushButton_4.clicked.connect(self.showDialogSave)
        self.pushButton_5.clicked.connect(self.show_graphic_source)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFileButton)
        fileMenu.addAction(saveFileButton)
        
    def show_graphic_filtered(self):
        #print('start show graphics filtered')
        if len(self.list_data) == 0:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        iter = 0
        last_max_value = 0
        self.progressBar.setProperty("visible", 1)
        self.progressBar.setValue(0)
        #print(self.dict_bandwidth_data.keys())
        #print(len(self.dict_bandwidth_data.keys()))
        if not '%s' % bandwidth in self.dict_bandwidth_data.keys():
            #print('new calculation')
            self.calc_add_bandwidth(bandwidth)
        #print('get dict_data')
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        #print('clear')
        self.graph.clear()
        self.dict_max_for_iter = {}
        #print('get count dict_data')
        total_count = len(dict_data)
        count = 0
        #print('show graphics')
        for time_stamp, row in dict_data.items():
            count += 1
            progress = count*25/total_count+25
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            iter -= ITER_VALUE + last_max_value
            y = row + iter
            self.graph.plot(self.tick_times,  y)
            #plt.plot(y,symbolPen='w')
            last_max_value = max(row)
            self.dict_max_for_iter.update({time_stamp:iter})
        self.show_graphic_extremums()
        #print(self.dict_bandwidth_data)
        
    def show_graphic_extremums(self):
        
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        iter_max = 0
        iter_min = 0
        if not '%s' % bandwidth in self.dict_extremums_data:
            self.calc_add_extremums(bandwidth)
        dict_data = self.dict_extremums_data['%s' % bandwidth]
        total_count = len(dict_data)
        count = 0
        for time_stamp, row in dict_data.items():
            count += 1
            progress = count*25/total_count+75
            self.progressBar.setValue(progress)
            QApplication.processEvents()
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
        self.graph.addItem(self.range_search_extremums)
        self.progressBar.setProperty("visible", 0)
        
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
            print(self.tick_times)
            self.graph.plot(self.tick_times,  y)
            last_max_value = max(row)
            
    def calc_add_extremums(self, bandwidth):
        
        where_find = self.range_search_extremums.getRegion()
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = {}
        count = 0
        total_count = len(dict_data)
        for time_stamp, row in dict_data.items():
            count += 1
            progress = count*25/total_count+50
            self.progressBar.setValue(progress)
            QApplication.processEvents()
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
        total_count = len(self.list_data)
        count = 0
        for key_curv, row in zip (self.list_times, self.list_data):
            count += 1
            progress = count*50/total_count
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            filtred_data = make_filter(row, bandwidth, self.fs, self.order)
            dict_curves_filtred.update({key_curv:filtred_data})
        self.dict_bandwidth_data.update({'%s' % bandwidth:dict_curves_filtred})
        #self.progressBar.setValue(0)
        #self.progressBar.setProperty("visible", 0)
        return True
        
    def add_new_bandwidth(self):
        text = self.lineEdit_3.text()
        self.listWidget.addItem(text)
        splitted_text = text.split(',')
        value =[
                int(splitted_text[0].replace('[', '')), 
                int(splitted_text[1].replace(']', '').replace(' ', ''))
                ] 
        self.bandwidths.append(value)
        self.lineEdit_3.clear()
        
    def showDialogOpen(self):

        self.source_filepath = self.fileDialogOpen.getOpenFileName(
                                                    self, 
                                                    'Open source file', 
                                                    './')[0]
        if not self.source_filepath:
            return False
        self.dict_bandwidth_data = {}
        #self.progress.setValue(self.completed)
        (self.fs, 
        self.list_times, 
        self.list_data) = prepare_data(self.source_filepath)
        self.tick_times = get_tick_times(self.fs, self.time_measuring)
        self.show_graphic_source()
        #print(self.dict_bandwidth_data)
        return self.source_filepath
        
    def prepare_data(self, filepath):
        print('loading data...')
        self.source_filepath = filepath
        self.fileDialogOpen.close()
        time.sleep(3)
        self.dict_bandwidth_data = {}
        #self.progress.setValue(self.completed)
        (self.fs, 
        self.list_times, 
        self.list_data) = prepare_data(self.source_filepath)
        self.tick_times = get_tick_times(self.fs, self.time_measuring)
        self.show_graphic_source()
        print(self.dict_bandwidth_data)
        
    def showDialogSave(self):

        filepath = self.fileDialogSave.getSaveFileName(
                                    self, 
                                    'Save filtered data', 
                                    './')[0]
        print(filepath)
    
    def export_data(self):
        
        pass
    

if __name__=='__main__':
    from sys import argv,exit
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
