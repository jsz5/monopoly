<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script>

    export default {
        data: () => ({
            reloaded: false
        }),
        mounted() {
            if (localStorage.getItem('reloaded')) {
                // The page was just reloaded. Clear the value from local storage
                // so that it will reload the next time this page is visited.
                localStorage.removeItem('reloaded');
            } else {
                // Set a flag so that we know not to reload the page twice.
                localStorage.setItem('reloaded', '1');
                location.reload();
            }
        },
        methods: {},
    };
</script>