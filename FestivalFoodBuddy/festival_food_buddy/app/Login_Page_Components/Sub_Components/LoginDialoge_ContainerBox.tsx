'use client'
import React, { ReactNode } from 'react';

interface DialogContainerProps {
  children: ReactNode;
}

export function DialogContainer({ children }: DialogContainerProps) {
  return (
    <div
      style={{
        width: "80%",
        borderRadius: "10px",
        padding: "10px",
        backgroundColor: "rgb(20 34 112 / 80%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      {children}
    </div>
  );
}

export default DialogContainer;
