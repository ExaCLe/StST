<template>
  <NuxtLayout />
</template>

<script setup>
// No additional script setup needed
</script>

<style scoped>
:root {
  --theme-color: #4a90e2; /* Adjust to your primary color */
}

body {
  background-color: #f9f9f9; /* Light background for the whole app */
  color: #333; /* Standard dark text color */
}

* {
  color-scheme: light; /* Enforces a light color scheme */
}

/* Ensures the layout background is light as well */
#app {
  background-color: #f9f9f9;
}
</style>
