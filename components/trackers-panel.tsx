"use client"

import { Card } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Eye, HelpCircle, ExternalLink } from "lucide-react"
import type { Tracker } from "@/lib/types"

interface TrackersPanelProps {
  trackers: Tracker[]
}

function ConfidenceBar({ value }: { value: number }) {
  const getColor = (val: number) => {
    if (val >= 80) return "bg-critical"
    if (val >= 50) return "bg-warning"
    return "bg-info"
  }

  return (
    <div className="w-20 h-2 bg-secondary rounded-full overflow-hidden">
      <div className={`h-full ${getColor(value)} transition-all`} style={{ width: `${value}%` }} />
    </div>
  )
}

export function TrackersPanel({ trackers }: TrackersPanelProps) {
  if (!trackers) {
    return null;
  }
  
  return (
    <Card className="bg-card border-border">
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <Eye className="w-5 h-5 text-warning" />
          <h3 className="text-lg font-semibold text-foreground">Trackers & Monitoring Entities</h3>
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <button className="text-muted-foreground hover:text-foreground">
                  <HelpCircle className="w-4 h-4" />
                </button>
              </TooltipTrigger>
              <TooltipContent side="right" className="max-w-xs bg-popover border-border text-popover-foreground">
                <p className="text-sm">
                  Entities likely tracking or aggregating your data based on your online presence, linked accounts, and
                  detected analytics/ad networks.
                </p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
        <p className="text-sm text-muted-foreground mt-1">Who is watching your online activity</p>
      </div>

      <div className="divide-y divide-border">
        {trackers.map((tracker, i) => (
          <div key={i} className="p-4 hover:bg-secondary/30 transition-colors">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-foreground">{tracker.name}</span>
                </div>
                <p className="text-sm text-muted-foreground mb-2">{tracker.tracking_methods.join(", ")}</p>
                <p className="text-xs text-muted-foreground/80">Confidence level: {tracker.confidence}%</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className="text-xs text-muted-foreground">Confidence</span>
                <div className="flex items-center gap-2">
                  <ConfidenceBar value={tracker.confidence} />
                  <span className="text-sm text-foreground w-8 text-right">{tracker.confidence}%</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}
