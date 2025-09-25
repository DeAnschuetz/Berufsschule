'use client'
// React Imports
import { useState } from 'react';

// Prime React Imports
import { ScrollPanel } from 'primereact/scrollpanel';

// Custom Compontents Imports
import MainHeaderBar from '../Menu_Components/MainHeader/MainHeader_MenuBar';
import PaymentDialoge from '../Page_Components/Payment_Dialoge';
import OrdersDialog from '../Page_Components/OderOverview_Page';
import StandOverview from '../Page_Components/FoodPlaceOverview_Page';
import WarenkorbDialog from '../Page_Components/ShoppingBasked_Dialoge';

interface VisitorLandingPageProps {
    loginNumber: string;
}

function VisitorLandingPage({ loginNumber }: VisitorLandingPageProps) {
    const [activePage, setActivePage] = useState('MainPage');
    const [creditBalance, setCreditBalance] = useState(20);

    const addCredits = (creditBalanceToAdd: number) => {
        console.log('Balance to Add:', creditBalanceToAdd);

        setCreditBalance((prevBalance) => {
            const newBalance = prevBalance + creditBalanceToAdd;
            console.log('Old Balance:', prevBalance);
            console.log('New Balance:', newBalance);
            return newBalance;
        });
        
        setActivePage('MainPage');
    };

    return (
        <div
            style={{
                height: "100%"
            }}
        >
            <MainHeaderBar
                loginNumber={loginNumber}
                creditBalance={creditBalance}
                notificationCount={0}
                shoppingCartCount={0}
                onMenuItemPressed={setActivePage}
            />
            {
                activePage === 'Payment' ? (
                    <PaymentDialoge
                        changeActivePage={setActivePage}
                        addCredits={addCredits}
                    />
                ) : (
                    <></>
                )
            }
            {
                activePage === 'ShoppingCart' ? (
                    <WarenkorbDialog
                        changeActivePage={setActivePage}
                        addCredits={addCredits}
                    />
                ) : (
                    <></>
                )
            }
            {
                activePage === `MainPage` ? (
                    <ScrollPanel style={{ width: '100%', height: '672px' }}>
                        <OrdersDialog />
                        <StandOverview />
                    </ScrollPanel>
                ) : (
                    <></>
                )
            }
        </div>
    );
}

export default VisitorLandingPage;