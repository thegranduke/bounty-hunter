import asyncpg
import os
from typing import List, Dict
from datetime import datetime

class Database:
    def __init__(self):
        self.pool = None
        
    async def connect(self):
        """Connect to the database and create pool"""
        if not self.pool:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL environment variable is not set")
            
            self.pool = await asyncpg.create_pool(database_url)
            
            # Create table if it doesn't exist
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS bounties (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        price TEXT NOT NULL,
                        description TEXT,
                        author TEXT,
                        link TEXT,
                        time_info TEXT,
                        status TEXT,
                        cycles TEXT,
                        scraped_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
    
    async def close(self):
        """Close the database connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    async def save_bounties(self, bounties: List[Dict]):
        """Save bounties to database, replacing all existing ones"""
        if not self.pool:
            await self.connect()
            
        async with self.pool.acquire() as conn:
            # Start a transaction
            async with conn.transaction():
                # First, delete all existing bounties
                await conn.execute('DELETE FROM bounties')
                
                # Then insert the new bounties
                for bounty in bounties:
                    await conn.execute('''
                        INSERT INTO bounties (
                            id, title, price, description, author, link, 
                            time_info, status, cycles, scraped_at
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ''', 
                    bounty['id'],  # Store ID as text
                    bounty['title'],
                    bounty['price'],
                    bounty['description'],
                    bounty['author'],
                    bounty['link'],
                    bounty['time_info'],
                    bounty['status'],
                    bounty['cycles'],
                    datetime.fromisoformat(bounty['scraped_at'])
                    )
    
    async def get_previous_bounties(self) -> List[Dict]:
        """Get all stored bounties"""
        if not self.pool:
            await self.connect()
            
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM bounties 
                ORDER BY scraped_at DESC
            ''')
            
            return [dict(row) for row in rows] 