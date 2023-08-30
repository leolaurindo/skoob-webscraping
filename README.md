# Skoob Scraper

[🇧🇷 Check the brazilian portuguese version of this read me here 🇧🇷](./README_PT-BR.md)


## Overview

This script logs into [Skoob](https://www.skoob.com.br/), a Brazilian "social network" for book lovers and retrieves the user's bookshelf data in csv and excel spreadsheet file.

## About this script

This script came to me when a friend of mine said she was having some trouble transferring her book's data to her notion notebook. As I was studying web scraping for the new job I've landed, I accepted the comment as a challenge. In the end, I made this script.

It is already one or two months old, and I think I can modularize the tasks into functions. Because I am lazy, I tried to do it with chatGPT, but it only made things worse. I will eventually do it, but for now I'll leave this as it is. You can, of course, make the changes you want for yourself.

For now, it uses `selenium` for interacting with the web page elements and its `html` as well as `pandas` for processing the data retrieved into a `dataframe` format.

## Installation

You can simply execute `setupt_environment.bat` or follow the steps below:

First, clone your repository to your local machine using `git clone`

```
git clone https://github.com/leolaurindo/skoob-webscraping.git
```

Then, install the required python packages

```
pip install -r requirements.txt
```

You will also need `google chrome` installed and the `chrome-driver.exe` for its current version. You can download Chrome on its [main page](https://www.google.com/intl/pt-BR/chrome/) and the chrome-driver from [here](https://googlechromelabs.github.io/chrome-for-testing/)

## Configuration

The script uses `config.json` for managing paths and passwords. You can replace the `config.json.sample` with your own credentials and remove the `sample` format.

## Running the script

Navigate to the cloned directory and run

```
python main.py
```

# License

You can use it however you want.
