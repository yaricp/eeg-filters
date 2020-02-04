#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main file of QT GUI
"""

import pyqtgraph as pg

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
                            QMainWindow,
                            QAction,
                            QFileDialog,
                            QApplication
                            )

import ui

from eeg_filters.upload import prepare_data
from eeg_filters.filters import make_filter, search_max_min, get_tick_times
from eeg_filters.export import export_curves
from settings import *


class MainWindow(QMainWindow, ui.Ui_MainWindow):

    def __init__(self: dict) -> None:
        super().__init__()
        self.setupUi(self)

        self.time_measuring = TIME_MEASUGING
        self.order = ORDER
        self.max_start_search = MAX_START_SEARCH
        self.max_end_search = MAX_END_SEARCH
        self.min_start_search = MIN_START_SEARCH
        self.min_end_search = MIN_END_SEARCH
        self.bandwidths = BANDWIDTHS
        self.max_iter_value = MAX_ITER_VALUE
        self.max_step_iter = MAX_STEP_ITER
        self.default_step_iter = DEFAULT_STEP_ITER
        self.iter_value = (
                            MAX_ITER_VALUE
                            *DEFAULT_STEP_ITER
                            /MAX_STEP_ITER
                            )

        self.source_filepath = ''
        self.target_dirpath = ''
        self.dict_bandwidth_data = {}
        self.dict_extremums_data = {}
#        self.dict_max_for_iter = {}
        self.dict_showed_extremums = {}
        self.total_count = 0
        self.fs = None
        self.list_times = []
        self.list_data = []
        self.tick_times = 0

        self.lineEditMaxStart.setText(str(self.max_start_search))
        self.lineEditMaxEnd.setText(str(self.max_end_search))
        self.lineEditMinStart.setText(str(self.min_start_search))
        self.lineEditMinEnd.setText(str(self.min_end_search))
        self.lineEditMaxStart.returnPressed.connect(
                self.change_text_line_max_edits
                )
        self.lineEditMaxEnd.returnPressed.connect(
                self.change_text_line_max_edits
                )
        self.lineEditMinStart.returnPressed.connect(
                self.change_text_line_min_edits
                )
        self.lineEditMinEnd.returnPressed.connect(
                self.change_text_line_min_edits
                )
        
        self.progressBar.setMaximum(100)

        self.listWidget.addItems(['%s' % b for b in self.bandwidths])
        self.listWidget.itemClicked.connect(self.list_item_activated)

        self.graph = pg.PlotWidget(self.widget)
        self.graph.setGeometry(QtCore.QRect(0, 0, 830, 475))
        self.graph.setBackground('w')
        
        self.range_search_maxmums = pg.LinearRegionItem(
                [self.max_start_search, self.max_end_search])
        self.range_search_maxmums.setBrush(
                QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
                )
        self.range_search_maxmums.sigRegionChangeFinished.connect(
                self.change_range_search_maxmums
                )
                
        self.range_search_minimums = pg.LinearRegionItem(
                [self.min_start_search, self.min_end_search])
        self.range_search_minimums.setBrush(
                QtGui.QBrush(QtGui.QColor(0, 0, 50, 50))
                )
        self.range_search_minimums.sigRegionChangeFinished.connect(
                self.change_range_search_minimums
                )
                
        openFileButton = QAction(QIcon('open.png'), 'Open', self)
        openFileButton.setShortcut('Ctrl+O')
        openFileButton.setStatusTip('Open Source File')
        openFileButton.triggered.connect(self.show_dialog_open)

        saveFileButton = QAction(QIcon('save.png'), 'Save', self)
        saveFileButton.setShortcut('Ctrl+S')
        saveFileButton.setStatusTip('Save Filtered Data')
        saveFileButton.triggered.connect(self.save_button_pressed)

        closeFileButton = QAction(QIcon('close.png'), 'Close', self)
        closeFileButton.setShortcut('Ctrl+X')
        closeFileButton.setStatusTip('Close')
        closeFileButton.triggered.connect(self.close_button_pressed)

        self.fileDialogOpen = QFileDialog()
        self.fileDialogOpen.setFileMode(0)
        self.fileDialogSave = QFileDialog()
        self.fileDialogSave.setFileMode(4)

        self.pushButton.clicked.connect(self.show_dialog_open)
        self.pushButton_3.clicked.connect(self.add_new_bandwidth)
        self.pushButton_4.clicked.connect(self.save_button_pressed)
        
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(self.max_step_iter)
        self.slider1.setValue(self.default_step_iter)
        self.slider1.valueChanged.connect(self.change_value_slider)
        

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFileButton)
        fileMenu.addAction(saveFileButton)
        fileMenu.addAction(closeFileButton)

    def list_item_activated(self: dict, item: dict) -> bool:

        if item.text() == 'source' and not self.source_filepath:
            self.show_dialog_open()
            return True
        self.show_graphic_filtered()
        return True

    def show_graphic_filtered(self: dict) -> bool:

        if self.total_count == 0:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.dict_max_for_iter = {}
        if not '%s' % bandwidth in self.dict_bandwidth_data.keys():
            self.calc_add_bandwidth(bandwidth)
        delta = 0
#        last_max_value = 0
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        count = 0
        for time_stamp, row in dict_data.items():
            delta -= self.iter_value 	#+ last_max_value
            y = row + delta
            graph_item = self.graph.getPlotItem().dataItems[count]
            graph_item.setData(self.tick_times,  y,)
#            last_max_value = max(row)
#            self.dict_max_for_iter.update({time_stamp: delta})
            count += 1
        self.show_graphic_extremums()
        return True
        
    def show_graphic_extremums(self: dict) -> bool:
        
        print('start show extremums')
        if self.total_count == 0:
            return False
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
#        iter_max = 0
#        iter_min = 0
        self.range_search_maxmums.setRegion([
                float(self.lineEditMaxStart.text()),
                float(self.lineEditMaxEnd.text())
                ])
        self.range_search_minimums.setRegion([
                float(self.lineEditMinStart.text()),
                float(self.lineEditMinEnd.text())
                ])
        if not '%s' % bandwidth in self.dict_extremums_data:
            self.calc_add_extremums(bandwidth, 'max')
            self.calc_add_extremums(bandwidth, 'min')
        self.graph.addItem(self.range_search_maxmums)
        self.reshow_extremums('max')
        self.graph.addItem(self.range_search_minimums)
        self.reshow_extremums('min')
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        return True

    def change_text_line_max_edits(self: dict) -> bool:

        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.dict_extremums_data = {}
        self.range_search_maxmums.setRegion([
                float(self.lineEditMaxStart.text()),
                float(self.lineEditMaxEnd.text())
                ])
        self.reshow_extremums('max')
        return True
        
    def change_text_line_min_edits(self: dict) -> bool:

        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.dict_extremums_data = {}
        self.range_search_minimums.setRegion([
                float(self.lineEditMinStart.text()),
                float(self.lineEditMinEnd.text())
                ])
        self.reshow_extremums('min')
        return True

    def change_range_search_maxmums(self: dict) -> bool:

        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.dict_extremums_data = {}
        self.lineEditMaxStart.setText(
                str(round(self.range_search_maxmums.getRegion()[0], 5))
                )
        self.lineEditMaxEnd.setText(
                str(round(self.range_search_maxmums.getRegion()[1], 5)))
        self.reshow_extremums('max')
        return True
        
    def change_range_search_minimums(self: dict) -> bool:

        if self.total_count == 0 or not self.dict_showed_extremums:
            return False
        self.dict_extremums_data = {}
        self.lineEditMinStart.setText(
                str(round(self.range_search_minimums.getRegion()[0], 5))
                )
        self.lineEditMinEnd.setText(
                str(round(self.range_search_minimums.getRegion()[1], 5)))
        self.reshow_extremums('min')
        return True
        
    def reshow_extremums(self, ext):
        
        delta = 0
        index = self.listWidget.currentRow()
        bandwidth = self.bandwidths[index]
        self.calc_add_extremums(bandwidth, ext)
        dict_data = self.dict_extremums_data[ext]['%s' % bandwidth]
        showed_extremums = self.dict_showed_extremums[ext]
        for time_stamp, row in dict_data.items():
            delta -= self.iter_value 	#+ last_max_value
            time_extremum = row[0]
            value_extremum = row[1] + delta
            showed_extremum = showed_extremums[time_stamp]
            showed_extremum.setData([time_extremum, ], [value_extremum, ])
            showed_extremums.update({
                    ext:{time_stamp: showed_extremum}
                    })
        return True

    def calc_add_extremums(
                            self: dict,
                            bandwidth: list,
                            ext: str
                            ) -> bool:
        range_search = self.range_search_maxmums
        if ext == 'min':
            range_search = self.range_search_minimums
        where_find = range_search.getRegion()
        #print("Where:", where_find)
        dict_data = self.dict_bandwidth_data['%s' % bandwidth]
        dict_extremums = {}
#        count = 0
        for time_stamp, row in dict_data.items():
#            count += 1
#            progress = count*50/self.total_count+50
#            self.progressBar.setValue(progress)
#            QApplication.processEvents()
            dict_extremums.update({
                time_stamp: search_max_min(
                        self.tick_times,
                        row,
                        where_find, 
                        ext
                        )
                })
        self.dict_extremums_data.update({ext:{'%s' % bandwidth: dict_extremums}})
        return True

    def calc_add_bandwidth(self: dict, bandwidth: list) -> bool:

        dict_curves_filtred = {}
        for key_curv, row in zip(self.list_times, self.list_data):
            filtred_data = make_filter(row, bandwidth, self.fs, self.order)
            dict_curves_filtred.update({key_curv: filtred_data})
        self.dict_bandwidth_data.update({
                '%s' % bandwidth: dict_curves_filtred
                })
        return True

    def add_new_bandwidth(self: dict) -> None:

        text = self.lineEdit_3.text()
        self.listWidget.addItem(text)
        splitted_text = text.split(',')
        value = [
                int(splitted_text[0].replace('[', '')),
                int(splitted_text[1].replace(']', '').replace(' ', ''))
                ]
        self.bandwidths.append(value)
        self.lineEdit_3.clear()

    def change_value_slider(self: dict) -> bool:

        self.iter_value = (self.slider1.value()
                *self.max_iter_value
                /self.max_step_iter
                )
        QApplication.processEvents()
        self.show_graphic_filtered()
        return True

    def show_dialog_open(self: dict) -> bool:

        self.source_filepath = self.fileDialogOpen.getOpenFileName(
                                                    self,
                                                    'Open source file',
                                                    './')[0]
        if not self.source_filepath:
            return False
        item = self.listWidget.item(0)
        item.setSelected(True)
        self.listWidget.setCurrentItem(item)
        self.prepare_data()
        return True

    def prepare_data(self: dict) -> bool:

        if not self.source_filepath:
            return False
#            print('loading data...')
        self.dict_bandwidth_data = {}
        self.dict_extremums_data = {}
#            self.dict_showed_extremums = {}
        (
            self.fs,
            self.list_times,
            self.list_data
        ) = prepare_data(self.source_filepath)
        self.tick_times = get_tick_times(self.fs, self.time_measuring)
        self.total_count = len(self.list_times)
        if self.total_count == 0:
            return False
        dict_curves_filtred = {}
        count = 0
        flag_new = False
        self.listWidget.setHidden(1)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        pen2 = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
        if not self.graph.getPlotItem().dataItems:
            flag_new = True
        for time_stamp, row in zip(self.list_times, self.list_data):
            count += 1
            progress = count*50/self.total_count
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            dict_curves_filtred.update({time_stamp: row})
            #  prepare graph
            if flag_new:
                self.graph.plot(
                        name=time_stamp
                        )
        if flag_new:
            maximums = {}
            minimums = {}
            for time_stamp in self.list_times:
                count += 1
                progress = count*50/self.total_count
                self.progressBar.setValue(progress)
                QApplication.processEvents()
                showed_max = self.graph.plot(
                        [0, 0],
                        [0, 0],
                        name='max_%s' % time_stamp,
                        symbol='o',
                        pen=pen2,
                        symbolSize=5,
                        symbolBrush=('r')
                        )
                showed_min = self.graph.plot(
                        [0, 0],
                        [0, 0],
                        name='min_%s' % time_stamp,
                        symbol='o',
                        pen=pen2,
                        symbolSize=5,
                        symbolBrush=('b')
                        )
                maximums.update({time_stamp: showed_max})
                minimums.update({time_stamp: showed_min})
            self.dict_showed_extremums.update({
                            'max': maximums, 
                            'min': minimums
                        })
        self.dict_bandwidth_data.update({'source': dict_curves_filtred})
        #print('KEYS:', self.dict_showed_extremums.keys())
        self.show_graphic_filtered()
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listWidget.setHidden(0)
        
        return True

    def save_button_pressed(self: dict) -> bool:

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

    def export_data(self: dict) -> None:

        value = self.dict_bandwidth_data[self.bandwidths[0]]
        rows = value[self.list_times[0]]
        count_rows = len(rows)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 1)
        self.listWidget.setHidden(1)
        count = 0
        total_count = len(self.bandwidths)
        for bandwidth, dict_data in self.dict_bandwidth_data.items():
            count += 1
            progress = count*100/total_count
            self.progressBar.setValue(progress)
            QApplication.processEvents()
            export_curves(
                count_rows,
                self.source_filepath,
                self.target_dirpath,
                bandwidth,
                dict_data)
        self.progressBar.setValue(0)
        self.progressBar.setProperty('visible', 0)
        self.listWidget.setHidden(0)

    def close_button_pressed(self: dict) -> None:
        if self.dict_bandwidth_data:
            self.save_button_pressed()
        QApplication.quit()


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    exit(app.exec_())
