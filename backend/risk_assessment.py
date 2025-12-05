# risk_assessment.py
"""Generate actionable security recommendations based on OSINT findings"""

class SecurityRecommendations:
    def __init__(self, osint_data, risk_score):
        self.osint_data = osint_data
        self.risk_score = risk_score
        self.recommendations = []
    
    def generate_all_recommendations(self):
        """Generate comprehensive list of next steps"""
        
        # CRITICAL: High risk score
        if self.risk_score >= 70:
            self.recommendations.append({
                'priority': 'CRITICAL',
                'icon': '⚠️',
                'title': 'Change All Passwords Immediately',
                'description': 'Your account is highly vulnerable. Change passwords for all linked accounts.',
                'action': 'Change passwords on: GitHub, Email, LinkedIn, Twitter',
                'time_to_fix': '15 minutes',
                'severity': 'critical'
            })
        
        # API Keys exposed
        exposed_secrets = self.osint_data.get('exposed_secrets', [])
        if exposed_secrets:
            secret_count = len(exposed_secrets)
            self.recommendations.append({
                'priority': 'HIGH',
                'icon': '🔑',
                'title': f'Rotate {secret_count} Exposed API Keys',
                'description': f'{secret_count} API keys found in GitHub commits. These need immediate rotation.',
                'action': f'Use: git filter-branch --tree-filter "rm -f {exposed_secrets[0].get("file", "")}" HEAD',
                'alternatives': [
                    'Use BFG Repo-Cleaner: bfg --delete-files {secrets}',
                    'Use git reset --hard HEAD~N to rewrite history'
                ],
                'time_to_fix': '30 minutes',
                'severity': 'high',
                'tools': ['git-filter-branch', 'BFG-Repo-Cleaner']
            })
        
        # 2FA not enabled
        linked_platforms = len(self.osint_data.get('platforms', {}))
        if linked_platforms > 0:
            self.recommendations.append({
                'priority': 'HIGH',
                'icon': '🔒',
                'title': f'Enable 2FA on {linked_platforms} Accounts',
                'description': 'Two-factor authentication significantly reduces account takeover risk.',
                'action': 'Enable 2FA on each platform account',
                'platforms': list(self.osint_data.get('platforms', {}).keys()),
                'time_to_fix': '20 minutes',
                'severity': 'high'
            })
        
        # Email in breaches
        breaches = self.osint_data.get('breaches', {})
        if breaches:
            total_breaches = sum(len(v) for v in breaches.values())
            self.recommendations.append({
                'priority': 'MEDIUM',
                'icon': '📧',
                'title': f'Email Exposed in {total_breaches} Data Breaches',
                'description': 'Your email appears in known data breaches. Monitor for unauthorized access.',
                'action': 'Check HaveIBeenPwned.com for details',
                'url': f'https://haveibeenpwned.com/search?q={list(breaches.keys())[0] if breaches else ""}',
                'time_to_fix': '5 minutes',
                'severity': 'medium'
            })
        
        # Privacy review
        trackers = self.osint_data.get('trackers', [])
        if trackers:
            self.recommendations.append({
                'priority': 'MEDIUM',
                'icon': '👁️',
                'title': f'Review Privacy Settings - {len(trackers)} Trackers Detected',
                'description': f'{len(trackers)} entities are likely tracking your online activity.',
                'action': 'Review privacy settings on each platform',
                'entities': [t.get('name', 'Unknown') for t in trackers],
                'time_to_fix': '15 minutes',
                'severity': 'medium'
            })
        
        # Location exposure
        if self.osint_data.get('locations'):
            self.recommendations.append({
                'priority': 'LOW',
                'icon': '📍',
                'title': 'Limit Location Information',
                'description': 'Your location data is publicly visible across multiple platforms.',
                'action': 'Update privacy settings to hide location',
                'time_to_fix': '10 minutes',
                'severity': 'low'
            })
        
        return self.recommendations
    
    def get_priority_score(self):
        """Calculate action priority score for sorting"""
        priority_map = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        
        scored = []
        for rec in self.recommendations:
            score = priority_map.get(rec['priority'], 0)
            rec['priority_score'] = score
            scored.append(rec)
        
        return sorted(scored, key=lambda x: x['priority_score'], reverse=True)