<template>
  <div class="home">
    <!--    <HelloWorld msg="Welcome to Your Vue.js App" />-->
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
  </div>
</template>

<script>
    // @ is an alias to /src
    // import HelloWorld from "@/components/HelloWorld.vue";
    import axios from 'axios'
    import baseUrl from "../config";

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
                console.log(this.form.login)
                console.log(this.form.password)
                axios.post(this.url, this.form)
                    .then(response => {
                      console.log(response);
                    })
                    .catch(error => {
                      console.log(error);
                    })
            },
        },
        // components: {
        //   HelloWorld
        // }
    };
</script>
