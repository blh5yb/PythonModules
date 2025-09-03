import pytest
from unittest.mock import patch, Mock
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@pytest.fixture(scope="session")
def multi_page_pdf(request, tmp_path_factory):
    """
    Fixture that creates a multi-page PDF file for testing.
    """
    print('params', request.param)
    pdf_path = tmp_path_factory.mktemp("pdf_data") / request.param['pdf_file']
    print(pdf_path)

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    for page in range(request.param['total_pages']):
        c.drawString(100, 750, f"This is Page {page}")
        c.showPage()

    c.save()

    yield pdf_path


@pytest.fixture(scope="function")
def create_named_test_file(request, tmp_path):
    """creates temp input files"""
    print('param', request.param)
    file = tmp_path / request.param
    yield file
    file.unlink()

@pytest.fixture(scope="function")
def create_general_test_file(tmp_path):
    """creates temp input files"""
    file = tmp_path / 'file.ext'
    yield file
    file.unlink()
