"use client"

import type React from "react"

import { useEffect, useRef, useState, useCallback } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ZoomIn, ZoomOut, Maximize2, X } from "lucide-react"
import type { ScanResult } from "@/lib/types"

interface GraphNode {
  id: string
  label: string
  type: string
  x: number
  y: number
  details: Record<string, any>
}

interface GraphEdge {
  source: string
  target: string
  relationship: string
}

interface IntelligenceGraphProps {
  data: ScanResult
  selectedNode: string | null
  onNodeSelect: (nodeId: string | null) => void
}

function generateGraphData(data: ScanResult): { nodes: GraphNode[]; edges: GraphEdge[] } {
  const nodes: GraphNode[] = []
  const edges: GraphEdge[] = []

  // Use the graph_data from the actual ScanResult structure
  if (data.graph_data) {
    // Convert the graph_data structure to the expected format
    data.graph_data.nodes.forEach((nodeData, i) => {
      nodes.push({
        id: nodeData.id,
        label: nodeData.label,
        type: nodeData.type,
        x: 400 + Math.cos(i * 0.5) * 150, // Position based on index
        y: 300 + Math.sin(i * 0.5) * 150,
        details: nodeData.attributes || {},
      });
    });
    
    data.graph_data.edges.forEach((edgeData) => {
      edges.push({
        source: edgeData.from,
        target: edgeData.to,
        relationship: edgeData.title || "connected",
      });
    });
  }

  return { nodes, edges }
}

export function IntelligenceGraph({ data, selectedNode, onNodeSelect }: IntelligenceGraphProps) {
  if (!data) {
    return null;
  }
  
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null)
  const [graphData] = useState(() => generateGraphData(data))
  const [nodePositions, setNodePositions] = useState<Map<string, { x: number; y: number }>>(
    () => new Map(graphData.nodes.map((n) => [n.id, { x: n.x, y: n.y }])),
  )
  const [draggingNode, setDraggingNode] = useState<string | null>(null)

  const getNodeColor = (type: string) => {
    // Enhanced color scheme based on the new.md specification
    const nodeColors: Record<string, string> = {
      'person': '#ff6b35',      // Orange - CENTER FOCUS
      'email': '#4ecdc4',       // Cyan - CONTACTS
      'repository': '#ffd166',  // Gold - PROJECTS
      'sensitive_data': '#ff0054', // RED - DANGER
      'organization': '#06ffa5', // Green - WORK
      'platform': '#9d4edd',    // Purple - SOCIAL
      'account': '#a0c4ff',     // Light Blue - ACCOUNT
      'identity': '#186ba0',    // Dark Blue - Identity
      'location': '#ffb6c1',    // Pink - Location
      'website': '#8a2be2',     // Blue Violet - Website
      'domain': '#daa520',      // Goldenrod - Domain
      'user': '#ff6b35',        // Orange - User (backward compatibility)
      'default': '#6b7280'      // Gray - Default
    };
    
    return nodeColors[type] || nodeColors['default'];
  }

  const getNodeSize = (type: string) => {
    // Enhanced size hierarchy based on the new.md specification
    const nodeSizes: Record<string, number> = {
      'person': 60,               // HUGE - center of attention
      'sensitive_data': 40,       // LARGE - highlight danger
      'repository': 28,
      'organization': 28,
      'email': 25,
      'platform': 24,
      'account': 22,
      'identity': 20,
      'location': 18,
      'website': 18,
      'domain': 16,
      'user': 30,                 // User (backward compatibility)
      'sensitive': 22,            // Sensitive (backward compatibility)
      'default': 20
    };
    
    return nodeSizes[type] || nodeSizes['default'];
  }

  const draw = useCallback(() => {
    const canvas = canvasRef.current
    const ctx = canvas?.getContext("2d")
    if (!canvas || !ctx) return

    const dpr = window.devicePixelRatio || 1
    const rect = canvas.getBoundingClientRect()
    canvas.width = rect.width * dpr
    canvas.height = rect.height * dpr
    ctx.scale(dpr, dpr)

    ctx.clearRect(0, 0, rect.width, rect.height)
    ctx.save()
    ctx.translate(pan.x, pan.y)
    ctx.scale(zoom, zoom)

    // Draw edges with labels
    graphData.edges.forEach((edge) => {
      const sourcePos = nodePositions.get(edge.source)
      const targetPos = nodePositions.get(edge.target)
      if (!sourcePos || !targetPos) return

      // Draw edge line
      ctx.beginPath()
      ctx.moveTo(sourcePos.x, sourcePos.y)
      ctx.lineTo(targetPos.x, targetPos.y)
      ctx.strokeStyle = "rgba(74, 144, 226, 0.6)"  // #4a90e2 with transparency
      ctx.lineWidth = 2
      ctx.stroke()

      // Draw edge label
      const midX = (sourcePos.x + targetPos.x) / 2;
      const midY = (sourcePos.y + targetPos.y) / 2;
      
      ctx.font = "10px Geist, sans-serif";
      ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      
      // Background for label
      const label = edge.relationship || "connected";
      const textWidth = ctx.measureText(label).width;
      ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
      ctx.fillRect(midX - textWidth/2 - 4, midY - 7, textWidth + 8, 14);
      
      // Label text
      ctx.fillStyle = "#ffffff";
      ctx.fillText(label, midX, midY);
    })

    // Draw nodes
    graphData.nodes.forEach((node) => {
      const pos = nodePositions.get(node.id)
      if (!pos) return

      const size = getNodeSize(node.type)
      const color = getNodeColor(node.type)
      const isHovered = hoveredNode?.id === node.id
      const isSelected = selectedNode === node.id

      // Glow effect for sensitive data nodes
      if (node.type === "sensitive_data" || node.type === "sensitive") {
        ctx.beginPath()
        ctx.arc(pos.x, pos.y, size + 8, 0, Math.PI * 2)
        const gradient = ctx.createRadialGradient(pos.x, pos.y, size, pos.x, pos.y, size + 8)
        gradient.addColorStop(0, "rgba(255, 0, 84, 0.4)")  // #ff0054 with transparency
        gradient.addColorStop(1, "rgba(255, 0, 84, 0)")
        ctx.fillStyle = gradient
        ctx.fill()
      }

      // Node circle with shadow effect
      ctx.beginPath()
      ctx.arc(pos.x, pos.y, size, 0, Math.PI * 2)
      ctx.fillStyle = isHovered || isSelected ? color : `${color}cc`
      ctx.fill()

      // Border
      ctx.strokeStyle = isHovered || isSelected ? "#ffffff" : "rgba(0, 0, 0, 0.3)"
      ctx.lineWidth = isHovered || isSelected ? 3 : 1
      ctx.stroke()

      // Node label
      ctx.font = "11px Geist, sans-serif"
      ctx.fillStyle = "#ffffff"
      ctx.textAlign = "center"
      ctx.textBaseline = "top"
      
      // Truncate long labels
      let label = node.label || node.id;
      if (label.length > 18) {
        label = label.substring(0, 15) + "...";
      }
      
      ctx.fillText(label, pos.x, pos.y + size + 5)
      
      // Add icon or indicator for special node types
      if (node.type === "sensitive_data" || node.type === "sensitive") {
        // Draw warning icon
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 14px Geist, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("⚠", pos.x, pos.y);
      }
    })

    ctx.restore()
  }, [graphData, nodePositions, zoom, pan, hoveredNode, selectedNode])

  useEffect(() => {
    draw()
  }, [draw])

  useEffect(() => {
    const handleResize = () => draw()
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [draw])

  const getNodeAtPosition = (clientX: number, clientY: number): GraphNode | null => {
    const canvas = canvasRef.current
    if (!canvas) return null

    const rect = canvas.getBoundingClientRect()
    const x = (clientX - rect.left - pan.x) / zoom
    const y = (clientY - rect.top - pan.y) / zoom

    for (const node of graphData.nodes) {
      const pos = nodePositions.get(node.id)
      if (!pos) continue
      const size = getNodeSize(node.type)
      const dist = Math.sqrt((x - pos.x) ** 2 + (y - pos.y) ** 2)
      if (dist <= size) return node
    }
    return null
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    const canvas = canvasRef.current
    if (!canvas) return

    if (draggingNode) {
      const rect = canvas.getBoundingClientRect()
      const x = (e.clientX - rect.left - pan.x) / zoom
      const y = (e.clientY - rect.top - pan.y) / zoom
      setNodePositions((prev) => new Map(prev).set(draggingNode, { x, y }))
      return
    }

    if (isDragging) {
      setPan({
        x: pan.x + (e.clientX - dragStart.x),
        y: pan.y + (e.clientY - dragStart.y),
      })
      setDragStart({ x: e.clientX, y: e.clientY })
      return
    }

    const node = getNodeAtPosition(e.clientX, e.clientY)
    setHoveredNode(node)
    canvas.style.cursor = node ? "pointer" : "grab"
  }

  const handleMouseDown = (e: React.MouseEvent) => {
    const node = getNodeAtPosition(e.clientX, e.clientY)
    if (node) {
      setDraggingNode(node.id)
    } else {
      setIsDragging(true)
      setDragStart({ x: e.clientX, y: e.clientY })
    }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
    setDraggingNode(null)
  }

  const handleClick = (e: React.MouseEvent) => {
    const node = getNodeAtPosition(e.clientX, e.clientY)
    onNodeSelect(node?.id || null)
  }

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.9 : 1.1
    setZoom((z) => Math.min(Math.max(z * delta, 0.5), 2))
  }

  const selectedNodeData = selectedNode ? graphData.nodes.find((n) => n.id === selectedNode) : null

  return (
    <Card className="bg-card border-border overflow-hidden">
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-foreground">Intelligence Graph</h3>
          <p className="text-sm text-muted-foreground">
            Click and drag nodes to explore relationships. Hover for details.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon" onClick={() => setZoom((z) => Math.min(z * 1.2, 2))}>
            <ZoomIn className="w-4 h-4" />
          </Button>
          <Button variant="outline" size="icon" onClick={() => setZoom((z) => Math.max(z * 0.8, 0.5))}>
            <ZoomOut className="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            onClick={() => {
              setZoom(1)
              setPan({ x: 0, y: 0 })
            }}
          >
            <Maximize2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="relative" ref={containerRef}>
        <canvas
          ref={canvasRef}
          className="w-full h-[400px]"
          onMouseMove={handleMouseMove}
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onClick={handleClick}
          onWheel={handleWheel}
        />

        {/* Legend */}
        {/* Enhanced Legend */}
        <div className="absolute bottom-4 left-4 bg-black/90 backdrop-blur-sm border-2 border-green-500 rounded-xl p-4 shadow-lg">
          <h4 className="text-green-500 text-xs font-bold mb-3 uppercase tracking-wider">🎯 Graph Legend</h4>
          <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
            {[
              { type: "person", label: "Target User", color: "#ff6b35", special: true },
              { type: "sensitive_data", label: "⚠️ SENSITIVE", color: "#ff0054", special: true },
              { type: "repository", label: "Repository", color: "#ffd166" },
              { type: "organization", label: "Organization", color: "#06ffa5" },
              { type: "email", label: "Email/Contact", color: "#4ecdc4" },
              { type: "platform", label: "Social Platform", color: "#9d4edd" },
            ].map(({ type, label, color, special }) => (
              <div key={type} className="flex items-center gap-2">
                <div 
                  className={`w-3 h-3 rounded-full ${special ? 'shadow-lg' : ''}`} 
                  style={{ 
                    backgroundColor: color,
                    boxShadow: special ? `0 0 8px ${color}80` : 'none'
                  }} 
                />
                <span className={`${special ? 'text-white font-bold' : 'text-gray-300'}`}>{label}</span>
              </div>
            ))}
          </div>
          <div className="mt-3 pt-2 border-t border-gray-700 text-xs text-gray-400">
            💡 <span className="font-bold">Tip:</span> Larger nodes = more important. Red nodes = danger!
          </div>
        </div>

        {/* Enhanced Hover tooltip */}
        {hoveredNode && !selectedNodeData && (
          <div className="absolute top-4 right-4 bg-gray-900 border-2 border-green-500 rounded-xl p-4 max-w-xs shadow-2xl">
            <div className="flex items-center gap-2 mb-3">
              <div 
                className="w-4 h-4 rounded-full shadow-lg" 
                style={{ 
                  backgroundColor: getNodeColor(hoveredNode.type),
                  boxShadow: `0 0 10px ${getNodeColor(hoveredNode.type)}80`
                }} 
              />
              <span className="font-bold text-white">{hoveredNode.type.toUpperCase()}</span>
            </div>
            
            <div className="mb-2">
              <p className="text-sm text-gray-300"><span className="font-semibold text-white">Value:</span> {hoveredNode.label}</p>
            </div>
            
            {hoveredNode.details?.description && (
              <div className="mb-2">
                <p className="text-sm text-gray-400">{hoveredNode.details.description}</p>
              </div>
            )}
            
            {hoveredNode.details?.severity && (
              <div className="mb-2">
                <p className="text-sm text-red-400 font-bold">⚠️ Severity: {hoveredNode.details.severity}</p>
              </div>
            )}
            
            {hoveredNode.details?.stars && (
              <div className="mb-2">
                <p className="text-sm text-yellow-400">⭐ {hoveredNode.details.stars} stars</p>
              </div>
            )}
            
            {hoveredNode.details?.language && (
              <div className="mb-2">
                <p className="text-sm text-blue-400">💻 Language: {hoveredNode.details.language}</p>
              </div>
            )}
            
            {hoveredNode.details?.platform_name && (
              <div className="mb-2">
                <p className="text-sm text-purple-400">📱 Platform: {hoveredNode.details.platform_name}</p>
              </div>
            )}
          </div>
        )}

        {/* Selected node drawer */}
        {selectedNodeData && (
          <div className="absolute top-0 right-0 bottom-0 w-80 bg-card border-l border-border p-4 overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: getNodeColor(selectedNodeData.type) }}
                />
                <span className="font-semibold text-foreground">{selectedNodeData.label}</span>
              </div>
              <Button variant="ghost" size="icon" onClick={() => onNodeSelect(null)}>
                <X className="w-4 h-4" />
              </Button>
            </div>
            <div className="space-y-3">
              <div>
                <span className="text-xs text-muted-foreground uppercase tracking-wider">Type</span>
                <p className="text-sm text-foreground capitalize">{selectedNodeData.type}</p>
              </div>
              <div>
                <span className="text-xs text-muted-foreground uppercase tracking-wider">Description</span>
                <p className="text-sm text-foreground">{selectedNodeData.details?.description}</p>
              </div>
              {selectedNodeData.details?.url && (
                <div>
                  <span className="text-xs text-muted-foreground uppercase tracking-wider">URL</span>
                  <a
                    href={selectedNodeData.details.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary hover:underline block truncate"
                  >
                    {selectedNodeData.details.url}
                  </a>
                </div>
              )}
              {selectedNodeData.details?.platforms && (
                <div>
                  <span className="text-xs text-muted-foreground uppercase tracking-wider">Connected Platforms</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {selectedNodeData.details.platforms.map((p: any) => (
                      <span key={p} className="px-2 py-0.5 bg-secondary text-secondary-foreground rounded text-xs">
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </Card>
  )
}
