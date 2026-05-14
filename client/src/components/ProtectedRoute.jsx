import { useToken } from "../stores/userStore";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
    const token = useToken()
    if (!token) return <Navigate to="/" />
    return children
}

export default ProtectedRoute