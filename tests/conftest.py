import pytest
from unittest.mock import patch, Mock
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@pytest.fixture(scope="session")
def multi_page_pdf(request, tmp_path_factory):
    """
    Fixture that creates a multi-page PDF file for testing.
    """
    file_name = request.param['file_name']
    pdf_path = tmp_path_factory.mktemp("pdf_data") / file_name
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    for file_text in request.param['text']:
        print('text', file_text, pdf_path)
        c.drawString(100, 750, file_text)
        c.showPage()

    c.save()
    yield pdf_path
    pdf_path.unlink()


@pytest.fixture(scope="function")
def create_named_test_file(request, tmp_path):
    """creates temp input files"""
    print('param', request.param)
    filename = request.param if request.param else 'file.ext'
    file = tmp_path / filename
    yield file
    file.unlink()

@pytest.fixture(scope="function")
def create_general_test_file(tmp_path):
    """creates temp input files"""
    file = tmp_path / 'file.ext'
    yield file
    file.unlink()
