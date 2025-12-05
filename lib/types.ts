export interface Recommendation {
  priority: string
  icon: string
  title: string
  description: string
  action?: string
  alternatives?: string[]
  time_to_fix: string
  severity: string
  tools?: string[]
  platforms?: string[]
  url?: string
  entities?: string[]
  priority_score?: number
}

export interface TimelineEvent {
  date: string
  timestamp: string
  type: string
  severity: string
  icon: string
  title: string
  description: string
  source: string
  color: string
  count?: number
  hovered?: boolean
}

export interface ThreatIntelligenceMatrix {
  identity_reconstruction_risk: number
  phishing_vulnerability: number
  account_takeover_risk: number
  data_broker_aggregation: number
  overall_risk_score: number
  estimated_data_brokers: number
  recommendations_count: number
}

export interface PredictionRiskAssessment {
  total_predictions: number
  high_confidence: number
  medium_confidence: number
  low_confidence: number
  risk_summary: string
}

export interface ScanResult {
  scan_id: string
  email: string
  platforms: PlatformLink[]
  profile_summary: {
    name: string
    bio: string
    locations: string[]
    organizations: string[]
  }
  risk_score: {
    total_score: number
    severity: string
    breakdown: {
      data_sensitivity: number
      cross_platform_correlation: number
      data_recency: number
      exploitability: number
    }
    calculated_at: string
  }
  graph_data: {
    nodes: Array<{
      id: string
      label: string
      type: string
      color: string
      size: number
      attributes: Record<string, any>
    }>
    edges: Array<{
      from: string
      to: string
      title: string
      width: number
      color: string
      attributes: Record<string, any>
    }>
  }
  detailed_findings: DetailedFinding[]
  trackers: Tracker[]
  username_predictions: UsernamePrediction[]
  repo_count: number
  created_at: string
  // New fields for advanced features
  recommendations?: Recommendation[]
  timeline?: TimelineEvent[]
  timeline_stats?: Record<string, any>
  threat_intelligence?: ThreatIntelligenceMatrix
  predictions?: Array<Record<string, any>>
  predictions_risk?: PredictionRiskAssessment
}

export interface DetailedFinding {
  platform: string
  type: string
  description: string
  severity: "critical" | "high" | "medium" | "low"
  evidence: string
  recommendation: string
}

export interface PlatformLink {
  name: string
  handle: string
  url: string
  source: "mandatory" | "optional" | "discovered"
  verified: boolean
}

export interface UsernamePrediction {
  platform: string
  predicted_username: string
  confidence: number
}

export interface Tracker {
  name: string
  tracking_methods: string[]
  confidence: number
}

export interface ScanInput {
  // Mandatory fields
  email: string
  github: string
  linkedin: string
  // Optional fields
  twitter?: string
  reddit?: string
  facebook?: string
  instagram?: string
  youtube?: string
}