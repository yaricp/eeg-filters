# eeg-filters

Package helps you to filter and analyze EEG signals.
Filter based on Chebyshev filter from scipy.signals

You can take data from files exported from NeuroExplorer Vesion 4.4 in ASCII format.
You can make a filter in some bandwidth like [1, 220].
These are the boundaries of frequencies in Hz.

Also you can find maximums in one region and minimums in another region.

Finally you can export data to files.
Curve data can be exported to the ascii format like NeuroExplorer file.
Extremums can be exported to a text file with tab splitted columns.

## Requirements

* numpy
* scipy
* matplotlib

## Instalation.

pip install eeg-filters

## Usage

For example:

```
$python3
>>> from eeg_filters.upload import prepare_data

>>> from eeg_filters.filters import show_plot

>>> sample_rate, list_times, list_ticks, list_out = prepare_data('input/data.txt')

>>> show_plot(list_times,list_ticks,list_out,[1, 200],sample_rate,3,2,0.003)

>>> show_plot(list_times,list_ticks,list_out,[1, 200],sample_rate,max_region=[0.08,0.104],min_region=[0.105,0.14])
```
In this example we made a filter in bandwidth = [1, 200].
And in the last line we make show_plot with extremums.

You can use it in scripts like this:

```
!#/usr/bin/python3

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
        
    # export data of filtered EEG signals
    export_curves(
                source_file_name,
                './',
                bandwidth,
                dict_data
                )
    # export extremums of filtered EEG signals
    export_extremums(
                    './',
                    bandwidth,
                    dict_extremums
                    )
```
Also you can use any UI for this package.
For example you can see this project:
* https://github.com/yaricp/qt5-eeg-filters
