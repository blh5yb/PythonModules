# Sample Python Modules
Some sample python modules I created just for practice and to give a glimpse into my coding style

## PDF Splitting

### Description: Using pypdf library to split pdfs into single pages or page ranges

```
Program: pdf_splitting.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/pdf_splitting.py <commands>
  -h/--help             show this help message
  -i/input_pdf          full/relative path to input file
  -o/--out_folder       full/relative path output folder
  -p/--out_prefix       output file prefix (i.e out_file)
```

### Output
  - single pages method: \<out_folder\>\/\<out_prefix\>_\<page_number\>.pdf
  - page range method:  \<out_folder\>\/\<out_prefix\>.pdf

### To Do
  - Exception handling for page numbers outside range of input pdf

## Static Scraping

### Description: Web Scraping modules for static html websites

```
Program: static_web_scraping.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/web_scraping.py <commands>
  -h/--help             show this help message
  -u/url                website url
```

### Output

## Dynamic Scraping

### Description: Web Scraping modules for dynamic javascript websites on chrome

```
Program: dynamic_web_scraping.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/web_scraping.py <commands>
  -h/--help             show this help message
  -u/url                website url
```

### Output

### To Do
  - user action simulation (button clicks, search bars, etc...)
  - handle exceptions for each library method used in the constructor of the ChromeScraper class

### Env Setup 

```
% python3 -m venv .venv
% pip install -r requirements
```

### Run Unit Tests
```
coverage run --source=./src -m pytest && coverage report -m
```

### Coverage
```
======================================================================================================= 18 passed in 0.29s ========================================================================================================
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/__init__.py                   0      0   100%
src/dynamic_web_scraping.py      51      9    82%   63-74, 77-81
src/pdf_splitting.py             55     11    80%   79-84, 88-99
src/shared.py                     3      0   100%
src/static_web_scraping.py       29      7    76%   35-36, 40-44
-----------------------------------------------------------
TOTAL                           138     27    80%
```