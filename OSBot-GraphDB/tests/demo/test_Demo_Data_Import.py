from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from osbot_graphsv.demo.Demo_Data_Import import Demo_Data_Import


class test_Demo_Data_Import(TestCase):

    def setUp(self):
        self.demo_data_import = Demo_Data_Import()
        self.result    = None

        self.demo_data_import.indexes.rebuild()

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test__init__(self):
        assert Files.folder_exists(self.demo_data_import.demo_data.data_folder) is True

    def test_import_all(self):
        self.demo_data_import.import_all()

    def test_import_Sample_Database_extracts(self):
        self.demo_data_import.import_Sample_Database_extracts__HR_Database()
        self.demo_data_import.import_Sample_Database_extracts__Sunways_application_user_extract()

    def test_dataset__People_Role_Reporting_line(self):
        self.result = self.demo_data_import.import_People_Role_Reporting_line()

    def test_import_Role_Team_Function_Business(self):
        self.result = self.demo_data_import.import_Role_Team_Function_Business()

    def test_import_Device_Person_Account_Application__by_Device(self):
        self.result = self.demo_data_import.import_Device_Person_Account_Application__by_Device()

    def test_import_Device_Person_Account_Application__by_Person(self):
        self.result = self.demo_data_import.import_Device_Person_Account_Application__by_Person()

    def test_import__Device_Person_Account_Application__by_Account(self):
        self.result = self.demo_data_import.import__Device_Person_Account_Application__by_Account()