"use client"

import { Card } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { HelpCircle } from "lucide-react"
import type { ScanResult } from "@/lib/types"

interface RiskScorePanelProps {
  data: ScanResult
}

function RiskGauge({ score }: { score: number }) {
  const circumference = 2 * Math.PI * 45
  const progress = (score / 100) * circumference
  const remaining = circumference - progress

  const getColor = (score: number) => {
    if (score >= 75) return "var(--critical)"
    if (score >= 50) return "var(--warning)"
    if (score >= 25) return "var(--info)"
    return "var(--safe)"
  }

  const getSeverityLabel = (score: number) => {
    if (score >= 75) return "Critical"
    if (score >= 50) return "High"
    if (score >= 25) return "Medium"
    if (score >= 10) return "Low"
    return "Minimal"
  }

  return (
    <div className="relative w-40 h-40 mx-auto">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="45" fill="none" stroke="var(--border)" strokeWidth="8" />
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke={getColor(score)}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={`${progress} ${remaining}`}
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-bold text-foreground">{score}</span>
        <span className="text-sm text-muted-foreground" style={{ color: getColor(score) }}>
          {getSeverityLabel(score)}
        </span>
      </div>
    </div>
  )
}

function SubMetricBar({
  label,
  value,
  maxValue = 100,
  tooltip,
}: { label: string; value: number; maxValue?: number; tooltip: string }) {
  const percentage = (value / maxValue) * 100

  const getColor = (val: number) => {
    if (val >= 75) return "bg-critical"
    if (val >= 50) return "bg-warning"
    if (val >= 25) return "bg-info"
    return "bg-safe"
  }

  return (
    <TooltipProvider>
      <div className="space-y-1">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-1">
            <span className="text-muted-foreground">{label}</span>
            <Tooltip>
              <TooltipTrigger asChild>
                <button className="text-muted-foreground/60 hover:text-muted-foreground transition-colors">
                  <HelpCircle className="w-3 h-3" />
                </button>
              </TooltipTrigger>
              <TooltipContent side="top" className="max-w-xs bg-popover border-border text-popover-foreground">
                <p className="text-sm">{tooltip}</p>
              </TooltipContent>
            </Tooltip>
          </div>
          <span className="text-foreground font-medium">{value}</span>
        </div>
        <div className="h-2 bg-secondary rounded-full overflow-hidden">
          <div
            className={`h-full ${getColor(value)} transition-all duration-500 ease-out rounded-full`}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    </TooltipProvider>
  )
}

export function RiskScorePanel({ data }: RiskScorePanelProps) {
  if (!data) {
    return null;
  }
  
  return (
    <Card className="p-6 bg-card border-border h-full">
      <h3 className="text-lg font-semibold text-foreground mb-4">Risk Score</h3>

      <RiskGauge score={data.risk_score.total_score} />

      <div className="mt-6 space-y-4">
        <SubMetricBar
          label="Data Sensitivity"
          value={data.risk_score.breakdown.data_sensitivity}
          tooltip="Measures the sensitivity of exposed data - API keys, passwords, and tokens score higher than public profile info."
        />
        <SubMetricBar
          label="Cross-Platform Correlation"
          value={data.risk_score.breakdown.cross_platform_correlation}
          tooltip="Higher when the same identity is linked across multiple platforms, increasing social engineering risk."
        />
        <SubMetricBar
          label="Recency"
          value={data.risk_score.breakdown.data_recency}
          tooltip="Recent exposures are more exploitable. Score increases if sensitive data was exposed within the last 90 days."
        />
        <SubMetricBar
          label="Exploitability"
          value={data.risk_score.breakdown.exploitability}
          tooltip="How easily the findings could be exploited - active API keys and clear-text passwords score highest."
        />
      </div>

      <div className="mt-6 p-3 bg-secondary/50 rounded-lg border border-border">
        <p className="text-sm text-foreground">
          <span className="font-medium">Insight: </span>
          <span className="text-muted-foreground">Risk assessment calculated at {data.risk_score.calculated_at}</span>
        </p>
      </div>
    </Card>
  )
}
