"""Rate Limiter Utility

This module provides rate limiting functionality to ensure ethical scraping
and compliance with API rate limits.
"""

import asyncio
import time
from typing import Dict, Optional
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_second: float = 1.0):
        """
        Initialize rate limiter
        
        Args:
            requests_per_second (float): Maximum requests per second allowed
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second if requests_per_second > 0 else 0
        self.last_request_time: Dict[str, float] = defaultdict(float)
        self._lock = asyncio.Lock()
    
    async def wait_if_needed(self, domain: str = "default"):
        """
        Wait if needed to respect rate limits
        
        Args:
            domain (str): Domain or service identifier for separate rate limiting
        """
        async with self._lock:
            current_time = time.time()
            last_time = self.last_request_time[domain]
            
            if current_time - last_time < self.min_interval:
                sleep_time = self.min_interval - (current_time - last_time)
                await asyncio.sleep(sleep_time)
                
            self.last_request_time[domain] = time.time()

# Global rate limiter instance
rate_limiter = RateLimiter(1.0)  # 1 request per second default

async def rate_limit(domain: str = "default"):
    """Simple rate limiting function"""
    await rate_limiter.wait_if_needed(domain)

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket rate limiter
        
        Args:
            capacity (int): Maximum number of tokens
            refill_rate (float): Tokens added per second
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self._lock = asyncio.Lock()
    
    async def consume(self, tokens: int = 1) -> bool:
        """
        Consume tokens from the bucket
        
        Args:
            tokens (int): Number of tokens to consume
            
        Returns:
            bool: True if tokens were consumed, False if rate limited
        """
        async with self._lock:
            current_time = time.time()
            
            # Refill tokens based on time passed
            time_passed = current_time - self.last_refill
            new_tokens = time_passed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = current_time
            
            # Try to consume tokens
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False

# Global token bucket instance
token_bucket_limiter = TokenBucketRateLimiter(10, 1.0)  # 10 tokens, refill 1 per second

async def token_limit(tokens: int = 1):
    """Token bucket rate limiting"""
    return await token_bucket_limiter.consume(tokens)