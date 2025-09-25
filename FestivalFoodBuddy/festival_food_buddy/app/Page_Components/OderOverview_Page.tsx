import { useState } from "react";

export default function OrdersDialog() {
  const [activeTab, setActiveTab] = useState("alle");

  const tabs = ["alle", "in Bearbeitung", "Abholbereit", "Abgeholt", "Storniert"];

  const orders = [
    {
      place: "Pizza Place",
      status: "in Bearbeitung",
      statusLabel: "30 Min",
      items: [
        { name: "Pizza Hawai", qty: 1 },
        { name: "Pizza Salame", qty: 2 },
        { name: "Pizza Speciale", qty: 3 },
      ],
    },
    {
      place: "Burger Place",
      status: "Abgeholt",
      statusLabel: "Abgeholt",
      items: [
        { name: "Cheeseburger", qty: 1 },
        { name: "Hamburger", qty: 2 },
        { name: "Pommes Frites", qty: 3 },
      ],
    },
    {
      place: "Sushi Place",
      status: "Storniert",
      statusLabel: "Storniert",
      items: [
        { name: "Nori Rolls", qty: 1 },
        { name: "Maki Rolls", qty: 2 },
        { name: "California Rolls", qty: 3 },
      ],
    },
  ];

  const filteredOrders =
    activeTab === "alle" ? orders : orders.filter((o) => o.status === activeTab);

  return (
    <div
      style={{
        color: "black",
        backgroundColor: "#fff",
        fontFamily: "Arial, sans-serif",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          backgroundColor: "#1f3a93",
          color: "#fff",
          fontWeight: "bold",
          padding: "10px 16px",
          fontSize: "18px",
        }}
      >
        Bestellungen
      </div>

      <div
        style={{
          display: "flex",
          borderBottom: "1px solid #ccc",
          backgroundColor: "#f7f7f7",
        }}
      >
        {tabs.map((tab) => (
          <div
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              flex: 1,
              textAlign: "center",
              padding: "5px",
              cursor: "pointer",
              fontSize: "100%",
              fontWeight: activeTab === tab ? "bold" : "normal",
              borderBottom: activeTab === tab ? "3px solid #1f3a93" : "none",
            }}
          >
            {tab}
          </div>
        ))}
      </div>
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "12px",
        }}
      >
        {filteredOrders.map((order, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ccc",
              borderRadius: "8px",
              marginBottom: "12px",
              padding: "10px",
              backgroundColor: "#fff",
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
              <span>{order.place}</span>
              <span style={{ fontSize: "14px", color: "#444" }}>
                {order.statusLabel}
              </span>
            </div>
            <div style={{ fontSize: "14px" }}>
              {order.items.map((item, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                  }}
                >
                  <span>{item.name}</span>
                  <span>x{item.qty}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
