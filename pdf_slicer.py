#!/bin/python
""" A program to slice sections of pages from .PDF files """

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is not installed, yet is required.")
    exit()

import argparse

# Initialize variables
FILENAME = ""
SLICE_START = 0
SLICE_SPLIT = 1
SLICE_STEP = 0
SLICE_STOP = 0
VERBOSE = False

def main():
    """ Main function """
    desc_str = """
    This program splits up a .pdf file into multiple pages.
    When run with no arguments, this program splits it into single pages.
    Starting page and number of pages per split can be set using arguments.
    """

    # Initialize the global variables
    global FILENAME
    global SLICE_START
    global SLICE_SPLIT
    global SLICE_STEP
    global SLICE_STOP
    global VERBOSE

    parser = argparse.ArgumentParser(description=desc_str)
    # Add arguments
    parser.add_argument("FILENAME", nargs=1,
                        help="The name of the .pdf file to be processed.")
    parser.add_argument('-f', '--from', nargs=1, dest='START',
                        type=int, required=False,
                        help="Starting page number, counting up from 0.")
    parser.add_argument('-p', '--pages', nargs=1, dest='SPLIT',
                        type=int, required=False,
                        help="How many pages to slice the pdf into.")
    parser.add_argument('-s', '--skip', nargs=1, dest='STEP',
                        type=int, required=False,
                        help="Set this to skip pages.")
    parser.add_argument('-t', '--to', nargs=1, dest='STOP',
                        type=int, required=False,
                        help="Page number to stop at, defaulting at the end.")
    parser.add_argument('-v', '--verbose', dest='VERBOSE', action='store_true',
                        required=False,
                        help="Produces more feedback while running.")
    args = parser.parse_args()
    # Process arguments
    if args.VERBOSE:
        VERBOSE = args.VERBOSE
    FILENAME = args.FILENAME[0]
    if VERBOSE:
        print("Splicing file {}.".format(FILENAME))
    if FILENAME[-4:].lower() != '.pdf':
        print("Supplied file is not recognized as a .pdf - exiting.")
        exit()
    if args.START:
        SLICE_START = args.START[0] - 1
        if VERBOSE:
            print("Starting at page {}".format(SLICE_START + 1))
    if args.SPLIT:
        SLICE_SPLIT = args.SPLIT[0]
        if VERBOSE:
            print("Taking {} page(s) per slice.".format(SLICE_SPLIT))
    if args.STEP:
        SLICE_STEP = args.STEP[0]
        if VERBOSE:
            print("Skipping {} page(s) in between splits.".format(SLICE_STEP))
    if args.STOP:
        SLICE_STOP = args.STOP[0]
        if VERBOSE:
            print("Stopping at page {}.".format(SLICE_STOP))
    if args.VERBOSE:
        VERBOSE = args.VERBOSE
    # Check for any possible conflicts
    if SLICE_START > SLICE_STOP:
        print("Error: indicated start is after stopping point.")
        exit()


def pdf_slice(FILENAME, start, stop, number):
    """ Splice the given file from start to stop, appending number to name """
    # Load the original file
    global PDF_ORIGINAL_FILE
    global PDF_ORIGINAL_READER
    # Intialize the writer
    pdf_writer = PyPDF2.PdfFileWriter()
    # Loop through pages and slice out a selection
    for pagenum in range(start, stop):
        # Snatch the single page
        page_obj = PDF_ORIGINAL_READER.getPage(pagenum)
        # Add the page to a file to write
        pdf_writer.addPage(page_obj)
    # Write the object to a file, using the file name minus extension
    pdf_output_file = open(FILENAME[:-4] + str(number) + '.pdf', 'wb')
    pdf_writer.write(pdf_output_file)
    pdf_output_file.close()

# If run as a program, process command-line arguments
if __name__ == '__main__':
    main()
# Load the original file
PDF_ORIGINAL_FILE = open(FILENAME, 'rb')
PDF_ORIGINAL_READER = PyPDF2.PdfFileReader(PDF_ORIGINAL_FILE)
# Set the stopping point at the total number of pager
if SLICE_STOP == 0:
    SLICE_STOP = PDF_ORIGINAL_READER.numPages
# Variable to track number to add to file
iteration = 0
# Set up variable to iterate through the PDF file
page_start = SLICE_START
# Loop through the page range
for page in range(SLICE_START, SLICE_STOP, SLICE_SPLIT):
    iteration += 1
    # Calculate end of new slice, and limit if needed
    page_stop = page_start + SLICE_SPLIT
    if page_stop > PDF_ORIGINAL_READER.numPages:
        page_stop = PDF_ORIGINAL_READER.numPages
    # Call on the slice function to do the actual work
    if VERBOSE:
        print("Slicing pages {} to {} from file.".format(page_start+1, page_stop))
    pdf_slice(FILENAME, page_start, page_stop, iteration)
    # Increase the iteration
    page_start += SLICE_SPLIT + SLICE_STEP
    if page_start > PDF_ORIGINAL_READER.numPages:
        page_start = PDF_ORIGINAL_READER.numPages
    if page_stop == SLICE_STOP:
        break
PDF_ORIGINAL_FILE.close()
