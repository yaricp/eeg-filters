
def create_head_output_file(source_filepath, target_filepath, bandwidth):
    '''
    create header of output files
    '''
    with open(source_filepath,'r') as file:
        textfile = file.read()
        header = textfile.split('Data:')[0]+'\n Data: \n'
        with open('%s%s.dat' % (target_filepath, bandwidth),'a') as outfile:
            outfile.write(header)


def write_out_data(target_filepath, bandwidth, out_dict):
    '''
    Write data to putput
    '''
    with open('%s%s.dat' % (target_filepath, bandwidth),'a') as outfile:
        for i in range(1, len(out_dict)+1):
            outfile.write('     '+str(i))
        outfile.write('\n')
        for row in range(0,3000):
            outfile.write('   %s:   ' % str(row+1))
            for col in range(0, len(out_dict)):
                outfile.write('%s    '% out_dict[col][row])
            outfile.write('\n')
