<template>
  <div class="home">
    <v-container>
      <v-card>
        <v-text-field
            v-model="form.username"
            :error-messages="errors.login"
            label="Login"
            required
        ></v-text-field>
        <v-text-field
            v-model="form.password"
            :error-messages="errors.password"
            label="E-mail"
            required
        ></v-text-field>
        <v-btn class="mr-4" @click="submit">submit</v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script>
    import axios from 'axios'
    import baseUrl from "../config";
    import {setToken} from "../utils/cookies"
    import router from "../router/index"

    export default {
        name: "Login",
        data: () => ({
            form: {
                username: '',
                password: '',
            },
            errors: {
                login: '',
                password: '',
            },
            url: baseUrl + '/api/login/'
        }),
        methods: {
            submit() {
                console.log(this.form.login);
                console.log(this.form.password);
                axios.post(this.url, this.form)
                    .then(response => {
                        setToken(response.data.key)
                        console.log(response.data.key);
                        router.push('/start-game')
                    })
                    .catch(error => {
                        console.log(error);
                    });
            },
        },
    };
</script>
