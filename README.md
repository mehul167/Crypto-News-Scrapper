# Crypto News Scrapper

This Python script demonstrates web scraping from Coindesk and Blockworks websites and stores the scraped data into a MongoDB database.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)


## Overview

The script `scrapper.py` scrapes data from two websites:
- [Coindesk](https://www.coindesk.com/)
- [Blockworks](https://blockworks.co/)

It extracts article titles, descriptions, image URLs, source URLs, and timestamps, then stores this data in separate collections within a MongoDB database.

## Requirements

To run this script, ensure you have the following installed:

- Python 3.x
- Required Python packages (`requests`, `beautifulsoup4`, `pymongo`, `python-dotenv`)


