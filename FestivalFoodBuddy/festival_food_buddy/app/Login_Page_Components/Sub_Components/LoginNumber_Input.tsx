'use client'
import React from 'react';
import { InputMask } from 'primereact/inputmask';

interface LoginNumberInputProps {
    value: string;
    onChange: (value: string) => void;
}

export function LoginNumberInput({ value, onChange }: LoginNumberInputProps) {
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
        <label style={{ fontSize: "150%" }}>Login-Nr.</label>
        <InputMask
            style={{ width: "223px" }}
            value={value}
            onChange={(e) => onChange(e.target.value ?? '')}
            mask="a-999-999"
            placeholder="B-111-111"
            tabIndex={1}
        />
    </div>
  );
}

export default LoginNumberInput;