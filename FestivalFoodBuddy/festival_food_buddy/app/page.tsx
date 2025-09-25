'use client'
// React Imports
import { useState } from "react";

// Custom Components Imports
import PageFrame from "./Menu_Components/Page_Frame";
import LoginDialoge from "./Login_Page_Components/MainLogin_Dialoge";
import RegistrationDialoge from "./Login_Page_Components/MainRegister_Dialoge";

// Styling Imports
import "primereact/resources/themes/fluent-light/theme.css";
import MainAppView from "./Login_Page_Components/MainApp_View";

export default function Home() {
    const [loginState, setLoginState] = useState('Not Logged In');
    const [loginNumber, setLoginNumber] = useState('');
    const [registrationState, setRegistrationState] = useState(false);

    return (
        <div
            style={{
                height: "100%"
            }}
        >
            <PageFrame>
                <div
                    style={{
                        flex: 1,
                        height: "100%"
                    }}
                >
                    {loginState === 'Not Logged In' ? (
                        registrationState === false ? (
                        <LoginDialoge
                            onLoginStateChange={setLoginState}
                            onRegister={() => setRegistrationState(true)}
                            onLoginNumberChange={setLoginNumber}
                        />
                        ) : (
                        <RegistrationDialoge
                            onLoginStateChange={setLoginState}
                            onLogin={() => setRegistrationState(false)}
                            onLoginNumberChange={setLoginNumber}
                        />
                        )
                    ) : (
                        <div
                            style={{
                                height: "100%"
                            }}
                        >
                            <MainAppView
                                userRole={loginState}
                                loginNumber={loginNumber}
                            />
                        </div>
                        )
                    }
                </div>
            </PageFrame>
        </div>
    );
}
