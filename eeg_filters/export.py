# -*- coding: utf-8 -*-

"""
Module for export data of EEG signal to file.

Format of output files like NeuroExplorer4.4 text acsii.

Extremums can be exported in text file with tab splitted columns.

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

                    source_filepath: str,
                    target_dirpath: str,
                    bandwidth: str,
                    dict_data: dict,
                    count_rows: int = None,
                    ) -> bool:
    """Write data to putput. Returns: True if export ok."""
    target_filepath = os.path.join(
            target_dirpath,
            'filter%s.dat' % bandwidth
            )
    if os.path.exists(target_filepath):
        os.remove(target_filepath)
    __create_head_output_file(
                                source_filepath,
                                target_filepath,
                                bandwidth
                                )
    keys = dict_data.keys()
    if not count_rows:
        count_rows = len(dict_data)
    with open(target_filepath, 'a') as outfile:
        for numrow in range(0, len(keys)):
            outfile.write('     '+str(numrow + 1))
        outfile.write('\n')
        for row in range(0, count_rows):
            outfile.write('   %s:   ' % str(row + 1))
            for timestamp in keys:
                outfile.write('%.5f    ' % dict_data[timestamp][row])
            outfile.write('\n')
    return True


def export_extremums(
                    target_dirpath: str,
                    bandwidth: str,
                    dict_extremums: dict = None
                    ) -> bool:
    """
    Function exports extremums of curves,
    which found in special ranges.

    Returns: True if export ok.

    """
    target_filepath = os.path.join(
            target_dirpath,
            'extremums%s.dat' % bandwidth
            )
    if os.path.exists(target_filepath):
        os.remove(target_filepath)
    with open(target_filepath, 'a') as outfile:
        outfile.write('timestamp\tmaxtime\tmaxval\tmintime\tminval')
        outfile.write('\n')
        for key, row in dict_extremums.items():
            outfile.write('%s\t' % key)
            outfile.write('%.5f\t' % row[0][0])
            outfile.write('%.5f\t' % row[0][1])
            outfile.write('%.5f\t' % row[1][0])
            outfile.write('%.5f\n' % row[1][1])
    return True
