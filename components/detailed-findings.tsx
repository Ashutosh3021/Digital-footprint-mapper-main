"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, ExternalLink, GitCommit, Key, User, ShieldAlert } from "lucide-react"
import type { ScanResult, DetailedFinding } from "@/lib/types"

interface DetailedFindingsProps {
  data: ScanResult
}

function SeverityBadge({ severity }: { severity: string }) {
  const colors = {
    critical: "bg-critical/20 text-critical border-critical/30",
    high: "bg-warning/20 text-warning border-warning/30",
    medium: "bg-info/20 text-info border-info/30",
    low: "bg-safe/20 text-safe border-safe/30",
  }

  return (
    <Badge variant="outline" className={colors[severity as keyof typeof colors] || colors.low}>
      {severity}
    </Badge>
  )
}

function FindingsTable({
  findings,
  searchQuery,
  severityFilter,
}: { findings: DetailedFinding[]; searchQuery: string; severityFilter: string }) {
  const filtered = findings.filter((f) => {
    const matchesSearch =
      searchQuery === "" ||
      f.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.evidence.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesSeverity = severityFilter === "all" || f.severity === severityFilter
    return matchesSearch && matchesSeverity
  })

  return (
    <div className="divide-y divide-border">
      {filtered.length === 0 ? (
        <div className="p-8 text-center text-muted-foreground">No findings match your filters</div>
      ) : (
        filtered.map((finding, i) => (
          <div key={i} className="p-4 hover:bg-secondary/30 transition-colors">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <Key className="w-4 h-4 text-warning" />
                  <span className="font-medium text-foreground">{finding.platform}: {finding.type}</span>
                  <SeverityBadge severity={finding.severity} />
                </div>
                <p className="text-sm text-muted-foreground mb-2">{finding.description}</p>
                <p className="text-xs text-muted-foreground mb-2">{finding.evidence}</p>
                <p className="text-xs text-info">{finding.recommendation}</p>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  )
}

export function DetailedFindings({ data }: DetailedFindingsProps) {
  if (!data) {
    return null;
  }
  
  const [searchQuery, setSearchQuery] = useState("")
  const [severityFilter, setSeverityFilter] = useState("all")

  return (
    <Card className="bg-card border-border">
      <Tabs defaultValue="findings" className="w-full">
        <div className="p-4 border-b border-border">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <TabsList className="bg-secondary">
              <TabsTrigger
                value="findings"
                className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
              >
                Detailed Findings
              </TabsTrigger>
              <TabsTrigger
                value="trackers"
                className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
              >
                Trackers
              </TabsTrigger>
              <TabsTrigger
                value="predictions"
                className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
              >
                Username Predictions
              </TabsTrigger>
            </TabsList>

            <div className="flex items-center gap-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Search findings..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 w-64 bg-secondary border-border"
                />
              </div>
              <Select value={severityFilter} onValueChange={setSeverityFilter}>
                <SelectTrigger className="w-36 bg-secondary border-border">
                  <SelectValue placeholder="Severity" />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="all">All Severities</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        <TabsContent value="findings" className="m-0">
          <FindingsTable findings={data.detailed_findings} searchQuery={searchQuery} severityFilter={severityFilter} />
        </TabsContent>

        <TabsContent value="trackers" className="m-0">
          <div className="divide-y divide-border">
            {data.trackers.map((tracker, i) => (
              <div key={i} className="p-4 hover:bg-secondary/30 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="font-medium text-foreground">{tracker.name}</span>
                    <Badge variant="outline" className="bg-info/20 text-info border-info/30">
                      {(tracker.confidence * 100).toFixed(0)}% confidence
                    </Badge>
                  </div>
                  <span className="text-sm text-muted-foreground">
                    {tracker.tracking_methods.join(", ")}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="m-0">
          <div className="divide-y divide-border">
            {data.username_predictions.map((prediction, i) => (
              <div key={i} className="p-4 hover:bg-secondary/30 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="font-medium text-foreground">{prediction.platform}</span>
                    <Badge variant="outline" className="bg-success/20 text-success border-success/30">
                      {(prediction.confidence * 100).toFixed(0)}% confidence
                    </Badge>
                  </div>
                  <span className="font-mono text-sm text-muted-foreground">
                    @{prediction.predicted_username}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  )
}