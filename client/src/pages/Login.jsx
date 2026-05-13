import { useLogin, useChangeActions } from "../stores/loginStore";
import RegistrationForm from "../components/RegistrationForm";
import LoginForm from "../components/LoginForm";
import { Button } from "../components/Styled";
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
            <Button type="button" onClick={() => changeLogin()}>{login ? "Register an account?" : "Already have an account?"}</Button>
            <Button type="button" onClick={() => handleTest()}>Test</Button>
        </div>
    )
}

export default Login