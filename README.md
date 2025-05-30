# Replit Bounty Hunter 🎯

An automated scraper that monitors Replit's bounty page and sends notifications for new bounties via Telegram. Built with Python, Playwright, and Neon PostgreSQL.

## Features

- 🔄 Automatically scrapes Replit's bounty page every 15 minutes
- 📊 Stores bounty data in Neon PostgreSQL database
- 🔔 Sends notifications for new bounties via Telegram
- 🎯 Intelligent duplicate detection to prevent repeat notifications
- 🕒 Human-readable timestamps in notifications
- 🚀 Runs automatically via GitHub Actions

## Prerequisites

- Python 3.11 or higher
- A Telegram bot token and chat ID
- A Neon PostgreSQL database
- GitHub account (for automated running)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thegranduke/bounty-hunter.git
cd bounty-hunter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

3. Create a `.env` file in the project root with your credentials:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
DATABASE_URL=your_neon_database_url
```

## Configuration

### Database Setup
The application uses Neon PostgreSQL to store bounty data. The database schema will be automatically created on first run, including:
- Bounty details (title, price, description, etc.)
- Timestamps for tracking
- Unique constraints to prevent duplicates

### GitHub Actions
The scraper runs automatically every 15 minutes using GitHub Actions. To set this up:

1. Fork this repository
2. Add the following secrets to your GitHub repository:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `DATABASE_URL`
3. The workflow will automatically start running

## Usage

### Running Locally
```bash
python scraper.py
```

### Manual Trigger
You can manually trigger the GitHub Action workflow through the Actions tab in your repository.

## Notification Format

Notifications are sent to Telegram in the following format:
```
🎯 New Replit Bounty!

Title: [Bounty Title]
Price: [Price]
Author: [Author Name]
Description: [Description]
Link: [Bounty URL]
Posted: March 14, 2024 at 02:30 PM
```

## How It Works

1. **Scraping**: Uses Playwright to scrape the Replit bounties page
2. **Storage**: Stores the latest 10 bounties in Neon PostgreSQL
3. **Comparison**: Compares new bounties against stored ones using:
   - Author
   - Price
   - Link
   - Description
4. **Notification**: Sends Telegram notifications only for truly new bounties

## Project Structure

```
bounty-hunter/
├── .github/
│   └── workflows/
│       └── bounty_scraper.yml  # GitHub Actions workflow
├── scraper.py                  # Main scraper logic
├── db.py                       # Database operations
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
└── README.md                   # This file
```

## Dependencies

- `playwright`: Web scraping and automation
- `asyncpg`: PostgreSQL database operations
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for Telegram API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.