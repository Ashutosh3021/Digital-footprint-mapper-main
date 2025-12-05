"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface Prediction {
  username: string
  platform: string
  confidence: number
  reason: string
  likely_platforms: string[]
}

interface PredictionRiskAssessment {
  total_predictions: number
  high_confidence: number
  medium_confidence: number
  low_confidence: number
  risk_summary: string
}

interface UsernamePredictionsProps {
  predictions: Prediction[]
  predictionsRisk: PredictionRiskAssessment
}

export function UsernamePredictions({ predictions, predictionsRisk }: UsernamePredictionsProps) {
  if (!predictions || predictions.length === 0) {
    return null
  }

  const topPredictions = predictions.slice(0, 10)

  const checkUsername = (username: string) => {
    // Open username checker on known platforms
    const platforms = {
      'instagram': `https://instagram.com/${username}`,
      'tiktok': `https://tiktok.com/@${username}`,
      'twitter': `https://twitter.com/${username}`,
      'github': `https://github.com/${username}`
    }

    // Check all platforms
    Object.values(platforms).forEach(url => {
      window.open(url, '_blank')
    })
  }

  return (
    <Card className="border border-border bg-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-lg">
            <span>🤖 Predicted Usernames (Self-Learning AI)</span>
          </CardTitle>
          <Badge variant="secondary">
            {predictions.length} predictions
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground text-sm mb-4">
          Based on pattern analysis, these usernames likely belong to you on other platforms:
        </p>

        <div className="space-y-3">
          {topPredictions.map((pred, index) => (
            <div 
              key={index}
              className="grid grid-cols-1 md:grid-cols-4 gap-4 items-center p-3 rounded-lg border border-border bg-muted/50"
            >
              <div className="font-mono text-primary font-medium break-all">
                {pred.username}
              </div>
              
              <div>
                <div className="flex flex-wrap gap-1">
                  {pred.likely_platforms.slice(0, 2).map((plat, platIndex) => (
                    <Badge key={platIndex} variant="secondary" className="text-xs">
                      {plat}
                    </Badge>
                  ))}
                  {pred.likely_platforms.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{pred.likely_platforms.length - 2} more
                    </Badge>
                  )}
                </div>
              </div>
              
              <div>
                <div className="flex items-center gap-2">
                  <div className="w-16 h-2 bg-muted rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-yellow-500 to-orange-500"
                      style={{ width: `${pred.confidence * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-xs font-bold text-yellow-500 min-w-[30px]">
                    {(pred.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">{pred.reason}</p>
              </div>
              
              <div className="flex justify-end">
                <Button 
                  size="sm" 
                  variant="secondary" 
                  onClick={() => checkUsername(pred.username)}
                  className="text-xs"
                >
                  🔍 Check
                </Button>
              </div>
            </div>
          ))}
        </div>

        {predictionsRisk && (
          <div className="mt-6 p-4 bg-orange-500/10 rounded-lg border border-orange-500/30">
            <strong className="text-orange-500 text-sm">⚠️ Prediction Risk:</strong>
            <p className="text-muted-foreground text-sm mt-1">
              {predictionsRisk.risk_summary}. Attackers can use these to target accounts.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}