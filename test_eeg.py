from eeg_filters.upload import prepare_data
from eeg_filters.filters import make_filter, search_max_min
from eeg_filters.export import export_curves, export_extremums

source_file_name = input('input path for source file, please: ')
bandwidths = [[1, 100],[5, 100],[10, 100],[1, 200], [5, 200],[10, 200]]
max_region = [0.08, 0.1]
min_region = [0.103, 0.12]
sample_rate, list_times, list_ticks, list_out = prepare_data(source_file_name)

dict_filtered_data = {}

for bandwidth in bandwidths:
    dict_data = {}
    dict_extremums = {}
    for timestamp, list_data in zip(list_times,list_out):
        filtered_data = make_filter(
                                   list_data, 
                                   bandwidth, 
                                   sample_rate,
                                   order=3,
                                   rp=2)
        dict_data.update({timestamp: filtered_data})
        dict_extremums.update({timestamp:(
                                search_max_min(
                                list_ticks,
                                filtered_data, 
                                max_region, 
                                'max'
                                ), 
                                search_max_min(
                                list_ticks,
                                filtered_data, 
                                min_region, 
                                'min'
                                )
                                )})
        
        
    print(dict_extremums)
    export_curves(
                source_file_name,
                './',
                bandwidth,
                dict_data
                )
    export_extremums(
                    './',
                    bandwidth,
                    dict_extremums
                    )
