'use client'

// Custom Component Imports
import CreditsDisplay from './Sub_Components/CreditsDisplay_ContainerBox';
import NotificationIcon from './Sub_Components/Notification_Icon';
import ShoppingCartIcon from './Sub_Components/ShoppingCart_Icon';
import UserMenuContainer from './Sub_Components/UserMenu_Container';

interface MainHeaderBarProps {
    loginNumber: string;
    creditBalance: number;
    notificationCount: number;
    shoppingCartCount: number;
    onMenuItemPressed: (item: string) => void;
}

function MainHeaderBar({ loginNumber, creditBalance, notificationCount, shoppingCartCount, onMenuItemPressed }: MainHeaderBarProps) {

    return (
        <div
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                backgroundColor: "white",
                border: "1px solid black",
                width: "100%",
                minHeight: "80px"
            }}
        >
            <UserMenuContainer
                loginNumber={loginNumber}
                onMenuItemPressed={onMenuItemPressed}
            />
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <ShoppingCartIcon 
                    currentShoppingCartCount={shoppingCartCount}
                    onMenuItemPressed={onMenuItemPressed}
                />
                <NotificationIcon
                    currentNotificationCount={notificationCount}
                    onMenuItemPressed={onMenuItemPressed}
                />
                <CreditsDisplay
                    currentCreditBalance={creditBalance}
                    onMenuItemPressed={onMenuItemPressed}
                />
            </div>
        </div>
    );
}

export default MainHeaderBar;