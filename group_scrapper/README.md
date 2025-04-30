# Facebook Group Scraper

A Python tool to search for Facebook groups based on keywords and save the results.

## Features

- Automated login to Facebook using Selenium for reliable authentication
- Search for Facebook groups using keywords
- Limit the number of search results
- Save results to a text file

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Download and install ChromeDriver:
   - Download the appropriate version of ChromeDriver from [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)
   - Make sure the ChromeDriver version matches your Chrome browser version
   - Add ChromeDriver to your system PATH or place it in the project directory

## Usage

### Login to Facebook

Before searching for groups, you need to login and save your Facebook cookies:

```
python main.py --login
```

You will be prompted to enter your Facebook email and password. A Chrome browser window will open for authentication. If Facebook requires additional verification, you'll be prompted to complete those steps in the browser window before continuing.

The cookies will be saved to `facebook_cookies.pkl` in the root directory.

### Search for Groups

To search for Facebook groups using a keyword:

```
python main.py --search "your keyword"
```

By default, the tool will fetch up to 50 results. You can change this limit:

```
python main.py --search "your keyword" --limit 100
```

The search process will open a Chrome browser window and automatically scroll through search results to find groups matching your keyword. The results will be saved to `result.txt` in the current directory.

## Notes

- Facebook's website structure may change over time, which could affect the scraper's functionality.
- Use responsibly and in accordance with Facebook's terms of service.
- This tool is for educational purposes only.

## Requirements

- Python 3.6+
- requests
- beautifulsoup4