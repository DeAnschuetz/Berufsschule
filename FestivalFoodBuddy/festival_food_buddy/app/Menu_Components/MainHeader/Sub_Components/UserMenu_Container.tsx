// Icon Imports
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser, faBars } from '@fortawesome/free-solid-svg-icons'

interface UserMenuContainerProps {
    loginNumber: string;
    onMenuItemPressed: (item: string) => void;
}

function UserMenuContainer({ loginNumber, onMenuItemPressed }: UserMenuContainerProps) {
    return (
        <div style={{ display: "flex", alignItems: "center" }}>
            <FontAwesomeIcon
                icon={faBars}
                onClick={() => onMenuItemPressed('Menu')}
                style={{ color: "black", width: "35px", height: "35px"}}
            />
            <FontAwesomeIcon
                icon={faUser}
                onClick={() => onMenuItemPressed('User')}
                style={{ color: "black", width: "30px", height: "30px"}}
            />
            <span style={{ fontSize: "140%", color: "black" }}>{loginNumber}</span>
        </div>
    );
}

export default UserMenuContainer;