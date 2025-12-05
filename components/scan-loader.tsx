"use client"

export function ScanLoader() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh]">
      {/* Custom bird/arrow loader */}
      <div className="loader mb-8" />

      <p className="text-foreground font-medium mb-2">Scanning public data sources...</p>
      <p className="text-muted-foreground text-sm max-w-md text-center">
        Analyzing GitHub repositories, social profiles, and checking breach databases across platforms.
      </p>

      <style jsx>{`
        .loader {
          width: calc(6 * 30px);
          height: 50px;
          display: flex;
          color: hsl(var(--primary));
          filter: drop-shadow(30px 25px 0 currentColor) 
                  drop-shadow(60px 0 0 currentColor) 
                  drop-shadow(120px 0 0 currentColor);
          clip-path: inset(0 100% 0 0);
          animation: l11 2s infinite steps(7);
        }
        
        .loader:before {
          content: "";
          width: 30px;
          height: 25px;
          background: currentColor;
          clip-path: polygon(
            0 50%,
            30% 40%,
            100% 0,
            60% 40%,
            100% 50%,
            60% 60%,
            100% 100%,
            30% 60%
          );
        }
        
        @keyframes l11 {
          100% {
            clip-path: inset(0 -30px 0 0);
          }
        }
      `}</style>
    </div>
  )
}
