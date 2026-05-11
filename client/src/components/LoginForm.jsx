import { useUserActions } from "../stores/userStore";
import useField from '../hooks/useField'
import { useNavigate } from 'react-router-dom'
import { Button } from "./Styled";

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
        navigate("");
    }

    return (
        <form onSubmit={handleLogin}>
            <label>
                username
                <input name="username" {...username} />
            </label>
            <label>
                password
                <input name="password" {...password} />
            </label>
            <Button type="submit">Login</Button>
        </form>
    )
}

export default LoginForm