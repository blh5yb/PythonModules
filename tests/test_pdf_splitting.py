# from os.path import split
# import os
# from os.path import split
from unittest.mock import MagicMock

from tests.conftest import multi_page_pdf, pytest, patch, Mock
from src.pdf_splitting import *

@pytest.fixture(scope="function")
def mock_pdf_writer():
    with patch('src.pdf_splitting.PdfWriter') as pdf_writer_mock:
        pdf_writer_mock.return_value.add_page = Mock(return_value=False)
        pdf_writer_mock.return_value.write = Mock(return_value=False)
        yield pdf_writer_mock


class TestPdfSplitting:
    ################################# Pytest Setup Reference #########################################
    # def setup_class(cls):
    #     """Setup for the entire class."""
    #     cls.common_resource = "Initialized common resource"
    #     print(f"setup_class: {cls.common_resource}")
    #
    # def setup_method(self, method):
    #     """Setup for each test method."""
    #     self.instance_resource = "Initialized instance resource"
    #     print(f"setup_method: {self.instance_resource} for {method.__name__}")
    ##################################################################################################
    @pytest.mark.parametrize('multi_page_pdf', [
        ({"file_name": "test_file.pdf", "text": ["INCLUDE THIS TEXT HERE", "EXCLUDE THIS TEXT HERE",
                                                 "INCLUDE THIS TEXT HERE, BUT NOT IF EXCLUDE THIS TEXT IS ALSO HERE"
                                                 ]})
    ], indirect=True)
    def test_split_pdf(self, multi_page_pdf, tmp_path):
        """"""
        res = PdfSplitting().split_pdf(multi_page_pdf, f'{tmp_path}', includes=["INCLUDE THIS TEXT"], excludes=["EXCLUDE THIS TEXT"] )
        filename = os.path.split(multi_page_pdf)[1]
        assert res ==  [f'{tmp_path}/{filename}'.replace(".pdf", "_0.pdf")]

    def test_filter_pages(self):
        """Test PdfSplitting methods which filter pages which have ALL inclusion regex and none of the exclusion regex"""
        mock_pdf_source = MagicMock()
        mock_pg1 = MagicMock()
        mock_pg1.extract_text.return_value = "INCLUDE THIS TEXT HERE"
        mock_pg2 = MagicMock()
        mock_pg2.extract_text.return_value = "EXCLUDE THIS TEXT HERE"
        mock_pg3 = MagicMock()
        mock_pg3.extract_text.return_value = "INCLUDE THIS TEXT HERE, BUT NOT IF EXCLUDE THIS TEXT IS ALSO HERE"
        mock_pdf_source.pages = [mock_pg1, mock_pg2, mock_pg3]
        mock_pdf_source.get_num_pages.return_value = 3
        res = PdfSplitting().filter_pages(mock_pdf_source, includes=["INCLUDE THIS TEXT"], excludes=["EXCLUDE THIS TEXT"])
        assert res == [0]

    def test_filter_pages_custom_over_ride(self):
        """Test CustomPDFSplitter which over-rides filter-pages method to include pages which have ANY inclusion regex and none of the exclusion regex"""
        mock_pdf_source = MagicMock()
        mock_pg1 = MagicMock()
        mock_pg1.extract_text.return_value = "INCLUDE THIS TEXT HERE"
        mock_pg2 = MagicMock()
        mock_pg2.extract_text.return_value = "ANOTHER TEXT TO INCLUDE"
        mock_pg3 = MagicMock()
        mock_pg3.extract_text.return_value = "INCLUDE THIS TEXT HERE, BUT NOT IF EXCLUDE THIS TEXT IS ALSO HERE"
        mock_pdf_source.pages = [mock_pg1, mock_pg2, mock_pg3]
        mock_pdf_source.get_num_pages.return_value = 3
        res = CustomPDFSplitter().filter_pages(mock_pdf_source, includes=["INCLUDE THIS TEXT", "ANOTHER TEXT TO INCLUDE"], excludes=["EXCLUDE THIS TEXT"])
        assert res == [0, 1]

    ################################# Pytest Teardown Reference #########################################
    # def teardown_method(self, method):
    #     """Teardown for each test method."""
    #     print(f"teardown_method: Cleaning up for {method.__name__}")
    #
    # def teardown_class(cls):
    #     """Teardown for the entire class."""
    #     print(f"teardown_class: Cleaning up common resource: {cls.common_resource}")
    ######################################################################################################
