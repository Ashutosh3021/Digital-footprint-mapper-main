# exposure_timeline.py
"""Generate exposure timeline for visual display"""

from datetime import datetime
import pytz

class ExposureTimeline:
    def __init__(self, osint_data):
        self.osint_data = osint_data
        self.events = []
    
    def generate_timeline(self):
        """Build chronological exposure event list"""
        
        # ===== GITHUB COMMITS =====
        commits = self.osint_data.get('commits', [])
        for commit in commits:
            self.events.append({
                'date': commit.get('date', 'Unknown'),
                'timestamp': self._parse_date(commit.get('date')),
                'type': 'github_commit',
                'severity': 'high',
                'icon': '📝',
                'title': 'Suspicious GitHub Commit',
                'description': f"Commit message: {commit.get('message', '')[:60]}...",
                'source': 'GitHub',
                'color': '#ff6b35'
            })
        
        # ===== DATA BREACHES =====
        breaches = self.osint_data.get('breaches', {})
        for email, breach_list in breaches.items():
            for breach in breach_list:
                self.events.append({
                    'date': breach.get('date', 'Unknown'),
                    'timestamp': self._parse_date(breach.get('date')),
                    'type': 'data_breach',
                    'severity': 'critical',
                    'icon': '🚨',
                    'title': f"Data Breach: {breach.get('name', 'Unknown')}",
                    'description': f"Email {email} exposed. {breach.get('count', '?'):,} records affected.",
                    'source': 'Data Breach DB',
                    'color': '#ff0054',
                    'count': breach.get('count', 0)
                })
        
        # ===== REPOSITORY CREATION =====
        repos = self.osint_data.get('repositories', [])
        for repo in repos:
            created_date = repo.get('created_at', 'Unknown')
            if created_date != 'Unknown':
                self.events.append({
                    'date': created_date,
                    'timestamp': self._parse_date(created_date),
                    'type': 'repo_created',
                    'severity': 'low',
                    'icon': '📦',
                    'title': 'GitHub Repository Created',
                    'description': f"Repository '{repo.get('name')}' created",
                    'source': 'GitHub',
                    'color': '#ffd166'
                })
        
        # ===== PROFILE UPDATES =====
        if self.osint_data.get('bio_updated'):
            self.events.append({
                'date': self.osint_data['bio_updated'],
                'timestamp': self._parse_date(self.osint_data['bio_updated']),
                'type': 'profile_update',
                'severity': 'low',
                'icon': '👤',
                'title': 'Profile Information Updated',
                'description': 'Bio or profile info changed - may expose new info',
                'source': 'Social Media',
                'color': '#4ecdc4'
            })
        
        # ===== ACCOUNT CREATION =====
        accounts = self.osint_data.get('accounts', {})
        for platform, username in accounts.items():
            if username:
                self.events.append({
                    'date': f'Active on {platform}',
                    'timestamp': datetime.now(),
                    'type': 'account_active',
                    'severity': 'low',
                    'icon': '🌐',
                    'title': f'{platform.capitalize()} Account Active',
                    'description': f"Username: {username}",
                    'source': platform.capitalize(),
                    'color': '#9d4edd'
                })
        
        # Sort by date (newest first)
        self.events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return self.events
    
    def _parse_date(self, date_str):
        """Parse various date formats"""
        if isinstance(date_str, datetime):
            return date_str
        
        formats = [
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y',
            '%m/%d/%Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return datetime.now()  # Fallback
    
    def get_timeline_stats(self):
        """Return summary statistics"""
        return {
            'total_events': len(self.events),
            'critical_events': len([e for e in self.events if e['severity'] == 'critical']),
            'high_events': len([e for e in self.events if e['severity'] == 'high']),
            'earliest_event': self.events[-1] if self.events else None,
            'latest_event': self.events[0] if self.events else None
        }