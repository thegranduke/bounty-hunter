import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright
import requests

class BountyScraper:
    def __init__(self, telegram_bot_token: str, telegram_chat_id: str):
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.storage_file = "last_bounties.json"
        
    async def scrape_bounties(self, limit: int = 15) -> List[Dict]:
        """Scrape bounties from Replit bounties page"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                print("Navigating to bounties page...")
                # Wait for network idle and longer timeout
                response = await page.goto(
                    "https://replit.com/bounties?order=creationDateDescending",
                    wait_until="networkidle",
                    timeout=30000
                )
                print(f"Page loaded with status: {response.status}")
                
                # Wait for key elements that indicate JS has loaded
                print("Waiting for JavaScript content to load...")
                try:
                    # Wait for the search input to be present
                    await page.wait_for_selector('input[placeholder="Search for a Bounty"]', timeout=30000)
                    print("Found search input")
                except Exception as e:
                    print(f"Warning: Could not find search input: {e}")
                
                # Additional wait for dynamic content
                await page.wait_for_timeout(8000)
                
                # # Take screenshot of current state
                # await page.screenshot(path='1_after_load.png')
                
                print("Looking for bounty cards...")
                # Try multiple selectors in order of specificity
                selectors = [
                    '.Surface_surfaceRoot__TeA2u.css-r1hogs',
                    'li[class*="Surface_surfaceRoot"]',
                    'li[class*="useView_view"]',
                    'li'
                ]
                
                bounty_cards = []
                for selector in selectors:
                    bounty_cards = await page.query_selector_all(selector)
                    print(f"Trying selector '{selector}': found {len(bounty_cards)} elements")
                    if len(bounty_cards) > 0:
                        print(f"Using selector: {selector}")
                        break
                
                # Save page state for debugging
                page_content = await page.content()
                with open('page_content.html', 'w', encoding='utf-8') as f:
                    f.write(page_content)
                
                bounties = []
                for i, card in enumerate(bounty_cards[:limit]):
                    if i >= limit:
                        break
                    
                    bounty = await self._extract_bounty_data(card)
                    if bounty:
                        bounties.append(bounty)
                
                return bounties
                
            except Exception as e:
                print(f"Error scraping bounties: {e}")
                try:
                    await page.screenshot(path='error_screenshot.png')
                    print("Error screenshot saved as error_screenshot.png")
                except:
                    print("Failed to save error screenshot")
                return []
            finally:
                await context.close()
                await browser.close()
    
    async def _extract_bounty_data(self, card) -> Optional[Dict]:
        """Extract bounty data from a card element"""
        try:
            # Title is in an h3 element with a link
            title_elem = await card.query_selector('h3 a')
            title = await title_elem.inner_text() if title_elem else "No title"
            
            # Price is in the first span with css-4qqdjk class
            price_elem = await card.query_selector('.css-4qqdjk')
            price = await price_elem.inner_text() if price_elem else "Price not found"
            
            # Description is in a span after the h3
            desc_elem = await card.query_selector('h3 + span.Text_text__T_hn_')
            description = await desc_elem.inner_text() if desc_elem else "No description"
            
            # Link is in the h3 a element
            link_elem = await card.query_selector('h3 a')
            link = await link_elem.get_attribute('href') if link_elem else None
            if link and not link.startswith('http'):
                link = f"https://replit.com{link}"
            
            # Author is in the link with css-1yzry6v class
            author_elem = await card.query_selector('.css-1yzry6v span.Text_text__T_hn_')
            author = await author_elem.inner_text() if author_elem else "Unknown author"

            # Get additional data like time remaining and status
            time_elem = await card.query_selector('.css-149xez1 span')
            time_info = await time_elem.inner_text() if time_elem else ""

            status_elem = await card.query_selector('.Surface_surfaceDefault__TcNI5 span')
            status = await status_elem.inner_text() if status_elem else "Unknown status"

            # Get cycles amount if available
            cycles_elem = await card.query_selector('.css-pvu419 span')
            cycles = await cycles_elem.inner_text() if cycles_elem else "0"
            
            return {
                'title': title.strip(),
                'price': price.strip(),
                'description': description.strip()[:200] + "..." if len(description.strip()) > 200 else description.strip(),
                'author': author.strip(),
                'link': link,
                'time_info': time_info.strip(),
                'status': status.strip(),
                'cycles': cycles.strip(),
                'scraped_at': datetime.now().isoformat(),
                'id': hash(f"{title}{price}{author}")  # Simple ID generation
            }
        except Exception as e:
            print(f"Error extracting bounty data: {e}")
            return None
    
    def load_previous_bounties(self) -> List[Dict]:
        """Load previously scraped bounties from storage"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def save_bounties(self, bounties: List[Dict]):
        """Save bounties to storage (keep only last 10)"""
        bounties_to_save = bounties[:10]  # Keep only last 10
        with open(self.storage_file, 'w') as f:
            json.dump(bounties_to_save, f, indent=2)
    
    def find_new_bounties(self, current_bounties: List[Dict], previous_bounties: List[Dict]) -> List[Dict]:
        """Find new bounties by comparing current with previous"""
        previous_ids = {bounty['id'] for bounty in previous_bounties}
        return [bounty for bounty in current_bounties if bounty['id'] not in previous_ids]
    
    def send_telegram_notification(self, bounty: Dict):
        """Send a single bounty notification to Telegram"""
        message = f"""🎯 **New Replit Bounty!**

**Title:** {bounty['title']}
**Price:** {bounty['price']}
**Author:** {bounty['author']}
**Description:** {bounty['description']}
**Link:** {bounty['link'] or 'No link available'}
**Posted:** {bounty['scraped_at']}

---"""
        
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        data = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Sent notification for: {bounty['title']}")
            else:
                print(f"❌ Failed to send notification: {response.text}")
        except Exception as e:
            print(f"❌ Error sending notification: {e}")
    
    async def run(self):
        """Main execution method"""
        print("🔍 Starting bounty scraper...")
        
        # Load previous bounties
        previous_bounties = self.load_previous_bounties()
        print(f"📚 Loaded {len(previous_bounties)} previous bounties")
        
        # Scrape current bounties
        current_bounties = await self.scrape_bounties()
        print(f"🔍 Found {len(current_bounties)} current bounties")
        
        if not current_bounties:
            print("❌ No bounties found, skipping...")
            return
        
        # Find new bounties
        new_bounties = self.find_new_bounties(current_bounties, previous_bounties)
        print(f"🆕 Found {len(new_bounties)} new bounties")
        
        # Send notifications for new bounties
        for bounty in new_bounties:
            self.send_telegram_notification(bounty)
        
        # Save current bounties for next run
        self.save_bounties(current_bounties)
        print("💾 Saved current bounties for next comparison")

async def main():
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not telegram_bot_token or not telegram_chat_id:
        print("❌ Missing required environment variables:")
        print("   - TELEGRAM_BOT_TOKEN")
        print("   - TELEGRAM_CHAT_ID")
        return
    
    scraper = BountyScraper(telegram_bot_token, telegram_chat_id)
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())