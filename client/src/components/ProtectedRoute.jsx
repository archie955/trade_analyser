import { useToken } from "../stores/userStore";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
    const token = useToken()
    console.log(token)
    if (!token) return <Navigate to="/" />
    return children
}

export default ProtectedRoute