# username_predictor.py
"""Machine learning-based username prediction across platforms"""

import re
from itertools import product
from datetime import datetime

class UsernamePrediction:
    def __init__(self, known_usernames, osint_data):
        self.known_usernames = known_usernames
        self.osint_data = osint_data
        self.predictions = []
        
        # Platform info for pattern matching
        self.platform_rules = {
            'instagram': {
                'max_length': 30,
                'allows_underscore': True,
                'allows_dot': True,
                'allows_number': True,
                'confidence_boost': 0.15
            },
            'tiktok': {
                'max_length': 24,
                'allows_underscore': True,
                'allows_dot': False,
                'allows_number': True,
                'confidence_boost': 0.10
            },
            'twitch': {
                'max_length': 25,
                'allows_underscore': False,
                'allows_dot': False,
                'allows_number': True,
                'confidence_boost': 0.12
            },
            'discord': {
                'max_length': 32,
                'allows_underscore': True,
                'allows_dot': True,
                'allows_number': True,
                'confidence_boost': 0.08
            },
            'snapchat': {
                'max_length': 15,
                'allows_underscore': False,
                'allows_dot': False,
                'allows_number': True,
                'confidence_boost': 0.10
            },
            'pinterest': {
                'max_length': 25,
                'allows_underscore': True,
                'allows_dot': False,
                'allows_number': True,
                'confidence_boost': 0.09
            }
        }
    
    def generate_predictions(self):
        """Generate all possible username variations"""
        
        for username in self.known_usernames:
            # ===== PATTERN 1: Underscore/dot manipulation =====
            if '_' in username:
                variants = [
                    username.replace('_', ''),           # Remove underscore
                    username.replace('_', '.'),          # Replace with dot
                    username.replace('_', ''),           # No separator
                ]
                for variant in variants:
                    self._add_prediction(variant, 'instagram', 0.75, 
                                       'Instagram prefers no underscores')
            
            if '.' in username:
                variants = [
                    username.replace('.', ''),           # Remove dot
                    username.replace('.', '_'),          # Replace with underscore
                ]
                for variant in variants:
                    self._add_prediction(variant, 'tiktok', 0.70,
                                       'TikTok doesn\'t allow dots')
            
            # ===== PATTERN 2: Number suffixes =====
            current_year = datetime.now().year
            number_suffixes = [
                123, 2024, 2025, 2023, 2022,  # Years
                1, 1, 42,                     # Common numbers
                current_year, current_year - 1  # Recent years
            ]
            
            for num in number_suffixes:
                variant = f"{username}{num}"
                confidence = 0.65 - (num > 1000) * 0.05  # Slight boost for recent years
                self._add_prediction(variant, 'any', confidence,
                                   f'Common pattern: username + {num}')
            
            # ===== PATTERN 3: Case variations =====
            self._add_prediction(username.lower(), 'any', 0.60, 'Lowercase variant')
            self._add_prediction(username.upper(), 'any', 0.50, 'Uppercase variant')
            
            # ===== PATTERN 4: Letter substitution (l33t speak) =====
            leet_subs = {
                'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'
            }
            for old_char, new_char in leet_subs.items():
                if old_char in username.lower():
                    variant = username.replace(old_char, new_char).replace(old_char.upper(), new_char)
                    self._add_prediction(variant, 'gaming', 0.40,
                                       'L33t speak variant (common in gaming)')
            
            # ===== PATTERN 5: Common prefixes/suffixes =====
            prefixes = ['', 'real_', 'the_', 'official_', '_']
            suffixes = ['_', '_official', '_tv', '___', '123']
            
            for prefix in prefixes:
                variant = prefix + username
                confidence = 0.55 - len(prefix) * 0.05
                self._add_prediction(variant, 'any', confidence,
                                   f'Prefix variant: {prefix}')
            
            for suffix in suffixes:
                variant = username + suffix
                confidence = 0.55 - len(suffix) * 0.05
                self._add_prediction(variant, 'any', confidence,
                                   f'Suffix variant: {suffix}')
            
            # ===== PATTERN 6: Historical usernames =====
            # If we found old commits, might have old usernames
            if self.osint_data.get('old_emails'):
                for old_email in self.osint_data['old_emails']:
                    old_username = old_email.split('@')[0]
                    self._add_prediction(old_username, 'any', 0.45,
                                       'Extracted from historical email')
        
        # Remove duplicates and sort by confidence
        unique_predictions = {p['username']: p for p in self.predictions}
        self.predictions = list(unique_predictions.values())
        self.predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return self.predictions[:20]  # Top 20 predictions
    
    def _add_prediction(self, username, platform, confidence, reason):
        """Add a prediction with confidence score"""
        
        # Skip if too short/long
        if len(username) < 3 or len(username) > 32:
            return
        
        # Skip if already known
        if username in self.known_usernames:
            return
        
        # Apply platform-specific confidence boost
        if platform in self.platform_rules:
            platform_rules = self.platform_rules[platform]
            
            if len(username) > platform_rules['max_length']:
                return  # Too long for platform
            
            if '_' in username and not platform_rules['allows_underscore']:
                confidence *= 0.7  # Reduce confidence
            
            if '.' in username and not platform_rules['allows_dot']:
                confidence *= 0.7
            
            confidence += platform_rules.get('confidence_boost', 0)
        
        self.predictions.append({
            'username': username,
            'platform': platform if platform != 'any' else 'Unknown',
            'confidence': round(min(confidence, 0.99), 2),  # Cap at 0.99
            'reason': reason,
            'likely_platforms': self._get_likely_platforms(username)
        })
    
    def _get_likely_platforms(self, username):
        """Determine which platforms this username likely works on"""
        platforms = []
        
        for platform, rules in self.platform_rules.items():
            if len(username) <= rules['max_length']:
                # Check character constraints
                has_underscore = '_' in username
                has_dot = '.' in username
                
                if has_underscore and not rules['allows_underscore']:
                    continue
                if has_dot and not rules['allows_dot']:
                    continue
                
                platforms.append(platform)
        
        return platforms if platforms else ['Any']

    def get_risk_assessment(self):
        """How risky are these predictions?"""
        return {
            'total_predictions': len(self.predictions),
            'high_confidence': len([p for p in self.predictions if p['confidence'] >= 0.7]),
            'medium_confidence': len([p for p in self.predictions if 0.5 <= p['confidence'] < 0.7]),
            'low_confidence': len([p for p in self.predictions if p['confidence'] < 0.5]),
            'risk_summary': f"Found {len([p for p in self.predictions if p['confidence'] >= 0.7])} " +
                           f"high-confidence username predictions across multiple platforms"
        }