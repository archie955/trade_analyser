import { useLogin, useChangeActions } from "../stores/loginStore";
import RegistrationForm from "../components/RegistrationForm";
import LoginForm from "../components/LoginForm";
import { Button } from "../components/Styled";

const Login = () => {
    const login = useLogin();
    const { changeLogin } = useChangeActions();
    console.log(login)

    return (
        <div>
            {(login && <LoginForm />) || (!login && <RegistrationForm />)}
            <Button type="button" onClick={() => changeLogin()}>{login ? "Register an account?" : "Already have an account?"}</Button>
        </div>
    )
}

export default Login