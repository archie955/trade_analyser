import { useUserActions } from '../stores/userStore'
import useField from '../hooks/useField'
import { useChangeActions } from '../stores/loginStore'
import { useState } from 'react'
import { Button, FormControl, Input, InputLabel, Card } from '@mui/material'

const RegistrationForm = () => {
  const [loading, setLoading] = useState(false)
  const { create } = useUserActions()
  const username = useField('text')
  const email = useField('text')
  const password = useField('password')
  const { changeLogin } = useChangeActions()

  const handleRegister = async (e) => {
    e.preventDefault()
    setLoading(true)

    const credentials = {
      email: email.value,
      username: username.value,
      password: password.value
    }

    await create(credentials)
    e.target.reset()
    setLoading(false)
    changeLogin()
  }

  return (
    <Card>
      <form onSubmit={handleRegister}>
        <FormControl>
          <InputLabel htmlFor="email">Email</InputLabel>
          <Input id="email" {...email} />
        </FormControl>
        <FormControl>
          <InputLabel htmlFor="username">Username</InputLabel>
          <Input id="username" {...username} />
        </FormControl>
        <FormControl>
          <InputLabel htmlFor="password">Password</InputLabel>
          <Input id="password" {...password} />
        </FormControl>
        <Button variant="contained" type="submit" loading={loading} loadingPosition="end" size="medium">REGISTER</Button>
      </form>
    </Card>
  )
}

export default RegistrationForm