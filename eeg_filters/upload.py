import numpy as np

def prepare_data(filepath):
    '''
    function get rows from input file 
    and append data to dictionary of data
    '''
    #dict_curves = {}
    list_times = []
    position = ''
    tmp_count = 0
    target_list = []
    with open(filepath,'r') as file:
        for row in file.readlines():
            if row.find('Sampling rate: ') != -1:
                simple_rate = float(row.split('Sampling rate: ')[1].replace('Hz',''))
                continue
            elif row.find('Measure times:') !=-1:
                position = 'times'
                tmp_count = 0
                continue
            elif row.find('Data:') !=-1:
                position = 'curves'
                tmp_count = 0
                continue
            elif position == '':
                continue
            elif tmp_count == 0:
               tmp_count += 1
               continue
            if position == 'times':
                list_times = [row.split('   ')[i].replace(' ','') for i in range(1,len(row.split('   '))-1)]
                tmp_count = 0
            else:
                target_list = append_data_to_list(target_list,row)
    list_out = np.array(target_list).transpose()
    return simple_rate, list_times, list_out


def append_data_to_list(target_list, row):
    '''
    Append data from row of file to dict of data
    '''
    row = row.replace('\n','')
    row_splitted = row.split(':')[1].split('   ')
    rowlist = []
    for i in range(1,len(row_splitted)):
        value = float(row_splitted[i].replace(' ',''))
        rowlist.append(value)
    target_list.append(rowlist)
    return target_list
    
