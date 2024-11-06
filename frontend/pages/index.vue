<template>
  <div class="text-center py-8">
    <h1 class="text-4xl font-bold mb-8 text-indigo-800">
      Welcome to St-Surveys
    </h1>
    
    <p class="text-xl mb-8 text-gray-700">
      Explore our surveys and contribute to valuable research!
    </p>
    
    <div class="space-y-4">
      <NuxtLink
        to="/surveys"
        class="block w-64 mx-auto bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300"
      >
        View Available Surveys
      </NuxtLink>

      <NuxtLink
        to="/admin/UploadSurvey"
        class="block w-64 mx-auto bg-purple-600 text-white py-2 px-4 rounded-full hover:bg-purple-700 transition duration-300"
      >
        Upload a Survey (Admin)
      </NuxtLink>

      <NuxtLink
        to="/admin/RequestResults"
        class="block w-64 mx-auto bg-green-600 text-white py-2 px-4 rounded-full hover:bg-green-700 transition duration-300"
      >
        Request Results (Admin)
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
// No additional setup required for this static page
</script>
