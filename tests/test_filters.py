import numpy as np
from eeg_filters.data_importer import DataImporter
from eeg_filters.filters import (
    show_plot, apply_filter, search_max_min
)


def test_apply_filter():
    data_importer = DataImporter("tests/data/sample_data.nex")
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
    assert max_filtered == np.float64(0.001940446691411313)

    bandwidth = [1, 50]
    filtered_curve = apply_filter(
        dataset, bandwidth, fs, order, rp
    )
    assert len(filtered_curve) == len(dataset)
    new_max_filtered = max(filtered_curve)
    assert max_filtered > new_max_filtered


def _test_search_max_min():
    pass


def _test_show_plot():
    pass


def _test_get_index_time():
    pass
