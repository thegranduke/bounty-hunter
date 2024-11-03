import json
import os
import asyncio
from playwright.async_api import async_playwright

# File path for storing bounties - Changed to use /tmp for Lambda
LOCAL_FILE_PATH = '/tmp/bounties.json'

async def fetch_bounties():
    async with async_playwright() as p:
        # Launch browser with Lambda-compatible arguments
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']  # Added flag for Lambda
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        page = await context.new_page()
        
        url = 'https://replit.com/bounties?status=open&order=creationDateDescending'
        print(f"Fetching bounties from {url}")
        
        try:
            await page.goto(url, timeout=60000)
            
            print("Waiting for bounties to load...")
            await page.wait_for_selector('.css-e1ns7d', timeout=60000)
            
            bounties = await page.query_selector_all('.css-e1ns7d')
            print(f"Found {len(bounties)} bounty elements")
            
            bounty_data = []
            
            for idx, bounty in enumerate(bounties[:20]):
                try:
                    id_elem = await bounty.query_selector('.css-1om7s53')
                    price_elem = await bounty.query_selector('.css-19oru95')
                    desc_elem = await bounty.query_selector('.css-10z1dta')
                    
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
                await page.screenshot(path='/tmp/error.png')  # Changed screenshot path to /tmp
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

async def async_lambda_handler(event, context):
    try:
        print("Starting bounty checker...")
        
        current_bounties = await fetch_bounties()
        
        if not current_bounties:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No bounties fetched, possibly an error occurred'})
            }
            
        previous_bounties = read_bounties_from_file()
        
        previous_bounty_ids = {bounty['id'] for bounty in previous_bounties}
        new_bounties = [bounty for bounty in current_bounties 
                       if bounty['id'] not in previous_bounty_ids]
        
        if new_bounties:
            latest_bounty = new_bounties[0]  # Fixed variable declaration order
            number_of_bounties = len(new_bounties)
            bounty_message = f"{number_of_bounties} new bounties\n- Latest bounty: {latest_bounty['id']}: {latest_bounty['price']} - \n{latest_bounty['text']}"
            write_bounties_to_file(current_bounties)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': bounty_message,
                    'new_bounties': new_bounties
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No new bounties found'})
            }
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def lambda_handler(event, context):
    """Main Lambda handler function"""
    return asyncio.get_event_loop().run_until_complete(async_lambda_handler(event, context))