<template>
  <v-app>
    <v-content>
      <v-btn v-if="!auth" @click="login">Zaloguj</v-btn>
      <v-btn v-else @click="logout">Wyloguj</v-btn>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
    import {checkToken, deleteToken} from "./utils/cookies"
    import axiosSession from "./utils/axiosSession"
    import baseUrl from "./config";

    export default {
        name: "App",

        data: () => ({
            auth: false
        }),
        mounted() {
            this.auth = checkToken()
            if (!this.auth) {
                this.$router.push('/')
            }
        },
        methods: {
            login() {
                window.location.href = '/#/';
            },
            logout() {
                axiosSession.post(baseUrl + '/api/logout/').then(() => {
                  deleteToken();
                  location.reload()
                }).catch(error => {
                  console.error(error);
                })
            }
        }
    };
</script>
