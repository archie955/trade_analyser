import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Styled from "./components/Styled";

const App = () => {
    return (
        <div>
            <Styled.Navigation>
                Nothing for now
            </Styled.Navigation>
            <Routes>
                <Route path="/home" element={<Home />} />
                <Route path="" element={<Login />} />
                <Route path="/*" element={<Home />} />
            </Routes>
        </div>
    )
}

export default App