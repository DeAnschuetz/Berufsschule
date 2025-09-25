import { useState } from "react";
import { Panel } from 'primereact/panel';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHourglassHalf, faPizzaSlice, faFish, faDrumstickBite } from "@fortawesome/free-solid-svg-icons";

export default function StandOverview() {
  const [stands] = useState([
    {
      name: "Pizza Place",
      waitTime: "30 Min",
      image: "🍕", // placeholder emoji, replace with real image
      items: [
        { icon: faPizzaSlice, qty: 30 },
        { icon: faDrumstickBite, qty: 20 },
      ],
    },
    {
      name: "Asia Place",
      waitTime: "1 Std",
      image: "🍣", // placeholder emoji, replace with real image
      items: [
        { icon: faFish, qty: 30 },
        { icon: faDrumstickBite, qty: 15 },
        { icon: faDrumstickBite, qty: 20 },
      ],
    },
  ]);

  return (
    <Panel
        header="Stand Übersicht"
        toggleable
        unstyled
        style={{
            backgroundColor: "#1f3a93",
        }}
    >
        <div
            style={{
                backgroundColor: "#fff",
                fontFamily: "Arial, sans-serif",
                display: "flex",
                flexDirection: "column",
            }}
        >
        <div style={{ flex: 1, overflowY: "auto", padding: "12px" }}>
            {stands.map((stand, index) => (
            <div
                key={index}
                style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                marginBottom: "12px",
                padding: "10px",
                backgroundColor: "#fff",
                color: "black",
                boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
                }}
            >
                <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: "8px",
                    fontWeight: "bold",
                }}
                >
                <span>{stand.name}</span>
                <span style={{ fontSize: "14px", display: "flex", alignItems: "center", gap: "6px" }}>
                    <FontAwesomeIcon icon={faHourglassHalf} />
                    {stand.waitTime}
                </span>
                </div>

                <div style={{ display: "flex", gap: "12px" }}>
                <div
                    style={{
                    width: "80px",
                    height: "80px",
                    fontSize: "50px",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    border: "1px solid #ccc",
                    borderRadius: "6px",
                    }}
                >
                    {stand.image}
                </div>

                <div
                    style={{
                    flex: 1,
                    backgroundColor: "#eef4ff",
                    padding: "8px",
                    borderRadius: "6px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "6px",
                    fontSize: "14px",
                    }}
                >
                    <span style={{ fontWeight: "bold", marginBottom: "4px" }}>Verfügbar</span>
                    {stand.items.map((item, i) => (
                    <div
                        key={i}
                        style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        }}
                    >
                        <FontAwesomeIcon icon={item.icon} /> {item.qty}
                    </div>
                    ))}
                </div>
                </div>
            </div>
            ))}
        </div>
        </div>
    </Panel>
  );
}
