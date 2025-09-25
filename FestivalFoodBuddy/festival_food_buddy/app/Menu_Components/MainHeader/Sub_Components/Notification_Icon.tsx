// Icon Imports
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBell } from '@fortawesome/free-solid-svg-icons'

interface NotificationIconProps {
    currentNotificationCount: number;
    onMenuItemPressed: (item: string) => void;
}

function NotificationIcon({ currentNotificationCount, onMenuItemPressed }: NotificationIconProps) {
    return (
        <div style={{ position: "relative" }}>
            <FontAwesomeIcon
                icon={faBell}
                onClick={() => onMenuItemPressed('Notifications')}
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
                {currentNotificationCount}
            </span>
        </div>
    );
}

export default NotificationIcon;