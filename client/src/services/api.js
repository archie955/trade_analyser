import axios from "axios";
import { useToken } from '../stores/userStore'

const api = axios.create({
    baseUrl: "/api",
    withCredentials: true
})

api.interceptors.request.use((config) => {
    const token = useToken()
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export default api