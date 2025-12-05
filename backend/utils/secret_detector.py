"""Secret Detection Utility

This module provides functionality to detect potential secrets in text data.
"""

import re
from typing import List, Dict, Tuple
import asyncio
import time

# Simple rate limiting function for standalone use
async def rate_limit(domain: str = "default"):
    """Simple rate limiting"""
    await asyncio.sleep(0.1)  # Simple delay

class SecretDetector:
    def __init__(self):
        """Initialize secret detector with common patterns"""
        # Common secret patterns
        self.patterns = {
            "aws_access_key": r"(?i)(aws|amazon)[_\s-]?access[_\s-]?key[_\s-]?id?[^\w\r\n]{0,10}[A-Z0-9]{20}",
            "aws_secret_key": r"(?i)(aws|amazon)[_\s-]?secret[_\s-]?access[_\s-]?key[^\w\r\n]{0,10}[A-Za-z0-9/+=]{40}",
            "github_token": r"(?i)github[_\s-]?token[^\w\r\n]{0,10}[a-zA-Z0-9_]{35,40}",
            "api_key": r"(?i)api[_\s-]?key[^\w\r\n]{0,10}[a-zA-Z0-9_-]{32,64}",
            "password": r"(?i)(password|pwd)[_\s-]?(?:\w*[=:]){0,1}[^\w\r\n]{0,10}[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>?]{8,}",
            "bearer_token": r"(?i)bearer[^\w\r\n]{0,10}[a-zA-Z0-9\-_\.+/=]{20,}",
            "authorization_header": r"(?i)authorization[^\w\r\n]{0,10}(basic|bearer|token)[^\w\r\n]{0,10}[a-zA-Z0-9\-_\.+/=]{10,}",
            "private_key": r"-----BEGIN[^\r\n]*PRIVATE KEY-----",
            "slack_token": r"(?i)xox[baprs]-[a-zA-Z0-9]{10,48}",
            "firebase": r"(?i)firebase[^\w\r\n]{0,10}[a-zA-Z0-9\-_]{30,}",
            "heroku_api_key": r"(?i)heroku[_\s-]?api[_\s-]?key[^\w\r\n]{0,10}[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}",
            "twilio_auth_token": r"(?i)twilio[_\s-]?auth[_\s-]?token[^\w\r\n]{0,10}[a-z0-9]{32}",
            "sendgrid_api_key": r"(?i)sendgrid[_\s-]?api[_\s-]?key[^\w\r\n]{0,10}[A-Za-z0-9\-_]{30,}",
            "mailgun_api_key": r"(?i)mailgun[_\s-]?api[_\s-]?key[^\w\r\n]{0,10}[a-z0-9]{32}",
            "paypal_client_id": r"(?i)paypal[_\s-]?client[_\s-]?id[^\w\r\n]{0,10}[a-zA-Z0-9]{16,}"
        }

    def detect_secrets(self, text: str) -> List[Dict[str, str]]:
        """
        Detect potential secrets in text
        
        Args:
            text (str): Text to scan for secrets
            
        Returns:
            List of detected secrets with type and value
        """
        secrets = []
        
        for secret_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                secrets.append({
                    "type": secret_type,
                    "value": match.group(),
                    "position": match.span()
                })
        
        return secrets
    
    def detect_secrets_with_context(self, text: str, context_lines: int = 3) -> List[Dict[str, str]]:
        """
        Detect potential secrets with surrounding context
        
        Args:
            text (str): Text to scan for secrets
            context_lines (int): Number of lines of context to include
            
        Returns:
            List of detected secrets with context
        """
        secrets = []
        lines = text.split('\n')
        
        for secret_type, pattern in self.patterns.items():
            for i, line in enumerate(lines):
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    # Get context lines
                    start_line = max(0, i - context_lines)
                    end_line = min(len(lines), i + context_lines + 1)
                    context = '\n'.join(lines[start_line:end_line])
                    
                    secrets.append({
                        "type": secret_type,
                        "value": match.group(),
                        "line": i + 1,
                        "context": context
                    })
        
        return secrets
    
    async def detect_secrets_in_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        Detect potential secrets in a file
        
        Args:
            file_path (str): Path to file to scan
            
        Returns:
            List of detected secrets
        """
        # Rate limit to be ethical
        await rate_limit("file_scanning")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                return self.detect_secrets(content)
        except Exception as e:
            return [{"error": f"Error reading file {file_path}: {str(e)}"}]

# Global secret detector instance
secret_detector = SecretDetector()

# Convenience functions
def detect_secrets(text: str) -> List[Dict[str, str]]:
    """Detect secrets in text"""
    return secret_detector.detect_secrets(text)

def detect_secrets_with_context(text: str, context_lines: int = 3) -> List[Dict[str, str]]:
    """Detect secrets with context"""
    return secret_detector.detect_secrets_with_context(text, context_lines)

async def detect_secrets_in_file(file_path: str) -> List[Dict[str, str]]:
    """Detect secrets in a file"""
    return await secret_detector.detect_secrets_in_file(file_path)