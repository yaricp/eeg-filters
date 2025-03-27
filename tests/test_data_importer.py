from eeg_filters import DataImporter


class TestDataImporter:

    data_importer = DataImporter("tests/data/sample_data.nex")

    def test_init(self):
        assert self.data_importer.type == "nex"
        assert self.data_importer.data["sample_rate"] == 10000.0
        assert len(self.data_importer.data["list_times"]) == 35
        assert self.data_importer.data["list_times"][0] == "13:34:40"
        assert self.data_importer.data["list_times"][-1] == "16:45:52"
        assert len(self.data_importer.data["list_ticks"]) == 800
        assert len(self.data_importer.data["list_data"]) == 35
        assert len(self.data_importer.data["list_data"][0]) == 800
        assert len(self.data_importer.data["list_data"][-1]) == 800

    def test_get_list_times_nex_file(self):
        row = "    13:34:40    13:45:10    13:49:14    13:58:54    "
        self.data_importer.get_list_times_nex_file(row)
        assert len(self.data_importer.data["list_times"]) == 4
        assert self.data_importer.data["list_times"] == [
            "13:34:40", "13:45:10", "13:49:14", "13:58:54"
        ]

    def test_append_data_nex_file(self):
        row = "   801 :   -0.00044     0.00044    -0.00044    "\
            "-0.00044    -0.00044    -0.00044     0.00001    "\
            "-0.00044    -0.00009    -0.00044    -0.00024    "\
            "-0.00156     0.00044    -0.00010     0.00107     "\
            "0.00090    -0.00035    -0.00033     0.00135     "\
            "0.00049    -0.00091     0.00096     0.00054    "\
            "-0.00031     0.00085     0.00008     0.00042    "\
            "-0.00077    -0.00034    -0.00050    -0.00058    "\
            "-0.00004     0.00033    -0.00016    -0.00004  "
        self.data_importer.append_data_nex_file(row)
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


class TestDataImporterTxt:

    data_importer = DataImporter("tests/data/sample_data.txt")

    def test__get_type_data(self):
        self.data_importer._DataImporter__get_type_data()
        assert self.data_importer.type == "nex"


class TestDataImporterEDF:

    data_importer = DataImporter("tests/data/sample_data.edf")

    def test__get_type_data(self):
        self.data_importer._DataImporter__get_type_data()
        assert self.data_importer.type == "edf"


class TestDataImporterTextEDF:

    data_importer = DataImporter("tests/data/sample_data_edf.txt")

    def test__get_type_data(self):
        self.data_importer._DataImporter__get_type_data()
        assert self.data_importer.type == "edf"