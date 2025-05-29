# Replit Bounty Scraper

Automated scraper that monitors Replit bounties and sends Telegram notifications for new postings.

## Features

- Scrapes Replit bounties page using Playwright headless browser
- Detects new bounties by comparing with previous runs
- Sends individual Telegram notifications for each new bounty
- Runs automatically every 15 minutes via GitHub Actions
- Stores only last 10 bounties for efficient comparison

## Setup

### 1. Telegram Bot Setup

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Save the bot token
4. Add bot to your chat/channel and get chat ID:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

### 2. GitHub Repository Setup

1. Fork/clone this repository
2. Go to Settings → Secrets and variables → Actions
3. Add repository secrets:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat/channel ID

### 3. Local Development Setup

```bash
# Clone repository
git clone <repo-url>
cd replit-bounty-scraper

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Run scraper
python scraper.py
```

## File Structure

```
├── scraper.py              # Main scraping logic
├── requirements.txt        # Python dependencies
├── test_scraper.py        # Test suite
├── .github/workflows/
│   └── bounty_scraper.yml # GitHub Actions workflow
├── last_bounties.json     # Storage file (auto-generated)
└── README.md              # This documentation
```

## How It Works

### Scraping Process
1. Launches headless Chromium browser
2. Navigates to Replit bounties page
3. Waits for JavaScript to load bounty cards
4. Extracts bounty data (title, price, author, description, link)
5. Generates unique IDs for comparison

### New Bounty Detection
1. Loads previously stored bounties from `last_bounties.json`
2. Compares current bounties with previous ones using unique IDs
3. Identifies new bounties not seen before
4. Sends Telegram notification for each new bounty

### Storage Management
- Keeps only last 10 bounties to minimize storage
- Updates storage file after each run
- GitHub Actions commits storage file to repository

## Testing

Run the test suite:

```bash
python test_scraper.py
```

### Test Coverage
- New bounty detection logic
- Storage operations (save/load)
- Telegram notification formatting
- Data structure validation

### Manual Testing

Set environment variables and uncomment the live testing section in `test_scraper.py`:

```python
# Uncomment to test live scraping
asyncio.run(test_live_scraping())
```

## Monitoring

### GitHub Actions
- Check Actions tab for run history
- View logs for debugging
- Manual trigger available via "Run workflow" button

### Notification Format
Each bounty notification includes:
- Title
- Price
- Author
- Description (truncated to 200 chars)
- Link
- Timestamp

## Troubleshooting

### Common Issues

**No bounties found:**
- Check if Replit changed their page structure
- Verify CSS selectors in `_extract_bounty_data()`
- Check browser logs in GitHub Actions

**Telegram notifications not sending:**
- Verify bot token and chat ID
- Check bot permissions in target chat
- Review Telegram API response in logs

**GitHub Actions failing:**
- Check secrets are properly set
- Verify workflow file syntax
- Review action logs for specific errors

### Debugging

Enable verbose logging by modifying the scraper:

```python
# Add at the top of scraper.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Run

Test locally before relying on automation:

```bash
python scraper.py
```

## Customization

### Scraping Frequency
Modify cron schedule in `.github/workflows/bounty_scraper.yml`:

```yaml
schedule:
  - cron: '*/30 * * * *'  # Every 30 minutes
```

### Bounty Limit
Change limit in `scrape_bounties()` call:

```python
current_bounties = await self.scrape_bounties(limit=20)
```

### Notification Format
Modify message template in `send_telegram_notification()` method.

## Security Notes

- Bot token and chat ID are stored as GitHub secrets
- No sensitive data is logged
- Storage file contains only public bounty information

## License

MIT License - feel free to modify and distribute.