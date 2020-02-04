# -*- coding: utf-8 -*-

"""
Module for export data of EEG signal to file.

Format of output files -.

"""

import os


def __create_head_output_file(
                            source_filepath: str,
                            target_filepath: str,
                            bandwidth: str) -> None:
    """ Create header of output files. """
    with open(source_filepath, 'r') as file:
        textfile = file.read()
        header = textfile.split('Data:')[0]+'\n Data: \n'
        with open(target_filepath, 'a') as outfile:
            outfile.write(header)


def export_curves(
                    count_row: int,
                    source_filepath: str,
                    target_dirpath: str,
                    bandwidth: str,
                    dict_data: dict,
                    ) -> bool:
    """Write data to putput. Returns: True if export ok."""
    target_filepath = os.path.join(
            target_dirpath,
            'filter%s.dat' % bandwidth
            )
    __create_head_output_file(
                                source_filepath,
                                target_filepath,
                                bandwidth
                                )
    keys = dict_data.keys()
    with open(target_filepath, 'a') as outfile:
        for numrow in range(0, len(keys)):
            outfile.write('     '+str(numrow + 1))
        outfile.write('\n')
        for row in range(0, count_row):
            outfile.write('   %s:   ' % str(row + 1))
            for timestamp in keys:
                outfile.write('%.5f    ' % dict_data[timestamp][row])
            outfile.write('\n')
    return True
    

def export_extremums(
                    target_dirpath: str,
                    bandwidth: str,
                    dict_data: dict,
                    dict_extremums: dict = None
                    ) -> bool:
    """
    """
    target_filepath = os.path.join(
            target_dirpath,
            'extremums%s.dat' % bandwidth
            )
    with open(target_filepath, 'a') as outfile:
        outfile.write('timestamp\tmaxtime\tmaxval\tmintime\tminval')
        outfile.write('\n')
        
    pass
    
