import { create } from 'zustand';
import loginService from '../services/login';
import persistentUserService from '../services/persistentUser';

const useUserStore = create((set) => ({
    username: null,
    token: '',
    actions: {

        create: async (credentials) => {
            try {
                await loginService.createAccount(credentials);
            } catch (error) {
                console.error("creation failed", error);
            }
        },

        login: async (credentials) => {
            try {
                const response = await loginService.login(credentials);
                const user = { username: credentials.username, token: response.access_token };
                persistentUserService.saveUser(user);
                set(() => ({
                    username: user.username, token: user.token
                }));
            } catch (error) {
                console.error("login failed", error)
            }
        },

        logout: () => {
            persistentUserService.removeUser();
            set(() => ({ username: null, token: '' }));
        },

        init: () => {
            const user = persistentUserService.getUser();
            if (user) {
                set(() => user);
            }
        }
    }
}))

export default useUserStore

export const useUser = () => useUserStore(state => state.username)

export const useToken = () => useUserStore(state => state.token)

export const useUserActions = () => useUserStore(state => state.actions)