# -*- coding: utf-8 -*-

"""
Module for extract data of EEG signals by time of measuring.

It contain one public function:
    prepare_data - get filepath and give tuple of data;
and one private function:
    __append_data_to_list - for append data to list;
Input file can be only format -.

"""

import numpy as np
from pyedflib import highlevel
from loguru import logger


class DataImporter:
    """
    Class for import data from edf and nex formats
    to data structure to have possibility to filter it.
    """
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.type: str = ""
        self.count_measure: int = 0
        self.target_list: list[list[float]] = []
        self.__get_type_data()
        self.data: dict = {
            "sample_rate": 5000,
            "list_name_curves": [],
            "list_tick_times": [],
            "list_curves": []
        }
        if self.type == "nex" or self.type == "nex5":
            self.unwrap_nex_file()
        elif self.type == "edf":
            self.unwrap_edf_file()
        time_measuring = self.count_measure/self.data["sample_rate"]
        self.data["list_tick_times"] = np.linspace(
            0, time_measuring, self.count_measure, endpoint=False
        )
        if self.type == "nex":
            list_data = np.array(self.target_list).transpose()
            self.data["list_curves"] = list_data
        logger.info(
            f"imported : {len(self.data['list_curves'])} curves"
        )

    def __get_type_data(self) -> None:
        """
        Gets format incoming data by extention of file
        or by content of file.
        """
        filename: str = self.filepath.split("/")[-1]
        ext_file: str = filename.split(".")[-1]
        self.type = ext_file
        if ext_file == "txt":
            with open(self.filepath, "r") as file:
                data_file: str = file.read()
                if data_file.find("NeuroExplorer") != -1:
                    self.type = "nex"
                    return

    def unwrap_nex_file(self) -> None:
        """
        Gets rows from nex or nex5 file and put data
        to dictionary of data.
        """
        position: str = ""
        tmp_count: int = 0
        with open(self.filepath, "r") as file:
            if not file.read():
                return
            file.seek(0)
            for row in file.readlines():
                if row.find("Sampling rate: ") != -1:
                    self.data["sample_rate"] = float(
                        row.split("Sampling rate: ")[1].replace("Hz", "")
                    )
                    continue
                elif row.find("Measure times:") != -1:
                    position = "name_curves"
                    tmp_count = 0
                    continue
                elif row.find("Data:") != -1:
                    position = "curves"
                    tmp_count = 0
                    continue
                elif position == "":
                    continue
                elif tmp_count == 0:
                    tmp_count += 1
                    continue
                if position == "name_curves":
                    self.get_list_name_curves_from_nex_file(row)
                    tmp_count = 0
                else:
                    self.append_data_from_nex_file(row)
                    self.count_measure += 1

    def get_list_name_curves_from_nex_file(self, row: str) -> None:
        """
        Gets list of times from nex file
        """
        list_times: list[str] = []
        splitted_row: list[str] = row.replace("\n", "").split("   ")
        if len(splitted_row) > 1:
            list_times = [
                splitted_row[i].replace(" ", "") for i in range(
                    1, len(splitted_row) - 1
                )
            ]
        self.data["list_name_curves"] = list_times

    def append_data_from_nex_file(self, row: str) -> None:
        """
        Append data from row of source file to list of data.
        """
        row = row.replace("\n", "")
        row_splitted = row.split(":")[1].split("   ")
        rowlist = []
        for i in range(1, len(row_splitted)):
            str_value = row_splitted[i].replace(" ", "")
            if str_value:
                int_value = float(row_splitted[i].replace(" ", ""))
                rowlist.append(int_value)
        self.target_list.append(rowlist)

    def unwrap_edf_file(self) -> None:
        """
        Unwraps edf file and put data to self.data dictionary
        """
        signals, signal_headers, header = highlevel.read_edf(self.filepath)
        channels = [i["label"] for i in signal_headers]
        sample_rate = signal_headers[0]["sample_frequency"]
        self.data["sample_rate"] = sample_rate
        self.data["list_name_curves"] = channels
        self.data["list_curves"] = signals
        # for row in signals:
        #     self.target_list.append(row)
        self.count_measure = len(signals[0])
