# Scopus-h-index-Scraper
A simple web scrapping script (able to handle CloudFlare) to extract h-index, citations &amp; number of publications from Scopus Author Profile

An input file (Excel xlsx) must be prepared beforehand with the Authors Lastname, Firstname and Affiliation.
# Requirements
Python 3, Pandas, Seleniumbase

# General Notes
1. There is even more efficient way of doing this, by using Scopus API. For more detail, please visit https://dev.elsevier.com/, However, you need to be connected to an institution that is registered with Scopus
2. If the search finds multiple authors or author has no Scopus profile an Error message is placed in the output.
