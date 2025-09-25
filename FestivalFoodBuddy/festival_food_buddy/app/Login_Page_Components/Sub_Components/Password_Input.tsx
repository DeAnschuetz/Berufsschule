'use client'
import React from 'react';
import { Password } from 'primereact/password';

interface PasswordInputProps {
    value: string;
    label: string;
    onChange: (value: string) => void;
}

export function PasswordInput({ value, label, onChange }: PasswordInputProps) {
  return (
    <div
        style={{
            width: "223px",
            margin: "5px",
            display: "flex",
            flexDirection: "column",
            alignItems: "flex-start",
        }}
    >
        <label style={{ fontSize: "100%" }}>{label}</label>
        <Password
            value={value}
            onChange={(e) => onChange(e.target.value ?? '')}
            feedback={false}
            tabIndex={2}
            toggleMask
        />
    </div>
  );
}

export default PasswordInput;
