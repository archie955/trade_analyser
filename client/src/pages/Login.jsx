import { useLogin, useChangeActions } from "../stores/loginStore";
import RegistrationForm from "../components/RegistrationForm";
import LoginForm from "../components/LoginForm";
import Styled from "../components/Styled";
import axios from "axios";

const Login = () => {
    const login = useLogin();
    const { changeLogin } = useChangeActions();

    const handleTest = async () => {
        const response = await axios.get("/api/health")
        console.log(response.data)
    }

    return (
        <div>
            {(login && <LoginForm />) || (!login && <RegistrationForm />)}
            <Styled.Button type="button" onClick={() => changeLogin()}>{login ? "Register an account?" : "Already have an account?"}</Styled.Button>
            <Styled.Button type="button" onClick={() => handleTest()}>Test</Styled.Button>
        </div>
    )
}

export default Login