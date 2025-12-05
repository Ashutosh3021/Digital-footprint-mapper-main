"use client"

import type React from "react"

import { Card } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { GitBranch, Link2, AlertTriangle, ShieldAlert, HelpCircle } from "lucide-react"
import type { ScanResult } from "@/lib/types"

interface ExposureSummaryProps {
  data: ScanResult
}

interface MetricCardProps {
  icon: React.ReactNode
  label: string
  value: string | number
  description: string
  tooltip: string
  severity?: "critical" | "warning" | "safe" | "info"
}

function MetricCard({ icon, label, value, description, tooltip, severity = "info" }: MetricCardProps) {
  const severityColors = {
    critical: "text-critical border-critical/30 bg-critical/10",
    warning: "text-warning border-warning/30 bg-warning/10",
    safe: "text-safe border-safe/30 bg-safe/10",
    info: "text-info border-info/30 bg-info/10",
  }

  const iconColors = {
    critical: "text-critical",
    warning: "text-warning",
    safe: "text-safe",
    info: "text-info",
  }

  return (
    <TooltipProvider>
      <Card className={`p-4 bg-card border-border hover:border-muted-foreground/30 transition-colors`}>
        <div className="flex items-start justify-between mb-3">
          <div className={`p-2 rounded-lg ${severityColors[severity]}`}>
            <span className={iconColors[severity]}>{icon}</span>
          </div>
          <Tooltip>
            <TooltipTrigger asChild>
              <button className="text-muted-foreground hover:text-foreground transition-colors">
                <HelpCircle className="w-4 h-4" />
              </button>
            </TooltipTrigger>
            <TooltipContent side="top" className="max-w-xs bg-popover border-border text-popover-foreground">
              <p className="text-sm">{tooltip}</p>
            </TooltipContent>
          </Tooltip>
        </div>
        <div className="space-y-1">
          <p className="text-2xl font-bold text-foreground">{value}</p>
          <p className="text-sm font-medium text-foreground">{label}</p>
          <p className="text-xs text-muted-foreground">{description}</p>
        </div>
      </Card>
    </TooltipProvider>
  )
}

export function ExposureSummary({ data }: ExposureSummaryProps) {
  // Add defensive checks for undefined properties
  if (!data) {
    return null;
  }
  
  const criticalFindings = (data.detailed_findings || []).filter((f) => f.severity === "critical").length
  const hasBreaches = false // Breaches are checked separately via API
  const mandatoryCount = (data.platforms || []).filter((p) => p.source === "mandatory").length
  const optionalCount = (data.platforms || []).filter((p) => p.source === "optional").length
  const discoveredCount = (data.platforms || []).filter((p) => p.source === "discovered").length
  
  // Get repository count from scan result
  const repoCount = data.repo_count || 0;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-foreground">Exposure Summary</h2>
        <span className="text-xs text-muted-foreground">
          Scanned {new Date(data.created_at).toLocaleDateString()} at {new Date(data.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={<GitBranch className="w-5 h-5" />}
          label="Public Repositories"
          value={repoCount}
          description={`${repoCount} public repositories`}
          tooltip="Total number of public repositories found on GitHub. Repositories marked may contain exposed credentials or sensitive data."
          severity="info"
        />
        <MetricCard
          icon={<Link2 className="w-5 h-5" />}
          label="Linked Platforms"
          value={data.platforms.length}
          description={`${mandatoryCount} required, ${optionalCount} optional, ${discoveredCount} discovered`}
          tooltip="Platforms where the user's identity was detected. Required = provided by user, Optional = user-provided extras, Discovered = found during scan."
          severity="info"
        />
        <MetricCard
          icon={<AlertTriangle className="w-5 h-5" />}
          label="Sensitive Findings"
          value={data.detailed_findings.length}
          description={
            criticalFindings > 0
              ? `${criticalFindings} critical findings require attention`
              : "No critical findings detected"
          }
          tooltip="Potential security issues found including exposed API keys, passwords, tokens, and other sensitive information in public code."
          severity={criticalFindings > 0 ? "critical" : data.detailed_findings.length > 0 ? "warning" : "safe"}
        />
        <MetricCard
          icon={<ShieldAlert className="w-5 h-5" />}
          label="Known Breaches"
          value={hasBreaches ? "Yes" : "None"}
          description={
            hasBreaches
              ? "Email found in breach database(s)"
              : "No breaches detected for linked emails"
          }
          tooltip="Checks if any associated email addresses appear in known data breach databases like HaveIBeenPwned."
          severity={hasBreaches ? "critical" : "safe"}
        />
      </div>
    </div>
  )
}
