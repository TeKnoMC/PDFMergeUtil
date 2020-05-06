"""
This program merges the PDFs in the input directory into the output file
"""

import glob
import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from args import Arguments, ArgumentMissingError, UnknownArgumentError

def get_pdfs_in_directory(directory):
    """
    Returns a list of full paths to pdfs in a specified directory
    """
    return [os.path.join(os.getcwd(), filename) for filename in glob.glob(directory + "/*.pdf")]

def merge_pdfs(pdf_list, output):
    """
    Merges the list of pdfs in the order specified by pdf_list, and outputs them to the output file
    """
    newpdf_writer = PdfFileWriter()

    for pdf_path in pdf_list:
        nextpdf_reader = PdfFileReader(pdf_path)

        # For each page in pdf
        for pagenum in range(nextpdf_reader.getNumPages()):
            newpdf_writer.addPage(nextpdf_reader.getPage(pagenum))

    # Write pdf to output
    with open(output, "wb") as f:
        newpdf_writer.write(f)



# Input dir and output file not necessary - defaults to current directory and "output.pdf"
ARG_HANDLER = Arguments(sys.argv, [("i/input-directory", False, "."),
                                   ("o/output-file", False, "output.pdf")])

ARGS = {}
try:
    ARGS = ARG_HANDLER.get_argument_values()
except (ArgumentMissingError, UnknownArgumentError) as arg_err:
    print(arg_err.msg)
    print(ARG_HANDLER.usage())
    sys.exit()

INP_DIR = ARGS["-i"]
OUT_FILE = ARGS["-o"]

PDF_LIST = get_pdfs_in_directory(INP_DIR)
merge_pdfs(PDF_LIST, OUT_FILE)
