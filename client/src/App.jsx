import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import { Navigation } from "./components/Styled";

const App = () => {
    return (
        <div>
            <Navigation>
                Nothing for now
            </Navigation>
            <Routes>
                <Route path="/home" element={<Home />} />
                <Route path="" element={<Login />} />
                <Route path="/*" element={<Home />} />
            </Routes>
        </div>
    )
}

export default App