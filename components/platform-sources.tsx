"use client"

import type React from "react"

import { Card } from "@/components/ui/card"
import {
  Github,
  Linkedin,
  Twitter,
  Youtube,
  Mail,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  Facebook,
  Instagram,
  CircleUser,
} from "lucide-react"
import type { PlatformLink } from "@/lib/types"

interface PlatformSourcesProps {
  platforms: PlatformLink[]
}

const platformIcons: Record<string, React.ReactNode> = {
  Email: <Mail className="w-4 h-4" />,
  GitHub: <Github className="w-4 h-4" />,
  LinkedIn: <Linkedin className="w-4 h-4" />,
  Twitter: <Twitter className="w-4 h-4" />,
  Reddit: <CircleUser className="w-4 h-4" />,
  Facebook: <Facebook className="w-4 h-4" />,
  Instagram: <Instagram className="w-4 h-4" />,
  YouTube: <Youtube className="w-4 h-4" />,
}

const sourceLabels: Record<string, { label: string; color: string }> = {
  mandatory: { label: "Required", color: "bg-primary/20 text-primary border-primary/30" },
  optional: { label: "Optional", color: "bg-info/20 text-info border-info/30" },
  discovered: { label: "Discovered", color: "bg-warning/20 text-warning border-warning/30" },
}

export function PlatformSources({ platforms }: PlatformSourcesProps) {
  if (!platforms) {
    return null;
  }
  
  const mandatoryPlatforms = platforms.filter((p) => p.source === "mandatory")
  const optionalPlatforms = platforms.filter((p) => p.source === "optional")
  const discoveredPlatforms = platforms.filter((p) => p.source === "discovered")

  return (
    <Card className="p-4 bg-card border-border">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-foreground">Platform Sources</h3>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-primary" />
            Required
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-info" />
            Optional
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-warning" />
            Discovered
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {/* Mandatory Platforms */}
        {mandatoryPlatforms.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Required Inputs</p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {mandatoryPlatforms.map((platform) => (
                <PlatformCard key={platform.name} platform={platform} />
              ))}
            </div>
          </div>
        )}

        {/* Optional Platforms */}
        {optionalPlatforms.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Optional Inputs</p>
            <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-2">
              {optionalPlatforms.map((platform) => (
                <PlatformCard key={platform.name} platform={platform} />
              ))}
            </div>
          </div>
        )}

        {/* Discovered Platforms */}
        {discoveredPlatforms.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              Auto-Discovered from Scan
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-5 gap-2">
              {discoveredPlatforms.map((platform) => (
                <PlatformCard key={platform.name} platform={platform} />
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  )
}

function PlatformCard({ platform }: { platform: PlatformLink }) {
  const sourceStyle = sourceLabels[platform.source]

  return (
    <div className="flex items-center gap-3 p-3 bg-secondary/50 rounded-lg border border-border/50 hover:border-border transition-colors group">
      <div className={`p-2 rounded-md ${sourceStyle.color}`}>
        {platformIcons[platform.name] || <ExternalLink className="w-4 h-4" />}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-foreground">{platform.name}</span>
          {platform.verified ? (
            <CheckCircle2 className="w-3.5 h-3.5 text-safe" />
          ) : (
            <AlertCircle className="w-3.5 h-3.5 text-warning" />
          )}
        </div>
        <p className="text-xs text-muted-foreground truncate">{platform.handle}</p>
      </div>
      {platform.url && (
        <a
          href={platform.url}
          target="_blank"
          rel="noopener noreferrer"
          className="p-1.5 text-muted-foreground hover:text-foreground transition-colors opacity-0 group-hover:opacity-100"
        >
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      )}
    </div>
  )
}
