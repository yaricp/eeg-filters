import numpy as np
from eeg_filters import DataImporter


class TestDataImporterNex:

    data_importer = DataImporter("tests/data/example2.nex")

    def test_init(self):
        assert self.data_importer.type == "nex"
        assert self.data_importer.data["sample_rate"] == 10000.0
        assert len(self.data_importer.data["list_name_curves"]) == 35
        assert self.data_importer.data["list_name_curves"][0] == "13:34:40"
        assert self.data_importer.data["list_name_curves"][-1] == "16:45:52"
        assert len(self.data_importer.data["list_tick_times"]) == 800
        assert len(self.data_importer.data["list_curves"]) == 35
        assert len(self.data_importer.data["list_curves"][0]) == 800
        assert len(self.data_importer.data["list_curves"][-1]) == 800

    def test_get_list_name_curves_from_nex_file(self):
        row = "    13:34:40    13:45:10    13:49:14    13:58:54    "
        self.data_importer.get_list_name_curves_from_nex_file(row)
        assert len(self.data_importer.data["list_name_curves"]) == 4
        assert self.data_importer.data["list_name_curves"] == [
            "13:34:40", "13:45:10", "13:49:14", "13:58:54"
        ]

    def test_append_data_from_nex_file(self):
        row = "   801 :   -0.00044     0.00044    -0.00044    "\
            "-0.00044    -0.00044    -0.00044     0.00001    "\
            "-0.00044    -0.00009    -0.00044    -0.00024    "\
            "-0.00156     0.00044    -0.00010     0.00107     "\
            "0.00090    -0.00035    -0.00033     0.00135     "\
            "0.00049    -0.00091     0.00096     0.00054    "\
            "-0.00031     0.00085     0.00008     0.00042    "\
            "-0.00077    -0.00034    -0.00050    -0.00058    "\
            "-0.00004     0.00033    -0.00016    -0.00004  "
        self.data_importer.append_data_from_nex_file(row)
        assert len(self.data_importer.target_list) == 801
        assert len(self.data_importer.target_list[-1]) == 35
        assert self.data_importer.target_list[-1] == [
            -0.00044, 0.00044, -0.00044, -0.00044, -0.00044,
            -0.00044, 0.00001, -0.00044, -0.00009, -0.00044,
            -0.00024, -0.00156, 0.00044, -0.00010, 0.00107,
            0.00090, -0.00035, -0.00033, 0.00135, 0.00049,
            -0.00091, 0.00096, 0.00054, -0.00031, 0.00085,
            0.00008, 0.00042, -0.00077, -0.00034, -0.00050,
            -0.00058, -0.00004, 0.00033, -0.00016, -0.00004
        ]


class TestDataImporterNexTxt:

    data_importer = DataImporter("tests/data/example3_nex.txt")

    def test__get_type_data(self):
        self.data_importer._DataImporter__get_type_data()
        assert self.data_importer.type == "nex"


class TestDataImporterEDF:

    data_importer = DataImporter("tests/data/example1.edf")

    def test_init(self):
        assert self.data_importer.type == "edf"
        assert self.data_importer.data["sample_rate"] == 200.0
        assert len(self.data_importer.data["list_name_curves"]) == 37
        assert self.data_importer.data["list_name_curves"][0] == "EEG FP1"
        assert self.data_importer.data["list_name_curves"][-1] == "DC04"
        assert len(self.data_importer.data["list_tick_times"]) == 363620
        assert len(self.data_importer.data["list_curves"]) == 37
        assert len(self.data_importer.data["list_curves"][0]) == 363620
        assert len(self.data_importer.data["list_curves"][-1]) == 363620
        assert self.data_importer.data["list_curves"][0][0] == np.float64(
            -0.00017187762289504373
        )
        assert self.data_importer.data["list_curves"][-1][-1] == np.float64(
            28.95083726253051
        )

    def test__get_type_data(self):
        self.data_importer._DataImporter__get_type_data()
        assert self.data_importer.type == "edf"
