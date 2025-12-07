from pypdf import PdfReader, PdfWriter
from src.shared import logger
import re
import os

########################################################################################################################
# Pdf Splitting Module
# Author: Barry Hykes Jr, bhykes@gmail.com
# version 1.0.0
########################################################################################################################


class PdfSplitting:
    """Split pdfs into separate pages"""

    @staticmethod
    def filter_pages(
            source: PdfReader,
            page_indices: list[int] = None,
            includes: list[str] = [],
            excludes: list[str] = [],
    ) -> list[int]:
        """
        Filter pdf by page number and/or text
        Args:
            source: input pdf
            page_indices: indices of the pdf to include
            includes: required page texts for inclusion
            excludes: exclude pages with these texts
        Returns: page indices to write to output
        """
        page_indices = [x for x in range(source.get_num_pages())] if page_indices is None else page_indices
        if len(includes) or len(excludes):
            remove_indices = set()
            for index in page_indices:
                page_text = source.pages[index].extract_text()
                for exclusion_regex in excludes:
                    exclusion_regex = exclusion_regex.replace(" ", "\\s*")
                    if re.compile(exclusion_regex).search(
                            page_text) is not None:  # only including if exclude text is not found
                        remove_indices.add(index)
                        break  # break the inner loop and continue to next index

                for inclusion_regex in includes:
                    # only including if all includes are matched
                    # Just create new splitter class and override this method if you instead need to include a page
                    # which is matching any of the includes regex patterns
                    inclusion_regex = inclusion_regex.replace(" ", "\\s*")
                    if re.compile(inclusion_regex).search(page_text) is None:
                        remove_indices.add(index)
                        break  # break the inner loop and continue to next index

            page_indices = [idx for idx in page_indices if idx not in remove_indices]
        return page_indices

    def split_pdf(self,
                  path_to_pdf: str,
                  out_folder: str,
                  page_indices: list[int] = None,
                  includes: list[str] = [],
                  excludes: list[str] = [],
                  ):
        """
        Split pdf and optionally filter pages and/or text
        """
        try:
            reader = PdfReader(path_to_pdf, strict=False)
            output_names = []
            page_nums = self.filter_pages(reader, page_indices, includes, excludes)
            filename = os.path.split(path_to_pdf)[1]
            for index, num in enumerate(page_nums):
                output_name = f'{out_folder}/{filename}'.replace(".pdf", f"_{index}.pdf") # use index for page name
                writer = PdfWriter()
                writer.add_page(reader.pages[num]) # use number to get the correct page num
                writer.write(output_name)
                writer.close()
                output_names.append(output_name)
            return output_names
        except Exception as e:
            logger.error(f"An error occurred writing splitting {path_to_pdf}: {e}")
            raise

class CustomPDFSplitter(PdfSplitting):
    """method to over-ride filter pages method for a different includes logic"""
    @staticmethod
    def filter_pages(
        source: PdfReader,
        page_indices: list[int] = None,
        includes: list[str] = [],
        excludes: list[str] = [],
    ) -> list[int]:
        """
        over-riding the filter_pages method to include pdfs matching any of the includes regex patterns
        """
        page_indices = [x for x in range(source.get_num_pages())] if page_indices is None else page_indices
        if len(includes) or len(excludes):
            remove_indices = set()
            for index in page_indices:
                page_text = source.pages[index].extract_text()
                for exclusion_regex in excludes:
                    exclusion_regex = exclusion_regex.replace(" ", "\\s*")
                    if re.compile(exclusion_regex).search(page_text) is not None: # only including if exclude text is not found
                        remove_indices.add(index)
                        break # break the inner loop and continue to next index
                page_is_valid = False
                for inclusion_regex in includes:
                    inclusion_regex = inclusion_regex.replace(" ", "\\s*")
                    if index not in remove_indices and re.compile(inclusion_regex).search(page_text) is not None:
                        page_is_valid = True
                        break # break the inner loop and continue to next index
                if not page_is_valid:
                    remove_indices.add(index)
            page_indices = [idx for idx in page_indices if idx not in remove_indices]
        return page_indices

def main(args):
    # input_pdf = "./Input/Python.pdf"
    PdfSplitting().split_pdf(args.input_pdf, args.out_folder, [0, 1, 2])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PDF Splitting Module")
    parser.add_argument('-i', '--input_pdf', type=str, action="store", required=True, help="full path to input file")
    parser.add_argument('-o', '--out_folder', type=str, action="store", required=True, help="output folder")
    parser_args = parser.parse_args()
    main(parser_args)