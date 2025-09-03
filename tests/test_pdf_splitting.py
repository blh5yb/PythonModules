# from os.path import split
# import os
# from os.path import split

from tests.custom_fixtures import multi_page_pdf, pytest, patch, Mock
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
    @patch('src.pdf_splitting.PdfReader')
    @pytest.mark.parametrize(
         'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_contructor(self, mock_pdf_reader, multi_page_pdf):
        in_pdf = multi_page_pdf
        # in_pdf.write_text('Some text')
        PdfSplitting(in_pdf)
        mock_pdf_reader.assert_called_with(in_pdf)

    @patch('src.pdf_splitting.PdfReader')
    @pytest.mark.parametrize(
        'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_constructor_exception(self, mock_pdf_reader, multi_page_pdf):
        in_pdf = multi_page_pdf
        # in_pdf.write_text('Some text')
        mock_pdf_reader.side_effect = Exception("PdfReader Exception")
        with pytest.raises(Exception) as e:
            PdfSplitting(in_pdf)
            assert e.value == "PdfReader Exception"

    @patch('src.pdf_splitting.PdfReader')
    @pytest.mark.parametrize(
        'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_write_single_pages(self, mock_pdf_reader, mock_pdf_writer, multi_page_pdf, tmp_path):

        split_pdf = PdfSplitting(multi_page_pdf)

        # with patch.object(split_pdf, '_PdfSplitting__write_output') as mock_write_output:
        split_pdf.write_single_pages({0, 1}, f'{tmp_path}/out_pdf')

        assert mock_pdf_writer.call_count == 2
        mock_pdf_reader.assert_called()
        mock_pdf_writer.return_value.add_page.assert_called()
        assert mock_pdf_writer.return_value.write.call_count == 2
        assert mock_pdf_writer.return_value.add_page.call_count == 2
        # assert mock_write_output.call_count == 2

    @pytest.mark.parametrize(
        'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_write_single_pages_exception(self, mock_pdf_writer, multi_page_pdf, tmp_path):

        split_pdf = PdfSplitting(multi_page_pdf)
        mock_pdf_writer.return_value.add_page.side_effect = Exception("Single Pages Exception Caught")
        with pytest.raises(Exception) as e:
            split_pdf.write_single_pages({0, 1}, f'{tmp_path}/out_pdf')
            assert e.value == "Single Pages Exception Caught"

        # with patch.object(split_pdf, '_PdfSplitting__write_output') as mock_write_output:


    @patch('src.pdf_splitting.PdfReader')
    @pytest.mark.parametrize(
        'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_write_page_range(self, mock_pdf_reader, mock_pdf_writer, multi_page_pdf, tmp_path):

        in_pdf = multi_page_pdf
        split_pdf = PdfSplitting(in_pdf)
        # with patch.object(split_pdf, '_PdfSplitting__write_output') as mock_write_output:
        test_out_file = f'{tmp_path}/single_page_test.pdf'
        split_pdf.write_page_range(0, 2, test_out_file)

        assert mock_pdf_writer.call_count == 1
        mock_pdf_reader.assert_called()
        mock_pdf_writer.return_value.add_page.assert_called()
        mock_pdf_writer.return_value.write.assert_called()
        assert mock_pdf_writer.return_value.add_page.call_count == 2

    @patch('src.pdf_splitting.PdfReader')
    @pytest.mark.parametrize(
        'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_write_page_range_exception(self, mock_pdf_reader, mock_pdf_writer, multi_page_pdf, tmp_path):

        in_pdf = multi_page_pdf
        split_pdf = PdfSplitting(in_pdf)
        # with patch.object(split_pdf, '_PdfSplitting__write_output') as mock_write_output:
        test_out_file = f'{tmp_path}/single_page_test.pdf'
        mock_pdf_writer.return_value.add_page.side_effect = Exception("Page Range Exception")
        with pytest.raises(Exception) as e:
            split_pdf.write_page_range(0, 2, test_out_file)
            assert e.value == "Page Range Exception"

    @patch('src.pdf_splitting.PdfReader')
    @pytest.mark.parametrize(
        'multi_page_pdf',
        [{"pdf_file": "test_pdf_file.pdf", "total_pages": 3}],
        indirect=True
    )
    def test_write_output_exception(self, mock_pdf_reader, mock_pdf_writer, multi_page_pdf, tmp_path):

        split_pdf = PdfSplitting(multi_page_pdf)
        # with patch.object(split_pdf, '_PdfSplitting__write_output') as mock_write_output:
        test_out_file = f'{tmp_path}/single_page_exception.pdf'
        mock_pdf_writer.return_value.write.side_effect = Exception("Write Output Exception")
        with pytest.raises(Exception) as e:
            split_pdf.write_page_range(0, 2, test_out_file)
            assert e.value == "Write Output Exception"



    ################################# Pytest Teardown Reference #########################################
    # def teardown_method(self, method):
    #     """Teardown for each test method."""
    #     print(f"teardown_method: Cleaning up for {method.__name__}")
    #
    # def teardown_class(cls):
    #     """Teardown for the entire class."""
    #     print(f"teardown_class: Cleaning up common resource: {cls.common_resource}")
    ######################################################################################################
