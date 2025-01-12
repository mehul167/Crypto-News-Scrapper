# Crypto News Scraper

A Python-based web scraping tool that collects cryptocurrency news articles from major news sources including CoinDesk and Blockworks. The scraper automatically stores article data in MongoDB for easy access and analysis.

## Features

- 🔄 Automated news article scraping
- 📰 Multiple news source support:
  - CoinDesk (including various newsletters)
  - Blockworks
- 🗃️ MongoDB integration for data storage
- 🔄 Duplicate article detection
- 📸 Image URL extraction
- 🔗 Complete article metadata collection
- 🕒 Article date tracking

## Prerequisites

Before running this script, ensure you have the following installed:

```bash
pip install beautifulsoup4
pip install requests
pip install pymongo
pip install python-dotenv
pip install lxml
```

You'll also need:
- MongoDB server
- Python 3.x
- `.env` file with MongoDB connection string

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd crypto-news-scraper
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your MongoDB connection string:
```env
MONGODB_URL=mongodb://your-mongodb-connection-string
```

## Database Configuration

The scraper uses MongoDB with the following structure:
- Database name: `Scrapped_Data`
- Collection name: `coindesk`

## Usage

Run the script:

```bash
python main.py
```

The script will:
1. Scrape articles from multiple CoinDesk newsletters
2. Scrape articles from Blockworks news section
3. Store unique articles in MongoDB
4. Skip duplicate articles automatically

## Data Sources

### 1. CoinDesk
- The Node Newsletter
- First Mover Newsletter
- Crypto Long & Short Newsletter
- The Protocol Newsletter
- Crypto for Advisors Newsletter

### 2. Blockworks
- Main news section
- Complete article metadata

## Data Schema

Each article is stored with the following structure:
```json
{
    "Title": "string",
    "Description": "string",
    "Date": "string",
    "image_url": "string",
    "source": "string",
    "post_url": "string",
    "logo_url": "string"
}
```

## Features in Detail

### Article Deduplication
- Checks for existing articles before insertion
- Prevents duplicate entries
- Uses complete document comparison

### Image Handling
- Extracts high-quality article images
- Stores both article and source logos
- Handles different image URL formats

### Error Handling
- User agent simulation
- Request error handling
- Encoding configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
