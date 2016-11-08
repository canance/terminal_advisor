# terminal_advisor.py

## Summary 

This script aims to automate mundane tasks in Webadvisor for faculty advisors.  The following tasks are currently supported:
- **Remove an advisement hold** - Removes the advisement hold from an advisee's account
- **Run a program evaluation** - Runs a program evaluation for the active program listed in Webadvisor.  The program evaluation is converted to pdf and stored in your current working directory.
- **Advisee search** - Search for an advisee using part of his/her name or student id number


## Dependencies
- [Python 3](https://www.python.org/downloads/)
  - bs4
  - configparser
  - keyring
  - pdfkit
  - selenium
- [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html)
- Selenium WebDriver
  - [PhantomJS](http://phantomjs.org/download.html)
  - [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Installation
1. Install [wkhtmltopdf](http://wkhtmltopdf.org/downloads.html) for your Operating System
2. Install a web driver for your Operating System:
    - [PhantomJS](http://phantomjs.org/download.html)
    - [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
3. Install [Python 3](https://www.python.org/downloads/)
4. Install [pip](https://pip.pypa.io/en/stable/installing/)
5. Run ```python setup.py install```

## Usage
```
usage: terminal_advisor.py [-h] [--user USER] [--base-url BASE_URL]
                           [--config CONFIG] [--driver [{PhantomJS,Chrome}]]
                           [-s] [-r] [-e]
                           [advisee]

Automate mundane tasks in Webadvisor

positional arguments:
  advisee               An advisee's name or student ID number.

optional arguments:
  -h, --help            show this help message and exit
  --user USER           User name to log in to webadvisor
  --base-url BASE_URL   Base URL for webadvisor. Example: https://wa.xyz.edu/
  --config CONFIG       Path to a configuration file
  --driver [{PhantomJS,Chrome}]
                        Webdriver to use with Selenium
  -s, --save-config     Save configuration file
  -r, --remove-hold     Remove the advisement hold
  -e, --program-eval    Run a program evaluation

```

## Future Development
- TBD




