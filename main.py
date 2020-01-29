#!/usr/bin/env python3

import time, datetime
import pyqtgraph as pg

from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, 
                            QTextEdit,
                            QAction, 
                            QFileDialog, 
                            QApplication,
                            QAbstractItemView
                            )
                            
import ui

from eeg_filters.upload import prepare_data
from eeg_filters.filters import make_filter, search_max_min, get_tick_times
from eeg_filters.export import create_head_output_file, write_out_data
from settings import *


class MainWindow(QMainWindow, ui.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.time_measuring = TIME_MEASUGING
        self.order = ORDER
        self.start_search = START_SEARCH
        self.end_search = END_SEARCH
        self.bandwidths = BANDWIDTHS
        self.iter_value = ITER_VALUE
        self.max_iter_value = MAX_ITER_VALUE
        
        self.source_filepath = ''
        self.target_dirpath = ''
        self.dict_bandwidth_data = {}
        self.dict_extremums_data = {}
        self.dict_max_for_iter = {}
        self.dict_showed_extremums = {}
        self.total_count = 0
        self.fs = None
        self.list_times = []
        self.list_data = []
        self.tick_times = 0
        
        self.lineEdit_1.setText(str(self.start_search))
        self.lineEdit_2.setText(str(self.end_search))
        self.progressBar.setMaximum(100)
#        self.progressBar.progressChanged.connect(progressBar.setValue, QtCore.Qt.QueuedConnection)
        self.listWidget.addItems(['%s'%b for b in self.bandwidths])
        self.listWidget.itemSelectionChanged.connect(self.show_graphic_filtered)
        
        self.graph = pg.PlotWidget(self.widget)
        self.graph.setGeometry(QtCore.QRect(0, 0, 830, 475))
        self.graph.setBackground('w')
        self.range_search_extremums = pg.LinearRegionItem(
                [self.start_search, self.end_search])
        self.range_search_extremums.setBrush(
                QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
                )
        #self.graph.addItem(self.range_search_extremums)
        self.range_search_extremums.sigRegionChangeFinished.connect(
                self.change_range_search_extremums
                )
        
        openFileButton = QAction(QIcon('open.png'), 'Open', self)
        openFileButton.setShortcut('Ctrl+O')
        openFileButton.setStatusTip('Open Source File')
        openFileButton.triggered.connect(self.show_dialog_open)
        
        saveFileButton = QAction(QIcon('save.png'), 'Save', self)
        saveFileButton.setShortcut('Ctrl+S')
        saveFileButton.setStatusTip('Save Filtered Data')
        saveFileButton.triggered.connect(self.save_button_pressed)
        
        self.lineEdit_1.returnPressed.connect(
                self.change_text_line_edits
                )
        self.lineEdit_2.returnPressed.connect(
                self.change_text_line_edits
                )
        
        self.fileDialogOpen = QFileDialog()
        self.fileDialogOpen.setFileMode(0)
        
        self.fileDialogSave = QFileDialog()
        self.fileDialogSave.setFileMode(4)
        
        self.pushButton.clicked.connect(self.show_dialog_open)
        self.pushButton_2.clicked.connect(self.show_graphic_filtered)
        self.pushButton_3.clicked.connect(self.add_new_bandwidth)
        self.pushButton_4.clicked.connect(self.save_button_pressed)
        self.pushButton_5.clicked.connect(self.show_graphic_source)
        
        self.slider1.valueChanged.connect(self.change_value_slider)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFileButton)
        fileMenu.addAction(saveFileButton)
        
    def show_graphic_filtered(self):
        
        if self.total_count == 0:
            return False
        index = self.listWidget.currentRow()
        item = self.listWidget.currentItem()
        print(dir(item))
        for ind in range(0, self.listWidget.count()):
            self.listWidget.item(ind).setFlags(
                                    QtCore.Qt.NoItemFlags)
        QApplication.processEvents()
        bandwidth = self.bandwidths[index]
        print('before clear')
        #QApplication.processEvents()
        self.graph.clear()
        self.dict_max_for_iter = {}
        print('after clear')
        #QApplication.processEvents()
        iter = 0
        last_max_value = 0
        self.progressBar.setProperty("visible", 1)
        self.progressBar.setValue(0)
        print('check if data ready')
        QApplication.processEvents()
        if not '%s' % bandwidth in self.dict_bandwidth_data.keys():
            print('calc new data')
            self.calc_add_bandwidth(bandwidth)
        print('get data')
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        count = 0
        print('befoer for')
        for time_stamp, row in dict_data.items():
            count += 1
            progress = count*25/self.total_count+25
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            iter -= self.iter_value + last_max_value
            y = row + iter
            self.graph.plot(self.tick_times,  y)
            last_max_value = max(row)
            self.dict_max_for_iter.update({time_stamp:iter})
        self.show_graphic_extremums()
        return True
        
    def show_graphic_extremums(self):
        
        if self.total_count == 0:
            return False
        index = self.listWidget.currentRow()
        print('INDEX:', index)
        bandwidth = self.bandwidths[index]
        iter_max = 0
        iter_min = 0
        self.range_search_extremums.setRegion([
                float(self.lineEdit_1.text()), 
                float(self.lineEdit_2.text())
                ])
        self.graph.addItem(self.range_search_extremums)
        if not '%s' % bandwidth in self.dict_extremums_data:
            self.calc_add_extremums(bandwidth)
        dict_data = self.dict_extremums_data['%s' % bandwidth]
        count = 0
        for time_stamp, row in dict_data.items():
            count += 1
            progress = count*25/self.total_count+75
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            iter_max = self.dict_max_for_iter[time_stamp]
            iter_min = self.dict_max_for_iter[time_stamp]
            max_x = row['max'][0]
            max_y = row['max'][1] + iter_max
            min_x = row['min'][0]
            min_y = row['min'][1] + iter_min
            pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
            showed_max = self.graph.plot([max_x, ],[max_y, ], symbol='o', pen=pen, 
                    symbolSize=5, symbolBrush=('r'))
            
            showed_min = self.graph.plot([min_x,], [min_y,],  symbol='o', pen=pen, 
                    symbolSize=5, symbolBrush=('b'))
            self.dict_showed_extremums.update({time_stamp:[showed_max, showed_min]})
        self.progressBar.setProperty("visible", 0)
        print('list: ', self.listWidget.count())
        for ind in range(0, self.listWidget.count()):
            item = self.listWidget.item(ind)
            self.listWidget.itemActivated(item)
#            self.listWidget.item(ind).setFlags(
#                                    QtCore.Qt.ItemIsEnabled)
#            self.listWidget.item(ind).setFlags(
#                                    QtCore.Qt.ItemIsSelectable)
#            self.listWidget.item(ind).setFlags(
#                                    QtCore.Qt.ItemIsUserCheckable)
        return True
        
    def change_text_line_edits(self):
        
        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.range_search_extremums.setRegion([
                float(self.lineEdit_1.text()), 
                float(self.lineEdit_2.text())
                ])
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.calc_add_extremums(bandwidth)
        dict_data = self.dict_extremums_data['%s' % bandwidth]
        for time_stamp, row in dict_data.items():
            iter_max = self.dict_max_for_iter[time_stamp]
            iter_min = self.dict_max_for_iter[time_stamp]
            max_x = row['max'][0]
            max_y = row['max'][1] + iter_max
            min_x = row['min'][0]
            min_y = row['min'][1] + iter_min
            showed_max = self.dict_showed_extremums[time_stamp][0]
            showed_max.setData([max_x, ], [max_y, ])
            showed_min = self.dict_showed_extremums[time_stamp][1]
            showed_min.setData([min_x, ], [min_y, ])
            self.dict_showed_extremums.update({time_stamp:[showed_max, showed_min]})
        return True
        
    def change_range_search_extremums(self):
        
        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.lineEdit_1.setText(
                str(round(self.range_search_extremums.getRegion()[0], 5))
                )
        self.lineEdit_2.setText(
                str(round(self.range_search_extremums.getRegion()[1], 5)))
        self.calc_add_extremums(bandwidth)
        dict_data = self.dict_extremums_data['%s' % bandwidth]
        for time_stamp, row in dict_data.items():
            iter_max = self.dict_max_for_iter[time_stamp]
            iter_min = self.dict_max_for_iter[time_stamp]
            max_x = row['max'][0]
            max_y = row['max'][1] + iter_max
            min_x = row['min'][0]
            min_y = row['min'][1] + iter_min
            showed_max = self.dict_showed_extremums[time_stamp][0]
            showed_max.setData([max_x, ], [max_y, ])
            showed_min = self.dict_showed_extremums[time_stamp][1]
            showed_min.setData([min_x, ], [min_y, ])
            self.dict_showed_extremums.update({time_stamp:[showed_max, showed_min]})
        return True
            
    def show_graphic_source(self):
        print(self.listWidget.currentRow())
        if self.total_count == 0:
            return False
        iter = 0
        last_max_value = 0
        self.graph.clear()
        for key_curv, row in zip (self.list_times, self.list_data):
            iter -= self.iter_value + last_max_value
            y = row + iter
            self.graph.plot(self.tick_times,  y)
            last_max_value = max(row)
            
    def calc_add_extremums(self, bandwidth):
        
        where_find = self.range_search_extremums.getRegion()
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = {}
        count = 0
        for time_stamp, row in dict_data.items():
            count += 1
            progress = count*25/self.total_count+50
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
        count = 0
        for key_curv, row in zip (self.list_times, self.list_data):
            count += 1
            progress = count*50/self.total_count
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            filtred_data = make_filter(row, bandwidth, self.fs, self.order)
            dict_curves_filtred.update({key_curv:filtred_data})
        self.dict_bandwidth_data.update({'%s' % bandwidth:dict_curves_filtred})
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
        
    def change_value_slider(self):
        
        self.iter_value = self.slider1.value()*self.max_iter_value/20
        QApplication.processEvents()
        self.show_graphic_filtered()
        return True 
        
    def show_dialog_open(self):

        self.source_filepath = self.fileDialogOpen.getOpenFileName(
                                                    self, 
                                                    'Open source file', 
                                                    './')[0]
        if not self.source_filepath:
            return False
        QApplication.processEvents()
        self.prepare_data()
        return self.source_filepath
        
    def prepare_data(self):
        
        print('loading data...')
        self.dict_bandwidth_data = {}
        #self.progress.setValue(self.completed)
        (self.fs, 
        self.list_times, 
        self.list_data) = prepare_data(self.source_filepath)
        self.tick_times = get_tick_times(self.fs, self.time_measuring)
        self.total_count = len(self.list_times)
        self.show_graphic_source()
        #print(self.dict_bandwidth_data)
        
    def save_button_pressed(self):
        
        if not self.target_dirpath:
            self.target_dirpath = self.fileDialogSave.getExistingDirectory(
                                    self, 
                                    'Save filtered data', 
                                    './')
        if not self.target_dirpath:
            return False
        QApplication.processEvents()
        self.export_data()
        return True
        
    def export_data(self):
        
        key, value = self.dict_bandwidth_data.popitem()
        key, rows = value.popitem()
        count_rows = len(rows)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        count = 0
        total_count = len(self.bandwidths)
        for bandwidth, dict_data in self.dict_bandwidth_data.items():
            count += 1
            progress = count*100/total_count
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            res = write_out_data(
                count_rows, 
                self.source_filepath, 
                self.target_dirpath, 
                bandwidth,
                dict_data)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        print('Files Saved')
    

if __name__=='__main__':
    from sys import argv,exit
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
