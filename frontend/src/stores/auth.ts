import { defineStore } from "pinia";
import { login, getMe } from "../api/auth";
import type { User } from "../types/api";

export const useAuthStore = defineStore('auth', {
  state: ()=>({
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    user: null as User | null, 
  }),

  getters: {
    isLoggedIn: (state) => Boolean(state.accessToken),
  },

  actions: {
    async login(username: string, password: string)
    {
      const response = await login({username, password})
      this.accessToken = response.data.access
      this.refreshToken = response.data.refresh
      
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)

      await this.loadMe()
    },

    async loadMe()
    {
      const response = await getMe()
      this.user = response.data
    },

    logout()
    {
      this.accessToken = ''
      this.refreshToken = ''
      this.user = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})