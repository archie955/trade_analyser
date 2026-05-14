import { useUserActions } from "../stores/userStore";
import { useState } from "react";
import useField from '../hooks/useField'
import { useNavigate } from 'react-router-dom'
import { Button, FormControl, Input, InputLabel, Card } from '@mui/material'

const LoginForm = () => {
    const [loading, setLoading] = useState(false)
    const { login } = useUserActions();
    const navigate = useNavigate();
    const username = useField('text');
    const password = useField('password');

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true)

        const credentials = {
            username: username.value,
            password: password.value
        };

        await login(credentials);
        e.target.reset();
        setLoading(false)
        navigate("/home");
    }

    return (
        <Card>
            <form onSubmit={handleLogin}>
                <FormControl>
                    <InputLabel htmlFor="username">Username or Email</InputLabel>
                    <Input id="username" {...username} />
                </FormControl>
                <FormControl>
                    <InputLabel htmlFor="password">Password</InputLabel>
                    <Input id="password" {...password} />
                </FormControl>
                <Button variant="contained" type="submit" loading={loading} loadingPosition="end" size="medium">LOGIN</Button>
            </form>
        </Card>
    )
}

export default LoginForm