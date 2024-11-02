import json
import os
import asyncio
from playwright.async_api import async_playwright

# File path for storing bounties
LOCAL_FILE_PATH = './bounties.json'

async def fetch_bounties():
    async with async_playwright() as p:
        # Launch browser with minimal arguments for compatibility
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox']
        )
        
        context = await browser.new_context()
        page = await context.new_page()
        
        url = 'https://replit.com/bounties?status=open&order=creationDateDescending'
        print(f"Fetching bounties from {url}")
        
        try:
            await page.goto(url, timeout=60000)
            
            print("Waiting for bounties to load...")
            await page.wait_for_selector('.css-e1ns7d', timeout=60000)
            
            # Get all bounty elements
            bounties = await page.query_selector_all('.css-e1ns7d')
            print(f"Found {len(bounties)} bounty elements")
            
            bounty_data = []
            
            # Process first 20 bounties
            for idx, bounty in enumerate(bounties[:20]):
                try:
                    # Using simpler selectors and data extraction
                    id_elem = await bounty.query_selector('.css-1om7s53')
                    price_elem = await bounty.query_selector('.css-19oru95')
                    desc_elem = await bounty.query_selector('.css-10z1dta')
                    
                    # Extract text content
                    bounty_id = await id_elem.text_content() if id_elem else None
                    price = await price_elem.text_content() if price_elem else None
                    description = await desc_elem.text_content() if desc_elem else None
                    
                    if bounty_id and price and description:
                        bounty_data.append({
                            'id': bounty_id.strip(),
                            'price': price.strip(),
                            'text': description.strip()
                        })
                        print(f"Processed bounty {idx + 1}: {bounty_id.strip()}")
                        
                except Exception as e:
                    print(f"Error processing bounty {idx + 1}: {e}")
                    continue
            
            print(f"Successfully processed {len(bounty_data)} bounties")
            return bounty_data
            
        except Exception as e:
            print(f"Error during bounty fetching: {e}")
            try:
                await page.screenshot(path='error.png')
            except:
                pass
            return []
            
        finally:
            print("Cleaning up browser resources...")
            await context.close()
            await browser.close()

def read_bounties_from_file():
    if os.path.exists(LOCAL_FILE_PATH):
        with open(LOCAL_FILE_PATH, 'r') as f:
            return json.load(f)
    return []

def write_bounties_to_file(bounty_data):
    with open(LOCAL_FILE_PATH, 'w') as f:
        json.dump(bounty_data, f, indent=2)

async def main():
    try:
        print("Starting bounty checker...")
        
        # Fetch current bounties
        current_bounties = await fetch_bounties()
        
        if not current_bounties:
            print("No bounties fetched, possibly an error occurred")
            return
            
        # Read previous bounties
        previous_bounties = read_bounties_from_file()
        
        # Compare and find new bounties
        previous_bounty_ids = {bounty['id'] for bounty in previous_bounties}
        new_bounties = [bounty for bounty in current_bounties 
                       if bounty['id'] not in previous_bounty_ids]
        
        # Report results
        if new_bounties:
            print(f"\nFound {len(new_bounties)} new bounties:")
            for bounty in new_bounties:
                print(f"- {bounty['id']}: {bounty['price']}")
            write_bounties_to_file(current_bounties)
        else:
            print("\nNo new bounties found")
            
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())