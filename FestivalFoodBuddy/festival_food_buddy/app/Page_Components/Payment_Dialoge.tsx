import { useState } from "react";
import { InputNumber } from 'primereact/inputnumber';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faApplePay, faGooglePay, faCcVisa, faCcMastercard } from "@fortawesome/free-brands-svg-icons";

interface PaymentDialogeProps {
    changeActivePage: (item: string) => void;
    addCredits: (creditBalanceToAdd: number) => void;
}

function PaymentDialoge({ changeActivePage, addCredits }: PaymentDialogeProps) {
    const [amount, setAmount] = useState(0);
    const [method, setMethod] = useState("applepay");
    const [accepted, setAccepted] = useState(false);

    const handleSubmit = (e: any) => {
        e.preventDefault();
        //alert(`Amount: €${amount}, Method: ${method}`);
        // TODO
    };

    return (
        <div
            style={{
                height: "672px",
                backgroundColor: "#fff",
                borderRadius: "12px",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                padding: "20px",
                fontFamily: "Arial, sans-serif",
            }}
        >
            <h2 style={{ fontSize: "20px", color:"black", fontWeight: "bold", marginBottom: "16px" }}>
                Festival Credits aufladen
            </h2>

            <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div>
                    <label style={{ display: "block", color:"black", fontSize: "14px", marginBottom: "6px" }}>
                        Aufladebetrag
                    </label>
                    <InputNumber
                        value={amount}
                        onValueChange={(e) => setAmount(e.value ?? 0)}
                        minFractionDigits={2} maxFractionDigits={2}
                    />
                </div>
                <div>
                    <label style={{ display: "block", color:"black", fontSize: "14px", marginBottom: "6px" }}>
                        Zahlungsmethode
                    </label>
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns: "1fr 1fr",
                            gap: "12px",
                            backgroundColor: "rgb(33 68 192 / 50%) ",
                            padding: "12px",
                            borderRadius: "8px",
                        }}
                    >
                        <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                            <input
                                type="radio"
                                name="method"
                                value="applepay"
                                checked={method === "applepay"}
                                onChange={(e) => setMethod(e.target.value)}
                            />
                            <FontAwesomeIcon icon={faApplePay} style={{ color: "black" }} size="2x" />
                        </label>
                        <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                            <input
                                type="radio"
                                name="method"
                                value="googlepay"
                                checked={method === "googlepay"}
                                onChange={(e) => setMethod(e.target.value)}
                            />
                            <FontAwesomeIcon icon={faGooglePay} style={{ color: "black" }} size="2x" />
                        </label>
                        <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                            <input
                                type="radio"
                                name="method"
                                value="mastercard"
                                checked={method === "mastercard"}
                                onChange={(e) => setMethod(e.target.value)}
                            />
                            <FontAwesomeIcon icon={faCcMastercard} style={{ color: "black" }} size="2x" />
                        </label>
                        <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                            <input
                                type="radio"
                                name="method"
                                value="visa"
                                checked={method === "visa"}
                                onChange={(e) => setMethod(e.target.value)}
                            />
                            <FontAwesomeIcon icon={faCcVisa} style={{ color: "black" }} size="2x" />
                        </label>
                    </div>
                </div>
                <label style={{ display: "flex", color:"black", alignItems: "center", gap: "8px", fontSize: "13px" }}>
                    <input
                        type="checkbox"
                        checked={accepted}
                        onChange={(e) => setAccepted(e.target.checked)}
                    />
                    Ich habe die Allgemeinen Geschäftsbedingungen gelesen und akzeptiere diese
                </label>
                <div style={{ display: "flex", justifyContent: "space-between", marginTop: "10px" }}>
                    <button
                        type="button"
                        style={{
                            padding: "8px 14px",
                            borderRadius: "8px",
                            border: "none",
                            backgroundColor: "#D9D9D9",
                            color: "black",
                            cursor: "pointer",
                        }}
                        onClick={() => changeActivePage('MainPage')}
                    >
                        Abbrechen
                    </button>
                    <button
                        type="submit"
                        style={{
                            padding: "8px 14px",
                            borderRadius: "8px",
                            border: "none",
                            backgroundColor: "#3b82f6",
                            color: "black",
                            cursor: "pointer",
                        }}
                        //disabled={!accepted}
                        onClick={() => addCredits(amount)}
                    >
                        Bestätigen
                    </button>
                </div>
            </form>
        </div>
    );
}

export default PaymentDialoge;