"use client"

import { useState } from "react"
import { SearchBar } from "@/components/search-bar"
import { EthicalBanner } from "@/components/ethical-banner"
import { ExposureSummary } from "@/components/exposure-summary"
import { RiskScorePanel } from "@/components/risk-score-panel"
import { IntelligenceGraph } from "@/components/intelligence-graph"
import { TrackersPanel } from "@/components/trackers-panel"
import { DetailedFindings } from "@/components/detailed-findings"
import { PlatformSources } from "@/components/platform-sources"
import { ScanLoader } from "@/components/scan-loader"
import { RecommendedNextSteps } from "@/components/recommended-next-steps"
import { ExposureTimeline } from "@/components/exposure-timeline"
import { ThreatIntelligence } from "@/components/threat-intelligence"
import { UsernamePredictions } from "@/components/username-predictions"
import type { ScanResult, ScanInput } from "@/lib/types"

export default function DashboardPage() {
  const [scanResult, setScanResult] = useState<ScanResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedNode, setSelectedNode] = useState<string | null>(null)

  const handleSearch = async (inputs: ScanInput) => {
    setIsLoading(true)
    setSelectedNode(null)
    setScanResult(null)

    try {
      // Make actual API call to backend
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/v1/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputs),
      })
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
      const data: ScanResult = await response.json();
      setScanResult(data);
    } catch (error: any) {
      console.error("[v0] Scan failed:", error);
      
      // Provide more specific error messages
      let errorMessage = "Scan failed. Please check the console for details.";
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const isNetworkAccessError = error.message.includes('private address space');
        
        if (isNetworkAccessError) {
          errorMessage = `Network access error: The browser is blocking access to the backend server due to secure context restrictions.

Solutions:
1. Access the application at http://localhost:8000 instead of http://20.3.7.200:8000
2. Or ensure both frontend and backend are running on the same network interface

To start the backend:
1. Open a terminal in the project root directory
2. Run: cd backend
3. Run: python main.py

Alternatively, run the start_system.bat file to start both frontend (port 8000) and backend (port 8001).`;
        } else {
          errorMessage = `Failed to connect to the backend server. Please make sure the backend is running on ${apiUrl} (port 8001).

To start the backend:
1. Open a terminal in the project root directory
2. Run: cd backend
3. Run: python main.py

Alternatively, run the start_system.bat file to start both frontend (port 8000) and backend (port 8001).`;
        }
      } else if (error.message) {
        errorMessage = `Scan failed: ${error.message}`;
      }
      
      // Show error to user
      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <EthicalBanner />

      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-6 py-4">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3 shrink-0">
              <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0 1 12 2.944a11.955 0 0 1 0 -8.618 3.04A12.02 12.02 0 0 0 3 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </div>
              <h1 className="text-xl font-semibold text-foreground">ExposureIQ</h1>
            </div>
            {scanResult && (
              <div className="text-sm text-muted-foreground ml-auto">
                Last scan: <span className="text-foreground">{scanResult.email}</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-[1600px] mx-auto px-6 py-6">
        <div className="mb-6">
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {!scanResult && !isLoading ? (
          <div className="flex flex-col items-center justify-center min-h-[50vh] text-center">
            <div className="w-20 h-20 rounded-2xl bg-primary/10 flex items-center justify-center mb-6">
              <svg className="w-10 h-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-foreground mb-2">Enter details to begin analysis</h2>
            <p className="text-muted-foreground max-w-md">
              Provide email, GitHub, and LinkedIn (required) plus optional social profiles to analyze your public
              digital footprint and identify potential exposures.
            </p>
          </div>
        ) : isLoading ? (
          <ScanLoader />
        ) : (
          scanResult && (
            <div className="space-y-6">
              {scanResult && <PlatformSources platforms={scanResult.platforms} />}

              {scanResult && <ExposureSummary data={scanResult} />}

              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                <div className="xl:col-span-2">
                  {scanResult && <IntelligenceGraph data={scanResult} selectedNode={selectedNode} onNodeSelect={setSelectedNode} />}
                </div>
                <div>
                  {scanResult && <RiskScorePanel data={scanResult} />}
                </div>
              </div>

              {scanResult && <TrackersPanel trackers={scanResult.trackers} />}

              {scanResult && <DetailedFindings data={scanResult} />}

              {scanResult.recommendations && (
                <RecommendedNextSteps recommendations={scanResult.recommendations} />
              )}
              
              {scanResult.threat_intelligence && (
                <ThreatIntelligence threatIntelligence={scanResult.threat_intelligence} />
              )}
              
              {scanResult.timeline && scanResult.timeline.length > 0 && (
                <ExposureTimeline 
                  timeline={scanResult.timeline} 
                  timelineStats={scanResult.timeline_stats || {}} 
                />
              )}
              
              {scanResult.predictions && scanResult.predictions.length > 0 && (
                <UsernamePredictions 
                  predictions={scanResult.predictions as any} 
                  predictionsRisk={scanResult.predictions_risk!} 
                />
              )}
            </div>
          )
        )}
      </main>
    </div>
  )
}