import { useUserActions } from "../stores/userStore";
import useField from '../hooks/useField'
import { useChangeActions } from "../stores/loginStore";
import Styled from "./Styled";

const RegistrationForm = () => {
    const { create } = useUserActions();
    const username = useField('text');
    const email = useField('text');
    const password = useField('password');
    const { changeLogin } = useChangeActions();

    const handleRegister = async (e) => {
        e.preventDefault();

        const credentials = {
            email: email.value,
            username: username.value,
            password: password.value
        };

        await create(credentials);
        e.target.reset();
        changeLogin();
    }

    return (
        <form onSubmit={handleRegister}>
            <Styled.FormDiv>
                <label>
                    email
                    <input name="email" {...email} />
                </label>
                <label>
                    username
                    <input name="username" {...username} />
                </label>
                <label>
                    password
                    <input name="password" {...password} />
                </label>
                <Styled.Button type="submit">Register</Styled.Button>
            </Styled.FormDiv>
        </form>
    )
}

export default RegistrationForm