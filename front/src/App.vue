<template>
  <v-app>
    <v-content>
        <router-link to="/">Go to Home</router-link>
        <router-link to="/about">Go to about</router-link>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: "App",

  data: () => ({
    //
  })
};
</script>
