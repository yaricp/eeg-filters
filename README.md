# eeg-filters

Package helps you to filter and analyze EEG signals and EP (evoked potentials).
Filter based on Chebyshev filter from scipy.signals

You can get data from files exported from NeuroExplorer Vesion 4.4 in ASCII format or from   in edf format.
Then you can apply a bandpass filter in some bandwidth like [1, 220]. These the lower and upper frequency boundaries in Hz.

Also you can find maximums in one time interval and minimums in another time interval.

Finally you can export data to files.
Filtered data could be exported to the ASCII file in the same (NeuroExplorer 4.4) format as the source file.
Extremums can be exported to a text file with tab splitted columns.

## Requirements

* numpy
* scipy
* matplotlib

## Installation.

pip install eeg-filters

## Usage

For example:

```
$python3
>>> from eeg_filters.data_importer import DataImporter

>>> from eeg_filters.filters import show_plot

>>> data_importer = DataImporter('input/data.txt')

>>> bandwidth = [1, 200]

>>> show_plot(data_importer.data, bandwidth, 3, 2, 0.003)

>>> show_plot(data_importer.data, bandwidth, max_region=[0.08,0.104], min_region=[0.105,0.14])
```
In this example we made a filter in bandwidth = [1, 200].
And in the last line we make show_plot with extremums.

You can use it in scripts like this:

```
!#/usr/bin/python3

from eeg_filters.data_importer import DataImporter
from eeg_filters.filters import apply_filter, search_max_min
from eeg_filters.export import export_curves, export_extremums

source_file_name = input('input path for source file, please: ')
bandwidths = [[1, 100],[5, 100],[10, 100],[1, 200], [5, 200],[10, 200]]
max_region = [0.01, 0.02]
min_region = [0.04, 0.06]
incoming_data = DataImporter(source_file_name).data
list_name_curves = incoming_data["list_name_curves"]
list_curves = incoming_data["list_curves"]
list_tick_times = incoming_data["list_tick_times"]
sample_rate = incoming_data["sample_rate"]

dict_filtered_data = {}

for bandwidth in bandwidths:
    dict_data = {}
    dict_extremums = {}
    for timestamp, curve in zip(list_name_curves, list_curves):
        filtered_data = apply_filter(
            curve, bandwidth, sample_rate, order=3, rp=2
        )
        dict_data.update({timestamp: filtered_data})
        dict_extremums.update(
            {timestamp:(
                search_max_min(
                    list_tick_times, filtered_data, max_region,'max'
                ), 
                search_max_min(
                    list_tick_times, filtered_data, min_region,'min'
                )
            )}
        )
        
    # export data of filtered EEG signals
    export_curves(
        source_file_name, './', bandwidth, dict_data
    )
    # export extremums of filtered EEG signals
    export_extremums(
        './', bandwidth, dict_extremums
    )
```
Also you can use any UI for this package.
For example you can see this project:
* https://github.com/yaricp/qt5-eeg-filters
