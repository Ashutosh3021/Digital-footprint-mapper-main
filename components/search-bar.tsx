"use client"

import type React from "react"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import {
  Search,
  Loader2,
  Mail,
  Github,
  Linkedin,
  Twitter,
  ChevronDown,
  ChevronUp,
  Youtube,
  CircleUser,
  Facebook,
  Instagram,
} from "lucide-react"
import type { ScanInput } from "@/lib/types"

interface SearchBarProps {
  onSearch: (inputs: ScanInput) => void
  isLoading: boolean
}

export function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [inputs, setInputs] = useState<ScanInput>({
    email: "",
    github: "",
    linkedin: "",
  })

  const handleChange = (field: keyof ScanInput, value: string) => {
    setInputs((prev: ScanInput) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (inputs.email.trim() && inputs.github.trim() && inputs.linkedin.trim()) {
      // Prepare the inputs to send - only include optional fields if they have values
      const preparedInputs: ScanInput = {
        email: inputs.email,
        github: inputs.github,
        linkedin: inputs.linkedin,
      }
      
      // Add optional fields only if they have values
      if (inputs.twitter?.trim()) preparedInputs.twitter = inputs.twitter
      if (inputs.reddit?.trim()) preparedInputs.reddit = inputs.reddit
      if (inputs.facebook?.trim()) preparedInputs.facebook = inputs.facebook
      if (inputs.instagram?.trim()) preparedInputs.instagram = inputs.instagram
      if (inputs.youtube?.trim()) preparedInputs.youtube = inputs.youtube
      
      onSearch(preparedInputs)
    }
  }

  const isValid = inputs.email.trim() && inputs.github.trim() && inputs.linkedin.trim()

  // Count optional fields that have values
  const optionalFieldsCount = [
    inputs.twitter?.trim(),
    inputs.reddit?.trim(),
    inputs.facebook?.trim(),
    inputs.instagram?.trim(),
    inputs.youtube?.trim()
  ].filter(Boolean).length

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Mandatory Fields Row */}
        <div className="flex flex-wrap items-end gap-3">
          <div className="flex-1 min-w-[200px]">
            <Label htmlFor="email" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
              <Mail className="w-3 h-3" />
              Email <span className="text-critical">*</span>
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="user@example.com"
              value={inputs.email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("email", e.target.value)}
              className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
              disabled={isLoading}
              required
            />
          </div>
          <div className="flex-1 min-w-[200px]">
            <Label htmlFor="github" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
              <Github className="w-3 h-3" />
              GitHub <span className="text-critical">*</span>
            </Label>
            <Input
              id="github"
              type="text"
              placeholder="username"
              value={inputs.github}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("github", e.target.value)}
              className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
              disabled={isLoading}
              required
            />
          </div>
          <div className="flex-1 min-w-[200px]">
            <Label htmlFor="linkedin" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
              <Linkedin className="w-3 h-3" />
              LinkedIn <span className="text-critical">*</span>
            </Label>
            <Input
              id="linkedin"
              type="text"
              placeholder="profile URL or username"
              value={inputs.linkedin}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("linkedin", e.target.value)}
              className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
              disabled={isLoading}
              required
            />
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="h-9 gap-1.5 border-border text-muted-foreground hover:text-foreground"
          >
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            {optionalFieldsCount > 0 ? `${optionalFieldsCount} Optional` : "Optional"}
          </Button>
          <Button type="submit" disabled={isLoading || !isValid} className="h-9 bg-primary hover:bg-primary/90 gap-2">
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Scanning...
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                Analyze
              </>
            )}
          </Button>
        </div>

        {/* Optional Fields - Collapsible */}
        {isExpanded && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 p-4 bg-secondary/50 rounded-lg border border-border/50">
            <div>
              <Label htmlFor="twitter" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
                <Twitter className="w-3 h-3" />
                Twitter / X
              </Label>
              <Input
                id="twitter"
                type="text"
                placeholder="@handle"
                value={inputs.twitter || ""}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("twitter", e.target.value)}
                className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
                disabled={isLoading}
              />
            </div>
            <div>
              <Label htmlFor="reddit" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
                <CircleUser className="w-3 h-3" />
                Reddit
              </Label>
              <Input
                id="reddit"
                type="text"
                placeholder="u/username"
                value={inputs.reddit || ""}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("reddit", e.target.value)}
                className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
                disabled={isLoading}
              />
            </div>
            <div>
              <Label htmlFor="facebook" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
                <Facebook className="w-3 h-3" />
                Facebook
              </Label>
              <Input
                id="facebook"
                type="text"
                placeholder="profile ID or name"
                value={inputs.facebook || ""}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("facebook", e.target.value)}
                className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
                disabled={isLoading}
              />
            </div>
            <div>
              <Label htmlFor="instagram" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
                <Instagram className="w-3 h-3" />
                Instagram
              </Label>
              <Input
                id="instagram"
                type="text"
                placeholder="@handle"
                value={inputs.instagram || ""}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("instagram", e.target.value)}
                className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
                disabled={isLoading}
              />
            </div>
            <div>
              <Label htmlFor="youtube" className="text-xs text-muted-foreground mb-1.5 flex items-center gap-1.5">
                <Youtube className="w-3 h-3" />
                YouTube
              </Label>
              <Input
                id="youtube"
                type="text"
                placeholder="channel ID or name"
                value={inputs.youtube || ""}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("youtube", e.target.value)}
                className="bg-secondary border-border text-foreground placeholder:text-muted-foreground h-9"
                disabled={isLoading}
              />
            </div>
          </div>
        )}
      </form>
    </div>
  )
}