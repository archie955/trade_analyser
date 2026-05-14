import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import { CssBaseline } from "@mui/material";
import ProtectedRoute from "./components/ProtectedRoute";
import Leagues from "./pages/Leagues";
import { useEffect } from "react";
import { useUserActions } from "./stores/userStore";

const App = () => {
    const { init } = useUserActions()

    useEffect(() => {
        init()
    }, [])
    
    return (
        <div>
            <CssBaseline />
            <Routes>
                <Route path="/home" element={
                    <ProtectedRoute>
                        <Home />
                    </ProtectedRoute>} />
                <Route path="" element={<Login />} />
                <Route path="/leagues" element={
                    <ProtectedRoute>
                        <Leagues />
                    </ProtectedRoute>
                } />
            </Routes>
        </div>
    )
}

export default App