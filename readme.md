# JUPAS Website Scraper

A python web scraper designed to scrap JUPAS website automatically to fetch the entry requirements of every UGC university programme offered.

## Prerequisite
This scraper uses two pip packages: bs4 (BeautifulSoup, for parsing HTML files) and tqdm (for displaying progress bar). The required packages were specified in the ```requirements.txt``` file.

## Usage
After installing the required packages, run ```python3 scrap.py```

## Results

Each program will be represented in a JSON object in the following format:

```javascript
    {
        "code": The jupas code for the programme,
        "school": Name of the university,
        "chineseName": Chinese name of the programme,
        "englishName": English name of the programme,
        "requirements": An object storing the entry requirements of the subject
    }
```

The ```requirements``` object were made by key-value pairs, where the key represents the subject, and the value represents the grade required. Grade 5* is represented by 6 and 5** is represented by 7. If the applicants were required to attain a certain grade in one of many subjects, these subjects were represented in a single key-value pair, with the key including all subjects seperated by space.

The subjects were represented by the abbreviated subject codes for easier processing. To find the corresponding full name of subjects, please refer to ```info.json``` and look into the ```electiveNames``` object.

## Tested Scenarios
This program was used to scrape the 2020 JUPAS programme entry requirements in between April 2020 to May 2020. There is no guarantee that this scraper will continue to work in later years.
