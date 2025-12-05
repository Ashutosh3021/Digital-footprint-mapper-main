# threat_intelligence.py
"""Sophisticated threat intelligence analysis"""

class ThreatIntelligence:
    def __init__(self, osint_data, risk_score, graph):
        self.osint_data = osint_data
        self.risk_score = risk_score
        self.graph = graph
    
    def calculate_identity_reconstruction_risk(self):
        """
        What % of identity can be reconstructed from public data?
        Formula: (data_points_found / total_possible_datapoints) * 100
        """
        max_possible = 100  # Email, phone, address, work, education, social media x5, etc.
        
        data_points = 0
        data_points += 10 if self.osint_data.get('emails') else 0
        data_points += 10 if self.osint_data.get('phone') else 0
        data_points += 10 if self.osint_data.get('locations') else 0
        data_points += 10 if self.osint_data.get('organizations') else 0
        data_points += len(self.osint_data.get('platforms', {})) * 8
        data_points += 10 if self.osint_data.get('repositories') else 0
        data_points += 10 if self.osint_data.get('websites') else 0
        data_points += 5 if self.osint_data.get('profile_bio') else 0
        
        percentage = min((data_points / max_possible) * 100, 100)
        return round(percentage, 1)
    
    def calculate_phishing_vulnerability(self):
        """
        Risk of successful phishing attack
        Formula: email_exposed * workplace_known * location_known * account_count
        """
        email_risk = 30 if self.osint_data.get('emails') else 0
        workplace_risk = 20 if self.osint_data.get('organizations') else 0
        location_risk = 15 if self.osint_data.get('locations') else 0
        social_risk = min(len(self.osint_data.get('platforms', {})) * 5, 20)
        
        total = min(email_risk + workplace_risk + location_risk + social_risk, 100)
        return round(total, 1)
    
    def calculate_account_takeover_risk(self):
        """
        Risk of account compromise
        Formula: exposed_secrets * account_count * breach_count
        """
        secrets_risk = min(len(self.osint_data.get('exposed_secrets', [])) * 15, 40)
        accounts_risk = min(len(self.osint_data.get('platforms', {})) * 8, 30)
        breach_risk = min(sum(1 for v in self.osint_data.get('breaches', {}).values() 
                             for _ in v) * 5, 30)
        
        total = min(secrets_risk + accounts_risk + breach_risk, 100)
        return round(total, 1)
    
    def calculate_data_broker_aggregation(self):
        """
        How many commercial data brokers have your info?
        Typical: 100+ data brokers worldwide
        """
        base_risk = 50  # Everyone is on some data brokers
        
        if self.osint_data.get('emails'):
            base_risk += 20
        if self.osint_data.get('phone'):
            base_risk += 15
        if self.osint_data.get('locations'):
            base_risk += 10
        if self.osint_data.get('breaches'):
            base_risk += 15
        
        return min(round(base_risk, 1), 100)
    
    def get_threat_matrix(self):
        """Return complete threat intelligence matrix"""
        return {
            'identity_reconstruction_risk': self.calculate_identity_reconstruction_risk(),
            'phishing_vulnerability': self.calculate_phishing_vulnerability(),
            'account_takeover_risk': self.calculate_account_takeover_risk(),
            'data_broker_aggregation': self.calculate_data_broker_aggregation(),
            'overall_risk_score': self.risk_score,
            'estimated_data_brokers': round(self.calculate_data_broker_aggregation() * 1.5),  # Estimate count
            'recommendations_count': len([r for r in self.osint_data.get('recommendations', []) 
                                         if r['priority'] in ['CRITICAL', 'HIGH']])
        }