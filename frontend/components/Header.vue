<template>
  <header class="bg-white shadow-md">
    <UContainer>
      <nav class="px-6 py-3">
        <div class="flex justify-between items-center">
          <NuxtLink to="/" class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-600">
            ST-UMFRAGEN
          </NuxtLink>
          <div class="flex items-center space-x-4">
            <UButton
              to="/"
              variant="ghost"
              class="text-gray-700 hover:text-indigo-600 transition duration-300"
            >
              Startseite
            </UButton>
            <UButton
              to="/surveys"
              variant="ghost"
              class="text-gray-700 hover:text-indigo-600 transition duration-300"
            >
              Umfragen
            </UButton>
            <UDropdown
              :items="items"
              :ui="{
                container: 'w-48',
                item: { base: 'flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white transition duration-300' },
                base: 'bg-white rounded-md shadow-lg'
              }"
            >
              <UButton
                color="gray"
                variant="ghost"
                class="text-gray-700 hover:text-indigo-600 transition duration-300"
              >
                Admin
                <template #trailing>
                  <UIcon name="i-heroicons-chevron-down-20-solid" />
                </template>
              </UButton>
            </UDropdown>
          </div>
        </div>
      </nav>
    </UContainer>
  </header>
</template>

<script setup lang="ts">
const items = [
  [
    {
      label: 'Ergebnisse Anfordern',
      icon: 'i-heroicons-document-duplicate-20-solid',
      to: '/admin/RequestResults'
    }
  ],
  [
    {
      label: 'Umfrage Hochladen',
      icon: 'i-heroicons-solid:cloud-upload',
      to: '/admin/UploadSurvey'
    }
  ]
]
</script>

<style scoped>
/* Remove all previous styles as we're using Tailwind classes */
</style>
