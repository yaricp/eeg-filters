import os
import numpy as np
from eeg_filters.data_importer import DataImporter
from eeg_filters.filters import (
    show_plot, apply_filter, search_max_min, get_index_time
)


def test_apply_filter():
    data_importer = DataImporter("tests/data/example2.nex")
    incoming_data = data_importer.data
    list_curves = incoming_data["list_curves"]
    fs = incoming_data["sample_rate"]
    dataset = list_curves[0]
    order = 3
    rp = 2
    bandwidth = [1, 200]
    filtered_curve = apply_filter(
        dataset, bandwidth, fs, order, rp
    )
    assert len(filtered_curve) == len(dataset)
    max_filtered = max(filtered_curve)
    assert round(max_filtered, 9) == round(
        np.float64(0.001940446691411313), 9
    )

    bandwidth = [1, 50]
    filtered_curve = apply_filter(
        dataset, bandwidth, fs, order, rp
    )
    assert len(filtered_curve) == len(dataset)
    new_max_filtered = max(filtered_curve)
    assert max_filtered > new_max_filtered


def test_search_max_min():
    data_importer = DataImporter("tests/data/example2.nex")
    incoming_data = data_importer.data
    result = search_max_min(
        list_tick_times=incoming_data["list_tick_times"],
        signal_data=incoming_data["list_curves"][0],
        where_find=[0.01, 0.02],
        what_find="max"
    )
    assert (round(result[0], 4), round(result[1], 5)) == (0.0131, 0.00205)
    result = search_max_min(
        list_tick_times=incoming_data["list_tick_times"],
        signal_data=incoming_data["list_curves"][0],
        where_find=[0.01, 0.02],
        what_find="min"
    )
    assert (round(result[0], 4), round(result[1], 5)) == (0.0104, -0.00185)
    result = search_max_min(
        list_tick_times=incoming_data["list_tick_times"],
        signal_data=incoming_data["list_curves"][0],
        where_find=[0.04, 0.06],
        what_find="max"
    )
    assert (round(result[0], 4), round(result[1], 5)) == (0.0514, 0.00193)
    result = search_max_min(
        list_tick_times=incoming_data["list_tick_times"],
        signal_data=incoming_data["list_curves"][0],
        where_find=[0.04, 0.06],
        what_find="min"
    )
    assert (round(result[0], 4), round(result[1], 5)) == (0.0457, -0.00191)


def test_show_plot():
    data_importer = DataImporter("tests/data/example2.nex")
    incoming_data = data_importer.data
    plt, filename = show_plot(
        incoming_data=incoming_data,
        bandwidth=[50, 100],
        testmode=True
    )
    assert plt
    assert len(plt.gca().lines) == 35
    assert plt.gca().get_xlabel() == "bandwidth: [50, 100]"
    assert len(plt.gca().lines[0].get_xdata()) == 800
    assert filename == "filtered[50, 100].png"
    assert os.path.exists(
        os.path.join(os.getcwd(), filename)
    )
    os.remove(
        os.path.join(os.getcwd(), filename)
    )


def test_get_index_time():
    list_tick_times = [0.05, 0.06, 0.07, 0.08]
    time_s = 0.06
    result = get_index_time(list_tick_times=list_tick_times, time=time_s)
    assert result == 1
    time_s = 0.063
    result = get_index_time(list_tick_times=list_tick_times, time=time_s)
    assert result == 2
    time_s = 0.065
    result = get_index_time(list_tick_times=list_tick_times, time=time_s)
    assert result == 2
    time_s = 0.074
    result = get_index_time(list_tick_times=list_tick_times, time=time_s)
    assert result == 3
