"use client"

import { Recommendation } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { 
  Accordion, 
  AccordionContent, 
  AccordionItem, 
  AccordionTrigger 
} from "@/components/ui/accordion"

interface RecommendedNextStepsProps {
  recommendations: Recommendation[]
}

export function RecommendedNextSteps({ recommendations }: RecommendedNextStepsProps) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <Card className="border border-border bg-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <span>🛡️ Recommended Next Steps</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-6 text-muted-foreground">
            ✅ No immediate actions needed. Your exposure is minimal.
          </div>
        </CardContent>
      </Card>
    )
  }

  // Sort recommendations by priority score
  const sortedRecommendations = [...recommendations].sort((a, b) => 
    (b.priority_score || 0) - (a.priority_score || 0)
  )

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'bg-destructive text-destructive-foreground'
      case 'high': return 'bg-orange-500 text-white'
      case 'medium': return 'bg-yellow-500 text-black'
      case 'low': return 'bg-green-500 text-white'
      default: return 'bg-gray-500 text-white'
    }
  }

  return (
    <Card className="border border-border bg-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <span>🛡️ Recommended Next Steps</span>
          <Badge variant="secondary" className="ml-auto">
            {sortedRecommendations.length} actions
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {sortedRecommendations.map((rec, index) => (
            <AccordionItem value={`item-${index}`} key={index} className="border-b border-border">
              <AccordionTrigger className="py-3 hover:no-underline">
                <div className="flex items-center gap-3 w-full">
                  <span className="text-xl">{rec.icon}</span>
                  <div className="flex-1 text-left">
                    <div className="font-medium">{rec.title}</div>
                    <div className="text-sm text-muted-foreground mt-1">
                      <span className={`inline-block w-3 h-3 rounded-full mr-2 ${getSeverityColor(rec.severity)}`}></span>
                      Priority: {rec.priority} • ⏱️ {rec.time_to_fix}
                    </div>
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent className="pb-4">
                <p className="text-muted-foreground text-sm mb-3">
                  {rec.description}
                </p>
                
                {rec.action && (
                  <div className="bg-muted p-3 rounded-md mb-3 font-mono text-sm">
                    {rec.action}
                  </div>
                )}
                
                {rec.alternatives && rec.alternatives.length > 0 && (
                  <div className="mb-3">
                    <p className="text-sm font-medium mb-2">Alternatives:</p>
                    <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                      {rec.alternatives.map((alt, altIndex) => (
                        <li key={altIndex}>{alt}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {rec.platforms && rec.platforms.length > 0 && (
                  <div className="mb-3">
                    <p className="text-sm font-medium mb-2">Platforms:</p>
                    <div className="flex flex-wrap gap-2">
                      {rec.platforms.map((platform, platformIndex) => (
                        <Badge key={platformIndex} variant="secondary">
                          {platform}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
                
                {rec.url && (
                  <a 
                    href={rec.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-sm text-primary hover:underline inline-flex items-center gap-1"
                  >
                    🔗 Learn more
                  </a>
                )}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
    </Card>
  )
}