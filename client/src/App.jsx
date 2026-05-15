import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import { CssBaseline } from "@mui/material";
import ProtectedRoute from "./components/ProtectedRoute";
import Leagues from "./pages/Leagues";
import League from "./pages/League";
import { useEffect } from "react";
import { useUserActions } from "./stores/userStore";
import Team from "./pages/Team";

const App = () => {
  const { init } = useUserActions();

  useEffect(() => {
    init();
  }, [init]);

  return (
    <div>
      <CssBaseline />
      <Routes>
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="" element={<Login />} />
        <Route
          path="/leagues"
          element={
            <ProtectedRoute>
              <Leagues />
            </ProtectedRoute>
          }
        />
        <Route
          path="/leagues/:id"
          element={
            <ProtectedRoute>
              <League />
            </ProtectedRoute>
          }
        />
        <Route
          path="/leagues/:league_id/:id"
          element={
            <ProtectedRoute>
              <Team />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
};

export default App;
