<template>
  <div class="layout">
    <Header />
    <NuxtPage />
    <UNotifications />
  </div>
</template>

<script setup>
import Header from '~/components/Header.vue'
</script>

<style scoped>
.layout {
  background-color: #f9f9f9; /* Set a light background for the layout */
  min-height: 100vh; /* Ensures it covers the full screen height */
  padding: 1rem;
}
</style>
