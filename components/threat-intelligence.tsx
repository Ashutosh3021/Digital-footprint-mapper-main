"use client"

import { ThreatIntelligenceMatrix } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ThreatIntelligenceProps {
  threatIntelligence: ThreatIntelligenceMatrix
}

export function ThreatIntelligence({ threatIntelligence }: ThreatIntelligenceProps) {
  if (!threatIntelligence) {
    return null
  }

  const metrics = [
    {
      title: "🆔 Identity Reconstruction Risk",
      value: `${threatIntelligence.identity_reconstruction_risk}%`,
      description: `An attacker can reconstruct ${threatIntelligence.identity_reconstruction_risk}% of your identity from publicly available data.`,
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
      borderColor: "border-orange-500/30",
      icon: "🆔"
    },
    {
      title: "🎣 Phishing Vulnerability",
      value: `${threatIntelligence.phishing_vulnerability}%`,
      description: "Email + workplace + location = easy phishing target. Consider security awareness training.",
      color: "text-yellow-500",
      bgColor: "bg-yellow-500/10",
      borderColor: "border-yellow-500/30",
      icon: "🎣"
    },
    {
      title: "🔓 Account Takeover Risk",
      value: `${threatIntelligence.account_takeover_risk}%`,
      description: "Exposed secrets + multiple accounts = high takeover likelihood. Rotate credentials NOW.",
      color: "text-purple-500",
      bgColor: "bg-purple-500/10",
      borderColor: "border-purple-500/30",
      icon: "🔓"
    },
    {
      title: "🌐 Data Broker Presence",
      value: `~${threatIntelligence.estimated_data_brokers}`,
      description: `Your data likely appears in ${threatIntelligence.estimated_data_brokers} commercial data broker databases worldwide.`,
      color: "text-teal-500",
      bgColor: "bg-teal-500/10",
      borderColor: "border-teal-500/30",
      icon: "🌐"
    }
  ]

  return (
    <Card className="border border-border bg-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <span>🎯 Threat Intelligence Matrix</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {metrics.map((metric, index) => (
            <div 
              key={index}
              className={`rounded-lg border p-4 ${metric.bgColor} ${metric.borderColor}`}
            >
              <h4 className={`font-medium mb-2 ${metric.color}`}>
                {metric.icon} {metric.title}
              </h4>
              <div className={`text-3xl font-bold my-2 ${metric.color}`}>
                {metric.value}
              </div>
              <p className="text-muted-foreground text-sm">
                {metric.description}
              </p>
            </div>
          ))}
        </div>
        
        <div className="mt-6 p-4 bg-primary/10 rounded-lg border border-primary/30">
          <strong className="text-foreground text-sm">🎯 Key Insight:</strong>
          <p className="text-muted-foreground text-sm mt-1">
            {threatIntelligence.recommendations_count} high-priority actions recommended. 
            Start with enabling 2FA.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}