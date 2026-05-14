import { useUserActions } from "../stores/userStore";
import useField from '../hooks/useField'
import { useNavigate } from 'react-router-dom'
import Styled from "./Styled";

const LoginForm = () => {
    const { login } = useUserActions();
    const navigate = useNavigate();
    const username = useField('text');
    const password = useField('password');

    const handleLogin = async (e) => {
        e.preventDefault();

        const credentials = {
            username: username.value,
            password: password.value
        };

        await login(credentials);
        e.target.reset();
        navigate("/home");
    }

    return (
        <form onSubmit={handleLogin}>
            <Styled.FormDiv>
                <Styled.Label>
                    username
                    <input name="username" {...username} />
                </Styled.Label>
                <Styled.Label>
                    password
                    <input name="password" {...password} />
                </Styled.Label>
                <Styled.Button type="submit">Login</Styled.Button>
            </Styled.FormDiv>
        </form>
    )
}

export default LoginForm