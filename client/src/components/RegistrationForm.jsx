import { useUserActions } from "../stores/userStore";
import useField from '../hooks/useField'
import { useChangeActions } from "../stores/loginStore";

const RegistrationForm = () => {
    const { create } = useUserActions();
    const username = useField('text');
    const email = useField('text');
    const password = useField('password');
    const { changeLogin } = useChangeActions();

    const handleRegister = async (e) => {
        e.preventDefault();

        const credentials = {
            username: username.value,
            password: password.value
        };

        await create(credentials);
        e.target.reset();
        changeLogin();
    }

    return (
        <form onSubmit={handleRegister}>
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
            <button type="submit">Rgister</button>
        </form>
    )
}

export default RegistrationForm