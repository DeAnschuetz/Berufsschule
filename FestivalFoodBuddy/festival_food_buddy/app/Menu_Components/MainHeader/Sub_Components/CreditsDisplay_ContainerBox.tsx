// Icon Imports
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCreditCard } from '@fortawesome/free-regular-svg-icons'
import { faPlus } from '@fortawesome/free-solid-svg-icons'

interface CreditsDisplayProps {
    currentCreditBalance: number;
    onMenuItemPressed: (item: string) => void;
}

function CreditsDisplay({ currentCreditBalance, onMenuItemPressed }: CreditsDisplayProps) {
    return (
        <div
            style={{
                display: "flex",
                alignItems: "center",
                backgroundColor: "rgb(33 68 192 / 50%) ",
                padding: "2px 2px",
                borderLeft: "2px solid black",
                borderBottom: "2px solid black",
            }}
        >
            <FontAwesomeIcon icon={faCreditCard} style={{ width: "30px", height: "30px", color: "black" }}/>
            <span style={{ marginLeft: "4px", fontSize: "120%", color: "black" }}>{currentCreditBalance.toFixed(2)}</span>
            <FontAwesomeIcon
                icon={faPlus}
                onClick={() => onMenuItemPressed('Payment')}
                style={{ width: "30px", height: "30px", color: "black" }}
            />
        </div>
    );
}

export default CreditsDisplay;