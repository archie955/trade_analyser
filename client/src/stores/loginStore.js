import { create } from "zustand";

const useLoginStore = create((set) => ({
    login: true,
    changeLogin: set(login => !login)
}))

export const useLogin = () => useLoginStore(state => state.login)

export const useChangeLogin = () => useLoginStore(state => state.changeLogin)