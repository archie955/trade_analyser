import { create } from "zustand";

const useLoginStore = create((set) => ({
    login: true,
    actions: {
        changeLogin: () => set(state => ({ login: !state.login }))
    }
}))

export const useLogin = () => useLoginStore(state => state.login)

export const useChangeActions = () => useLoginStore(state => state.actions)