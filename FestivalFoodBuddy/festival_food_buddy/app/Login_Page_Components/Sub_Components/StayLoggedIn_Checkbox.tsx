'use client'
// React Imports
import React from 'react';

// Prime React Imports
import { Checkbox } from "primereact/checkbox";

interface StayLoggedInCheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
}

function StayLoggedInCheckbox({ checked, onChange }: StayLoggedInCheckboxProps) {

    return (
        <div
            style={{
                margin: "5px",
                padding: "10px",
                display: "flex",
                flexDirection: "row",
                alignItems: "center"

            }}
        >
            <Checkbox
                onChange={e => onChange(e.checked ?? false)}
                checked={checked}
            />
            <label
                style={{
                fontSize: "120%"
                }}
            >
                Eingeloggt bleiben
            </label>
        </div>
    );
}

export default StayLoggedInCheckbox;