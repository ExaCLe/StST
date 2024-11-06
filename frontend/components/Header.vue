<template>
  <header class="bg-white shadow-md">
    <nav class="container mx-auto px-6 py-3">
      <div class="flex justify-between items-center">
        <NuxtLink to="/" class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-600">
          ST-UMFRAGEN
        </NuxtLink>
        <div class="flex space-x-4 items-center">
          <NuxtLink to="/" class="text-gray-700 hover:text-indigo-600 transition duration-300">
            Startseite
          </NuxtLink>
          <NuxtLink to="/surveys" class="text-gray-700 hover:text-indigo-600 transition duration-300">
            Umfragen
          </NuxtLink>
          <div class="relative group">
            <button class="text-gray-700 hover:text-indigo-600 transition duration-300 flex items-center">
              Admin
              <UIcon name="i-heroicons-chevron-down-20-solid" class="ml-1 w-4 h-4" />
            </button>
            <div class="absolute right-0 mt-1 w-48 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50 transform">
              <div class="py-1">
                <NuxtLink 
                  to="/admin/RequestResults" 
                  class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                  <UIcon name="i-heroicons-document-duplicate-20-solid" />
                  <span>Ergebnisse Anfordern</span>
                </NuxtLink>
                <NuxtLink 
                  to="/admin/UploadSurvey" 
                  class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                  <UIcon name="i-heroicons-solid:cloud-upload" />
                  <span>Umfrage Hochladen</span>
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
// No additional setup needed
</script>

<style scoped>
/* Remove all previous styles as we're using Tailwind classes */
</style>
