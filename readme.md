# pdf_slicer.py

This program slices up a pdf into separate pages. It can be used to extract just a single set of pages or to split an entire pdf up into sections.

## Command-line Options
**-h, --help**  show the help message
**-f [page], --from [page]**  Page to start from, counting up from 0.
**-p [pages], --pages [pages]** Number of pages to slice the pdf into, i.e. pages per subset
**-s [pages], --skip [pages]**  Set this option to skip pages between sub-set.
**-t [page], --to [page]**  Page to stop at, defaulting at the end.
**-v, --verbose** Produces more feedback while running
