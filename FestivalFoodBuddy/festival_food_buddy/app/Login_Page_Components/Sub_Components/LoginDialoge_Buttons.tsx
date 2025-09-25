'use client'
// React Imports
import React from 'react';

// Prime React Imports
import { Button } from 'primereact/button';

interface ButtonConfig {
    label: string;
    onClick: () => void;
    disabled?: boolean;
}

interface ButtonRowProps {
    buttons: ButtonConfig[];
}

export function ButtonRow({ buttons }: ButtonRowProps) {
    return (
        <div
            style={{
                width: "100%",
                margin: "5px",
                padding: "10px",
                display: "flex",
                justifyContent: "space-around",
            }}
        >
            {buttons.map((btn, index) => (
                <Button
                    key={index}
                    style={{ margin: "5px" }}
                    label={btn.label}
                    onClick={btn.onClick}
                    disabled={btn.disabled}
                />
            ))}
        </div>
    );
}

export default ButtonRow;
