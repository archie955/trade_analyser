import axios from 'axios'

const createAccount = async (credentials) => {
  const response = await axios.post('/api/users', credentials)
  return response.data
}

const login = async (credentials) => {
  const formData = new URLSearchParams()
  formData.append('username', credentials.username)
  formData.append('password', credentials.password)

  const response = await axios.post('/api/users/login',
    formData,
    { headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    } }
  )

  return response.data
}

export default { createAccount, login }