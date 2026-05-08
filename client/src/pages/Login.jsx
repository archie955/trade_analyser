import { useLogin, useChangeActions } from "../stores/loginStore";
import RegistrationForm from "../components/RegistrationForm";
import LoginForm from "../components/LoginForm";

const Login = () => {
    const login = useLogin();
    const { changeLogin } = useChangeActions();
    console.log(login)

    return (
        <div>
            {(login && <LoginForm />) || (!login && <RegistrationForm />)}
            <button type="button" onClick={() => changeLogin()}>{login ? "Register an account?" : "Already have an account?"}</button>
        </div>
    )
}

export default Login