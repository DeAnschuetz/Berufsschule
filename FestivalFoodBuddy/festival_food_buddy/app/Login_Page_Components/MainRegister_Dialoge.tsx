'use client'
// React Imports
import React, { useRef, useState } from 'react';

// Prime React Imports
import { Toast } from 'primereact/toast';
import LoginHeader from './Sub_Components/LoginHeader_Label';
import StayLoggedInCheckbox from './Sub_Components/StayLoggedIn_Checkbox';
import PasswordInput from './Sub_Components/Password_Input';
import LoginNumberInput from './Sub_Components/LoginNumber_Input';
import ButtonRow from './Sub_Components/LoginDialoge_Buttons';
import DialogContainer from './Sub_Components/LoginDialoge_ContainerBox';

function checkRegistration(userName: string) {
    if(userName.includes("A")) {
        return "Admin";
    } else if (userName.includes("V")) {
        return "Verkäufer";
    } else if (userName.includes("B")) {
        return "Besucher";
    } else {
        return "Error";
    }
}

function handleRegistration(
    loginNumber: string,
    password: string,
    passwordConfirm: string,
    onLoginStateChange: (state: string) => void,
    onLoginNumberChange: (loginNumber: string) => void,
    toast: any, setPassword: any,
    setPasswordConfirm: any,
    setUserName: any
) {
    const userType: string = checkRegistration(loginNumber);
    console.log("UserType based on LoginNr:", userType);
    if(userType === "Error") {
        setPassword('');
        setPasswordConfirm('');
        setUserName('');
        showErrorMessage(toast, 'Die eingegebene Login-Nr. ist falsch');
    } else if (onLoginStateChange) {
        onLoginNumberChange(loginNumber);
        onLoginStateChange(userType);
    }
}

function showErrorMessage(toast: any, message: string) {
    toast.current.show({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
}

interface RegistrationDialogeProps {
    onLoginStateChange?: (state: string) => void;
    onLogin?: () => void;
    onLoginNumberChange: (loginNumber: string) => void;
}

export function RegistrationDialoge({ onLoginStateChange, onLogin, onLoginNumberChange }: RegistrationDialogeProps) {
    const [userName, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [stayLoggedIn, setStayLoggedIn] = useState(false);
    const toast = useRef(null);

    return (
        <div
            style={{
                height: "100%",
                paddingTop: "30%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                
            }}
        >
            <LoginHeader />
            <DialogContainer >
                <div
                    style={{
                        width: "100%",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                    }}
                >
                    <LoginNumberInput
                        value={userName}
                        onChange={setUserName}
                    />
                    <PasswordInput 
                        value={password} 
                        onChange={setPassword} 
                        label="Passwort" 
                    />
                    <PasswordInput 
                        value={passwordConfirm} 
                        onChange={setPasswordConfirm} 
                        label="Passwort bestätigen" 
                    />
                    <StayLoggedInCheckbox 
                        checked={stayLoggedIn} 
                        onChange={setStayLoggedIn} 
                    />
                </div>
                <ButtonRow
                    buttons={[
                        {
                            label: "Login",
                            onClick: () => onLogin?.()
                        },
                        {
                            onClick: () =>
                                handleRegistration(
                                    userName,
                                    password,
                                    passwordConfirm,
                                    onLoginStateChange!,
                                    onLoginNumberChange!,
                                    toast,
                                    setPassword,
                                    setPasswordConfirm,
                                    setUserName
                                ),
                            label: "Registrieren",
                            disabled: (password != passwordConfirm || password === '' || passwordConfirm === '')
                        }
                    ]}
                />
            </DialogContainer>
            <Toast
                ref={toast}
                position="top-center"
            />
        </div>
    );
}

export default RegistrationDialoge;
