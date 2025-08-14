from pypdf import PdfReader, PdfWriter
# from src.shared import logger
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %Z')
logger = logging.getLogger(__name__)

########################################################################################################################
# Pdf Splitting Module
# Author: Barry Hykes Jr, bhykes@gmail.com
# version 1.0.0
########################################################################################################################


class PdfSplitting:
    """Split pdfs into separate pages"""
    def __init__(self, in_pdf):
        """
        Initialize PdfReader for input file
        :param in_pdf: full path to input pdf file, str
        """
        # super().__init__()
        try:
            self.__reader = PdfReader(in_pdf)
            logger.info(f"Created pdf reader for {in_pdf}")
        except Exception as e:
            logger.error(f"An error occurred reading pdf file, {in_pdf}: {e}")
            raise

    def write_single_pages(self, my_pages, out_file_prefix):
        """
        write individual pages to pdfs
        :param my_pages: pages numbers to print, set of integers
        :param out_file_prefix: prefix of out pdf, str
        :return:
        """
        logger.info(f"Writing individual pdf pages {my_pages}")
        for page_num in list(my_pages):
            out_file = f"{out_file_prefix}_{page_num}.pdf"
            try:
                writer = PdfWriter()
                writer.add_page(self.__reader.pages[page_num])
                self.__write_output(out_file, writer)
            except Exception as e:
                logger.error(f"An error occurred writing {page_num} to {out_file}: {e}")
                raise

    def write_page_range(self, start, end, out_file):
        """
        write page range to a pdf
        :param start: range start, int
        :param end: range end, int
        :param out_file: full path of out file, str
        :return:
        """
        logger.info(f"Writing pdf page range: {start} - {end - 1}")
        try:
            writer = PdfWriter()
            for page_num in range(start, end):
                writer.add_page(self.__reader.pages[page_num])
            self.__write_output(out_file, writer)

        except Exception as e:
            logger.error(f"Error writing pdf page range, {start} - {end - 1}: {e}")
            raise

    @staticmethod
    def __write_output(filename, writer):
        try:
            with open(filename, "wb") as out_pdf:
                writer.write(out_pdf)
                logger.info(f"Wrote outfile {filename}")

        except Exception as e:
            logger.error(f"Error writing pdf to {filename}: {e}")
            raise

def main(args):
    # input_pdf = "./Input/Python.pdf"
    out = f"{args.out_folder}/{args.out_prefix}"
    split_pdf = PdfSplitting(args.input_pdf)
    # SplitPdf.write_page_range(0, 2, f'./Output/sample_out1.pdf')
    split_pdf.write_page_range(0, 2, f'{out}.pdf')
    # SplitPdf.write_single_pages({0,2}, './Output/single_pdf_page')
    split_pdf.write_single_pages({0,2}, out)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PDF Splitting Module")
    parser.add_argument('-i', '--input_pdf', type=str, action="store", required=True, help="full path to input file")
    parser.add_argument('-o', '--out_folder', type=str, action="store", required=True, help="output folder")
    parser.add_argument('-p', '--out_prefix', type=str, action="store", required=True, help="output file prefix (i.e out_file)")
    parser_args = parser.parse_args()
    # parser_args = {
    #     'input_pdf':  input("Please enter the full path to the input pdf file: "),
    #     'out_folder': input("Please enter the path to the output folder: "),
    #     'out_prefix': input("Please enter the out file prefix: ")
    # }
    main(parser_args)