<template>
  <UContainer class="text-center py-8">
    <h1 class="text-4xl font-bold mb-8 text-indigo-800">
      Welcome to St-Surveys
    </h1>
    
    <p class="text-xl mb-8 text-gray-700">
      Explore our surveys and contribute to valuable research!
    </p>
    
    <div class="space-y-4 max-w-xs mx-auto">
      <UButton
        to="/surveys"
        color="indigo"
        variant="solid"
        class="w-full rounded-full transition duration-300 hover:opacity-90"
      >
        View Available Surveys
      </UButton>

      <UButton
        to="/admin/UploadSurvey"
        color="purple"
        variant="solid"
        class="w-full rounded-full transition duration-300 hover:opacity-90"
      >
        Upload a Survey (Admin)
      </UButton>

      <UButton
        to="/admin/RequestResults"
        color="green"
        variant="solid"
        class="w-full rounded-full transition duration-300 hover:opacity-90"
      >
        Request Results (Admin)
      </UButton>
    </div>
  </UContainer>
</template>

<script setup>
// No additional setup required for this static page
</script>
