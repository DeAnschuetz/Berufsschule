// Icon Imports
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCartShopping } from '@fortawesome/free-solid-svg-icons'

interface ShoppingCartIconPros {
    currentShoppingCartCount: number;
    onMenuItemPressed: (item: string) => void;
}

function ShoppingCartIcon({ currentShoppingCartCount, onMenuItemPressed }: ShoppingCartIconPros) {
    return (
        <div style={{ position: "relative" }}>
            <FontAwesomeIcon
                icon={faCartShopping}
                onClick={() => onMenuItemPressed('ShoppingCart')}
                style={{ color: "black", width: "30px", height: "30px"}}
            />
            <span
                style={{
                    position: "absolute",
                    top: "-4px",
                    right: "-8px",
                    backgroundColor: "red",
                    color: "white",
                    fontSize: "10px",
                    borderRadius: "50%",
                    padding: "0 4px",
                }}
            >
                {currentShoppingCartCount}
            </span>
            </div>
    );
}

export default ShoppingCartIcon;