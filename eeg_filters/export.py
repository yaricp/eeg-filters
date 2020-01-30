# -*- coding: utf-8 -*-

import os


def __create_head_output_file(
                            source_filepath: str,
                            target_filepath: str,
                            bandwidth: str) -> None:
    """ create header of output files """
    with open(source_filepath, 'r') as file:
        textfile = file.read()
        header = textfile.split('Data:')[0]+'\n Data: \n'
        with open(target_filepath, 'a') as outfile:
            outfile.write(header)


def write_out_data(
                    count_row: int,
                    source_filepath: str,
                    target_dirpath: str,
                    bandwidth: str,
                    dict_data: dict,
                    dict_extremums: dict = None
                    ) -> bool:
    """Write data to putput"""
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
