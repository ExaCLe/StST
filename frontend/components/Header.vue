<template>
  <header class="bg-white shadow-md">
    <nav class="container mx-auto px-6 py-3">
      <div class="flex justify-between items-center">
        <NuxtLink to="/" class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-600">
          ST-UMFRAGEN
        </NuxtLink>
        <!-- Menu toggle button for small screens -->
        <button @click="isMenuOpen = !isMenuOpen" class="text-gray-700 md:hidden">
          <UIcon name="i-heroicons-bars-3" class="w-6 h-6" />
        </button>
        <!-- Navigation links for medium and larger screens -->
        <div class="hidden md:flex space-x-4 items-center">
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
                  to="/admin/create-survey" 
                  class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                  <UIcon name="i-heroicons-plus-circle" />
                  <span>Neue Umfrage</span>
                </NuxtLink>
                <NuxtLink 
                  to="/admin/edit-survey" 
                  class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                  <UIcon name="i-heroicons-pencil" />
                  <span>Umfrage Bearbeiten</span>
                </NuxtLink>
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
                <NuxtLink 
                  to="/admin/DeleteSurvey" 
                  class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                  <UIcon name="i-heroicons-trash" />
                  <span>Umfrage Löschen</span>
                </NuxtLink>
                <NuxtLink 
                  to="/admin/ResetSurveyResults" 
                  class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                  <UIcon name="i-heroicons-arrow-path" />
                  <span>Ergebnisse Zurücksetzen</span>
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Mobile navigation menu -->
      <div v-if="isMenuOpen" class="mt-2 md:hidden">
        <div class="flex flex-col space-y-2">
          <NuxtLink to="/" class="text-gray-700 hover:text-indigo-600 transition duration-300">
            Startseite
          </NuxtLink>
          <NuxtLink to="/surveys" class="text-gray-700 hover:text-indigo-600 transition duration-300">
            Umfragen
          </NuxtLink>
          <!-- Admin submenu -->
          <div>
            <button @click="isAdminMenuOpen = !isAdminMenuOpen" class="text-gray-700 hover:text-indigo-600 transition duration-300 flex items-center">
              Admin
              <UIcon name="i-heroicons-chevron-down-20-solid" class="ml-1 w-4 h-4" />
            </button>
            <div v-if="isAdminMenuOpen" class="mt-1 flex flex-col space-y-1">
              <NuxtLink 
                to="/admin/create-survey" 
                class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                <UIcon name="i-heroicons-plus-circle" />
                <span>Neue Umfrage</span>
              </NuxtLink>
              <NuxtLink 
                to="/admin/edit-survey" 
                class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                <UIcon name="i-heroicons-pencil" />
                <span>Umfrage Bearbeiten</span>
              </NuxtLink>
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
              <NuxtLink 
                to="/admin/DeleteSurvey" 
                class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                <UIcon name="i-heroicons-trash" />
                <span>Umfrage Löschen</span>
              </NuxtLink>
              <NuxtLink 
                to="/admin/ResetSurveyResults" 
                class="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-indigo-500 hover:text-white">
                <UIcon name="i-heroicons-arrow-path" />
                <span>Ergebnisse Zurücksetzen</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  const isMenuOpen = ref(false);
  const isAdminMenuOpen = ref(false);
</script>

<style scoped>
/* Remove all previous styles as we're using Tailwind classes */
</style>
