import { defineStore } from 'pinia'
export const userInformation = defineStore('user', {
    state: () => ({
      username:'',
      userhead:'',
      is_login:false
    })})