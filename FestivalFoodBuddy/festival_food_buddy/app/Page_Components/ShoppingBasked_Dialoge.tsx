import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faHourglassHalf, faTimes, faCoins, } from "@fortawesome/free-solid-svg-icons";

interface WarenkorbDialogPros {
    changeActivePage: (item: string) => void;
    addCredits: (creditBalanceToAdd: number) => void;
}


export default function WarenkorbDialog({ changeActivePage, addCredits }: WarenkorbDialogPros) {
  const [items, setItems] = useState([
    { name: "Cheeseburger*", qty: 3, price: 8.0 },
    { name: "Hamburger", qty: 3, price: 8.0 },
    { name: "Pommes Frites", qty: 3, price: 8.0 },
  ]);

  const updateQty = (index: any, newQty: any) => {
    const updated = [...items];
    updated[index].qty = newQty;
    setItems(updated);
  };

  const removeItem = (index: any) => {
    const updated = [...items];
    updated.splice(index, 1);
    setItems(updated);
  };

  const total = items.reduce((sum, i) => sum + i.qty * i.price, 0);

  return (
    <div
      style={{
        height: "672px",
        backgroundColor: "#fff",
        border: "1px solid #ccc",
        borderRadius: "8px",
        boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "8px 12px",
          fontWeight: "bold",
          color: "black",
          borderBottom: "1px solid #ccc",
        }}
      >
        Warenkorb
        <button
          onClick={() => changeActivePage('MainPage')}
          style={{
            border: "none",
            background: "transparent",
            cursor: "pointer",
            fontSize: "16px",
          }}
        >
          <FontAwesomeIcon icon={faTimes} />
        </button>
      </div>
      <div
        style={{
            backgroundColor: "#aab9ff",
            padding: "10px",
            minHeight: "120px",
            color: "black", 
        }}
      >
        {items.map((item, i) => (
          <div
            key={i}
            style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                marginBottom: "8px",
            }}
          >
            <span style={{ flex: 1 }}>{item.name}</span>
            <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
              <span>X</span>
              <input
                type="number"
                value={item.qty}
                min={1}
                onChange={(e) => updateQty(i, parseInt(e.target.value))}
                style={{
                    width: "40px",
                    padding: "2px",
                    textAlign: "center",
                }}
              />
              <button
                onClick={() => removeItem(i)}
                style={{
                  border: "none",
                  background: "transparent",
                  cursor: "pointer",
                  color: "red",
                }}
              >
                <FontAwesomeIcon icon={faTrash} />
              </button>
              <span>{(item.price).toFixed(2)}</span>
              <FontAwesomeIcon icon={faCoins} />
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: "10px" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            fontWeight: "bold",
            marginBottom: "8px",
            color: "black",

          }}
        >
          <span>Gesamt</span>
          <span>
            {total.toFixed(2)} <FontAwesomeIcon icon={faCoins} />
          </span>
        </div>

        <div style={{ fontSize: "14px", marginBottom: "12px", color: "black" }}>
          geschätzte Zubereitungszeit
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontWeight: "bold",
              marginTop: "4px",
            }}
          >
            <FontAwesomeIcon icon={faHourglassHalf} /> 30 Min
          </div>
        </div>

        <button
            onClick={() => addCredits(-total)}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#aab9ff",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Bestellen
        </button>
      </div>
    </div>
  );
}
