# Sample Python Modules
Some sample python modules I created just for practice and to give a glimpse into my coding style

## PDF Splitting

### Description: Using pypdf library to split pdfs into single pages or page ranges

```
Program: pdf_splitting.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/pdf_splitting.py <commands>
  -h/--help             show this help message
  -i/--input_pdf        full/relative path to input file
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
  -u/--url              website url
```

### Output

## Dynamic Scraping

### Description: Web Scraping modules for dynamic javascript websites on chrome

```
Program: dynamic_web_scraping.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/web_scraping.py <commands>
  -h/--help             show this help message
  -u/--url              website url
```

### Output

### To Do
  - user action simulation (button clicks, search bars, etc...)
  - handle exceptions for each library method used in the constructor of the ChromeScraper class

## Pandas Dataframe Manipulation

### Read dataframe of school subjects offered for certain districts and perform the following operations:
  - Drop rows/ schools that offer fewer than <min_subjects> subjects
  - remove non alpha-numeric characters from the school_code column
  - create data frame with total number of schools offering each <query_subjects> per district

```
Program: pandas_df_manipulation.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/pandas_df_manipulation.py <commands>
  -h/--help                 show this help message
  -i/--input_csv            full path to csv input file
  -m/--min_subjects         minimum school subjects offered
  -s/--query_subjects       subjects to counts for output df
```

### Output
  - returns new dataframe

## Important Words Search

### Search the text for words occurring at least k times and return array of words in order of occurrence in the original string
  - At least one word meets the criteria
  - the string is space separated
  - Drop rows/ schools that offer fewer than <min_subjects> subjects
```
Program: important_words.py
Version 1.0.0 (python 3.6+ compatible)
Usage: python src/important_words.py <commands>
  -h/--help                 show this help message
  -i/--input_csv            full path to csv input file
  -m/--min_subjects         minimum school subjects offered
  -s/--query_subjects       subjects to counts for output df
```

### Output
  - returns new dataframe


### Env Setup 

```
% python3 -m venv .venv
% pip install -r requirements
```

### Run Unit Tests
```
% coverage run --source=./src -m pytest && coverage report -m
```

### Coverage
```
======================================================================================================= 22 passed in 0.71s ========================================================================================================
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
src/__init__.py                     0      0   100%
src/dynamic_web_scraping.py        51      9    82%   78-89, 92-96
src/important_words.py             14      5    64%   30-34
src/pandas_df_manipulation.py      32      6    81%   53-58
src/pdf_splitting.py               53     11    79%   76-79, 83-89
src/shared.py                       3      0   100%
src/static_web_scraping.py         29      7    76%   44-45, 49-53
-------------------------------------------------------------
TOTAL                             182     38    79%
```