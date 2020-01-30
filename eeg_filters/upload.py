# -*- coding: utf-8 -*-

import numpy as np


def prepare_data(filepath: str) -> tuple:
    """
    function get rows from input file
    and append data to dictionary of data

    """
    list_times = []
    position = ''
    tmp_count = 0
    target_list = []
    with open(filepath, 'r') as file:
        for row in file.readlines():
            if row.find('Sampling rate: ') != -1:
                simple_rate = float(
                        row.split('Sampling rate: ')[1].replace('Hz', '')
                        )
                continue
            elif row.find('Measure times:') != -1:
                position = 'times'
                tmp_count = 0
                continue
            elif row.find('Data:') != -1:
                position = 'curves'
                tmp_count = 0
                continue
            elif position == '':
                continue
            elif tmp_count == 0:
                tmp_count += 1
                continue
            if position == 'times':
                splitted_row = row.replace('\n', '').split('   ')
                if len(splitted_row) > 1:
                    list_times = [
                            splitted_row[i].replace(' ', '') for i in range(
                                    1, len(splitted_row) - 1
                                    )
                            ]
                tmp_count = 0
            else:
                target_list = __append_data_to_list(target_list, row)
    list_out = np.array(target_list).transpose()
    return simple_rate, list_times, list_out


def __append_data_to_list(target_list: list, row: str) -> list:
    """ Append data from row of file to dict of data """
    row = row.replace('\n', '')
    row_splitted = row.split(':')[1].split('   ')
    rowlist = []
    for i in range(1, len(row_splitted)):
        str_value = row_splitted[i].replace(' ', '')
        if str_value:
            int_value = float(row_splitted[i].replace(' ', ''))
            rowlist.append(int_value)
    target_list.append(rowlist)
    return target_list
