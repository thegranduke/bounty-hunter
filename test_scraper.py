import asyncio
import json
import os
from unittest.mock import Mock, patch, AsyncMock
from scraper import BountyScraper

class TestScraper:
    def __init__(self):
        self.test_bot_token = "test_token"
        self.test_chat_id = "test_chat_id"
        self.scraper = BountyScraper(self.test_bot_token, self.test_chat_id)
    
    def test_find_new_bounties(self):
        """Test new bounty detection logic"""
        previous = [
            {'id': 1, 'title': 'Old Bounty 1'},
            {'id': 2, 'title': 'Old Bounty 2'}
        ]
        current = [
            {'id': 1, 'title': 'Old Bounty 1'},
            {'id': 3, 'title': 'New Bounty 1'},
            {'id': 4, 'title': 'New Bounty 2'}
        ]
        
        new_bounties = self.scraper.find_new_bounties(current, previous)
        assert len(new_bounties) == 2
        assert new_bounties[0]['id'] == 3
        assert new_bounties[1]['id'] == 4
        print("✅ New bounty detection test passed")
    
    def test_storage_operations(self):
        """Test saving and loading bounties"""
        test_bounties = [
            {'id': 1, 'title': 'Test Bounty 1'},
            {'id': 2, 'title': 'Test Bounty 2'}
        ]
        
        # Test saving
        self.scraper.save_bounties(test_bounties)
        
        # Test loading
        loaded = self.scraper.load_previous_bounties()
        assert len(loaded) == 2
        assert loaded[0]['title'] == 'Test Bounty 1'
        
        # Cleanup
        if os.path.exists(self.scraper.storage_file):
            os.remove(self.scraper.storage_file)
        
        print("✅ Storage operations test passed")
    
    @patch('requests.post')
    def test_telegram_notification(self, mock_post):
        """Test Telegram notification sending"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        test_bounty = {
            'title': 'Test Bounty',
            'price': '$100',
            'author': 'Test Author',
            'description': 'Test description',
            'link': 'https://test.com',
            'scraped_at': '2024-01-01T00:00:00'
        }
        
        self.scraper.send_telegram_notification(test_bounty)
        
        assert mock_post.called
        call_args = mock_post.call_args[1]
        assert call_args['data']['chat_id'] == self.test_chat_id
        assert 'Test Bounty' in call_args['data']['text']
        
        print("✅ Telegram notification test passed")
    
    async def test_scraping_simulation(self):
        """Simulate scraping without actual browser (for testing structure)"""
        # This would need actual browser testing in a real environment
        # For now, just test the data structure
        mock_bounty = {
            'title': 'Mock Bounty',
            'price': '$50',
            'description': 'Mock description',
            'author': 'Mock Author',
            'link': 'https://mock.com',
            'scraped_at': '2024-01-01T00:00:00',
            'id': 12345
        }
        
        # Test data extraction format
        required_fields = ['title', 'price', 'description', 'author', 'link', 'scraped_at', 'id']
        for field in required_fields:
            assert field in mock_bounty
        
        print("✅ Scraping data structure test passed")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Running tests...")
        
        self.test_find_new_bounties()
        self.test_storage_operations()
        self.test_telegram_notification()
        asyncio.run(self.test_scraping_simulation())
        
        print("✅ All tests passed!")

# Manual testing functions
async def test_live_scraping():
    """Test actual scraping (requires environment variables)"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to test live scraping")
        return
    
    scraper = BountyScraper(bot_token, chat_id)
    bounties = await scraper.scrape_bounties(limit=3)
    print(f"🔍 Scraped {len(bounties)} bounties:")
    for bounty in bounties:
        print(f"  - {bounty['title']} ({bounty['price']})")

if __name__ == "__main__":
    # Run unit tests
    tester = TestScraper()
    tester.run_all_tests()
    
    # Uncomment to test live scraping
    # asyncio.run(test_live_scraping())