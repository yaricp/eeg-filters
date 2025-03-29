import os
from eeg_filters.export import export_curves


def test_copy_header():
    source_filepath = "tests/data/example2.nex"
    target_dirpath = "tests/data/"
    bandwidth = [100, 200]
    dict_data = {}

    with open(source_filepath, "r") as file:
        textfile = file.read()
        source_header = textfile.split("Data:")[0]

    export_curves(
        source_filepath=source_filepath,
        target_dirpath=target_dirpath,
        bandwidth=bandwidth,
        dict_data=dict_data
    )

    root_path = os.getcwd()
    result_filepath = os.path.join(
        root_path,
        "tests/data/example2-Filter-[100-200].dat"
    )
    print(result_filepath)
    print(os.path.exists(result_filepath))
    assert os.path.exists(result_filepath)

    with open(result_filepath, "r") as file:
        textfile = file.read()
        result_header = textfile.split("Data:")[0]

    assert source_header == result_header

    os.remove(result_filepath)
