"""Email Collector Module

This module handles email validation and basic analysis including:
- Email format validation
- Domain extraction
- Disposable email detection
- MX record checking
"""

import re
import dns.resolver
import socket
from typing import Dict, Any
from datetime import datetime
from utils.rate_limiter import rate_limit

class EmailCollector:
    def __init__(self):
        """Initialize email collector"""
        # Common disposable email domains
        self.disposable_domains = {
            '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
            'yopmail.com', 'tempmail.org', 'throwawaymail.com'
        }
        
    async def collect_email_data(self, email: str) -> Dict[str, Any]:
        """
        Collect and analyze email data
        
        Args:
            email (str): Email address to analyze
            
        Returns:
            Dict containing email analysis data
        """
        await rate_limit("dns")
        
        # Validate email format
        is_valid = self._validate_email_format(email)
        
        if not is_valid:
            return {
                "email": email,
                "valid": False,
                "error": "Invalid email format"
            }
            
        # Extract domain
        domain = email.split('@')[1] if '@' in email else ""
        
        # Check if disposable email
        is_disposable = domain.lower() in self.disposable_domains
        
        # Check MX records
        mx_records = await self._check_mx_records(domain)
        
        # Determine if likely corporate email
        is_corporate = self._is_corporate_email(domain)
        
        return {
            "email": email,
            "valid": True,
            "domain": domain,
            "disposable": is_disposable,
            "mx_records": mx_records,
            "corporate": is_corporate,
            "analyzed_at": datetime.now().isoformat()
        }
        
    def _validate_email_format(self, email: str) -> bool:
        """
        Validate email format using regex
        
        Args:
            email (str): Email to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    async def _check_mx_records(self, domain: str) -> Dict[str, Any]:
        """
        Check MX records for a domain
        
        Args:
            domain (str): Domain to check
            
        Returns:
            Dict containing MX record information
        """
        try:
            await rate_limit("dns")
            mx_records = dns.resolver.resolve(domain, 'MX')
            
            records = []
            for record in mx_records:
                records.append({
                    "priority": record.preference,
                    "server": str(record.exchange)
                })
                
            return {
                "exists": True,
                "records": records
            }
        except Exception as e:
            return {
                "exists": False,
                "error": str(e)
            }
            
    def _is_corporate_email(self, domain: str) -> bool:
        """
        Determine if email is likely from a corporate domain
        
        Args:
            domain (str): Email domain
            
        Returns:
            bool: True if likely corporate, False otherwise
        """
        # Common consumer email providers
        consumer_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'protonmail.com'
        }
        
        return domain.lower() not in consumer_domains

    async def collect_all_data(self, email: str) -> Dict[str, Any]:
        """
        Collect all available data for an email
        
        Args:
            email (str): Email address to analyze
            
        Returns:
            Dict containing all collected email data
        """
        email_data = await self.collect_email_data(email)
        
        return {
            "platform": "Email",
            "data": email_data,
            "collected_at": datetime.now().isoformat()
        }