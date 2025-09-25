import VisitorLandingPage from "../Visitor_Page_Components/Visitor_LandingPage";

interface MainAppViewProps {
    loginNumber: string;
    userRole: string;
}


export default function MainAppView({ userRole, loginNumber }: MainAppViewProps) {

    return (
        <div
            style={{
                height: "100%"
            }}
        >
            {userRole === 'Besucher' ? (
                    <VisitorLandingPage
                        loginNumber={loginNumber}
                    />
                ) : (
                    <></>
                )
            }
        </div>
    );
}