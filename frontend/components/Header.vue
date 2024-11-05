<template>
  <UContainer class="header">
    <div class="logo">
      <NuxtLink to="/" class="logo-link">
        ST-UMFRAGEN
      </NuxtLink>
    </div>
    <div class="nav-links">
      <UButton to="/" variant="link" color="black">Startseite</UButton>
      <UButton to="/surveys" variant="link" color="black">Umfragen</UButton>
      <UDropdown :items="items" :popper="{ placement: 'bottom-start' }" class="admin-dropdown">
        <UButton color="primary" label="Admin" trailing-icon="i-heroicons-chevron-down-20-solid" />
      </UDropdown>
    </div>
  </UContainer>
</template>

<script setup lang="ts">
import { navigateTo } from '#app'

const items = [
  [
    {
      label: 'Ergebnisse Anfordern',
      icon: 'i-heroicons-document-duplicate-20-solid',
      click: () => navigateTo('/admin/RequestResults')
    }
  ],
  [
    {
      label: 'Umfrage Hochladen',
      icon: 'i-heroicons-solid:cloud-upload',
      click: () => navigateTo('/admin/UploadSurvey')
    }
  ]
]
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #ffffff;
  color: #333333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.logo-link {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--theme-color);
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.admin-dropdown .u-dropdown-item {
  background-color: #ffffff !important; /* Light background for dropdown items */
  color: #333333 !important; /* Dark text for readability */
  padding: 0.5rem 1rem;
  border-radius: 5px;
}

.admin-dropdown .u-dropdown-item:hover {
  background-color: var(--theme-color) !important; /* Highlight color on hover */
  color: #ffffff !important; /* White text on hover */
}

.u-button[color="primary"] {
  color: #ffffff !important; /* White text color for primary buttons */
}
</style>
