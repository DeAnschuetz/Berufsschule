'use client'
// React Imports
import React, { useRef, useState } from 'react';

// Prime React Imports
import { Toast } from 'primereact/toast';
import LoginHeader from './Sub_Components/LoginHeader_Label';
import StayLoggedInCheckbox from './Sub_Components/StayLoggedIn_Checkbox';
import LoginNumberInput from './Sub_Components/LoginNumber_Input';
import PasswordInput from './Sub_Components/Password_Input';
import ButtonRow from './Sub_Components/LoginDialoge_Buttons';
import DialogContainer from './Sub_Components/LoginDialoge_ContainerBox';

function checkLogin(userName: string) {
  if(userName.toLowerCase().includes("a")) {
    return "Admin";
  } else if (userName.toLowerCase().includes("v")) {
    return "Verkäufer";
  } else if (userName.toLowerCase().includes("b")) {
    return "Besucher";
  } else {
    return "Error";
  }
}

function handleLogin(
    loginNumber: string,
    password: string,
    onLoginStateChange: (state: string) => void,
    onLoginNumberChange: (loginNumber: string) => void,
    toast: any, setPassword: any,
    setUserName: any
) {
  const userType: string = checkLogin(loginNumber);
  console.log("UserType based on LoginNr:", userType);
  if(userType === "Error") {
    setPassword('');
    setUserName('');
    showErrorMessage(toast, 'Die eingegebene Login-Nr. ist falsch.');
  } else if (onLoginStateChange) {
    onLoginNumberChange(loginNumber);
    onLoginStateChange(userType);
  }
}

function showErrorMessage(toast: any, message: string) {
  toast.current.show({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
}

interface LoginDialogeProps {
  onLoginStateChange?: (state: string) => void;
  onRegister?: () => void;
  onLoginNumberChange?: (loginNumber: string) => void;
}

export function LoginDialoge({ onLoginStateChange, onRegister, onLoginNumberChange }: LoginDialogeProps) {
    const [userName, setUserName] = useState('');
    const [password, setPassword] = useState('');
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
        <DialogContainer>
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
                    label={"Passwort"}
                    onChange={setPassword}
                />
                <StayLoggedInCheckbox 
                    checked={stayLoggedIn} 
                    onChange={setStayLoggedIn} 
                />
            </div>
            <ButtonRow
                buttons={[
                    {
                        label: "Registrieren",
                        onClick: () => onRegister?.()
                    },
                    {
                    label: "Login",
                    onClick: () =>
                        handleLogin(
                        userName,
                        password,
                        onLoginStateChange!,
                        onLoginNumberChange!,
                        toast,
                        setPassword,
                        setUserName
                        ),
                    disabled: password === ""
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

export default LoginDialoge;
