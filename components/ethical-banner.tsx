"use client"

import { useState } from "react"
import { Shield, X } from "lucide-react"

export function EthicalBanner() {
  const [isVisible, setIsVisible] = useState(true)

  if (!isVisible) return null

  return (
    <div className="bg-primary/10 border-b border-primary/20">
      <div className="max-w-[1600px] mx-auto px-6 py-2 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm">
          <Shield className="w-4 h-4 text-primary" />
          <span className="text-primary font-medium">Ethical Use Notice:</span>
          <span className="text-foreground/80">
            This tool analyzes only publicly available data for security awareness and defense purposes, not
            exploitation.
          </span>
        </div>
        <button
          onClick={() => setIsVisible(false)}
          className="text-muted-foreground hover:text-foreground transition-colors"
          aria-label="Dismiss banner"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  )
}
