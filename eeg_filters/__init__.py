# -*- coding: utf-8 -*-
"""
This package helps you to get curves EEG from files exported from
NeuroEplorer4.4 in acsii format (.nex) or from .edf files.

After that you can to filter its for analize.

Also you can find extremums of curves in ranges which you need.

You can use this package for export filtered data in format like
from NeuroExplorer4.4.

Extremums can be exported in text file with tab splitted columns.

"""
from .data_importer import DataImporter


__author__ = "Iaroslav Pisarev"
__copyright__ = "Copyright (C) 2019 Iaroslav Pisarev"
__license__ = "MIT License"
__version__ = "0.0.8"
__all__ = ["export", "filters", "DataImporter", "upload"]
