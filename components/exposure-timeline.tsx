"use client"

import { TimelineEvent } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface ExposureTimelineProps {
  timeline: TimelineEvent[]
  timelineStats: Record<string, any>
}

export function ExposureTimeline({ timeline, timelineStats }: ExposureTimelineProps) {
  if (!timeline || timeline.length === 0) {
    return null
  }

  // Sort timeline events by timestamp (newest first)
  const sortedTimeline = [...timeline].sort((a, b) => 
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  )

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'bg-destructive'
      case 'high': return 'bg-orange-500'
      case 'medium': return 'bg-yellow-500'
      case 'low': return 'bg-green-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <Card className="border border-border bg-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg">
            <span>📅 Exposure Timeline</span>
          </CardTitle>
          <div className="text-sm text-muted-foreground">
            {timelineStats?.total_events || timeline.length} events •{' '}
            {timelineStats?.critical_events || 0} 🚨 critical
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative pl-8 border-l-2 border-primary/30 ml-4">
          {sortedTimeline.map((event, index) => (
            <div key={index} className="mb-8 relative">
              {/* Timeline dot */}
              <div 
                className={`absolute -left-11 top-1 w-6 h-6 rounded-full border-4 border-background ${getSeverityColor(event.severity)}`}
                style={{ boxShadow: `0 0 0 2px ${event.color}` }}
              ></div>
              
              {/* Event card */}
              <div 
                className="bg-muted/50 border border-border rounded-lg p-4 hover:bg-muted/80 transition-colors cursor-pointer"
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl mt-1">{event.icon}</span>
                  <div className="flex-1">
                    <div className="flex justify-between items-start">
                      <h4 className="font-medium">{event.title}</h4>
                      <Badge 
                        className={`${getSeverityColor(event.severity)} text-white`}
                      >
                        {event.severity}
                      </Badge>
                    </div>
                    
                    <p className="text-muted-foreground text-sm mt-2 mb-3">
                      {event.description}
                    </p>
                    
                    <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
                      <span>📅 {event.date}</span>
                      <span>📍 {event.source}</span>
                      {event.count && <span>👥 {event.count.toLocaleString()} records</span>}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}