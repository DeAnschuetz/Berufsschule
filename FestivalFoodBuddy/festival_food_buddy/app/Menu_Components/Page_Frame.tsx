'use client';

// React Imports
import React, { ReactNode } from "react";

interface PageFrameProps {
  children: ReactNode;
}

export default function PageFrame({ children }: PageFrameProps) {
  return (
    <div
        style={{
            minWidth: "390px",
            minHeight: "852px",
            backgroundImage: "url('/Assets/Background.jpg')",
            backgroundSize: "100% 100%",
            backgroundRepeat: "no-repeat",
            display: "flex",
            flexDirection: "column",
        }}
    >
      {/* Top bar */}
      <div className="w-[100%] h-[3.125rem] bg-[#0d0d0d]" />

      {/* Main content area */}
      <div style={{ flex: 1 }}>{children}</div>

      {/* Bottom bar */}
      <div className="w-[100%] h-[3.125rem] bg-[#0d0d0d]" />
    </div>
  );
}