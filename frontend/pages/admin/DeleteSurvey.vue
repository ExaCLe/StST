<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 text-red-800">Delete Survey</h1>
    
    <form @submit.prevent="deleteSurvey" class="space-y-6">
      <div>
        <label for="survey" class="block text-sm font-medium text-gray-700">Select Survey</label>
        <select
          id="survey"
          v-model="selectedSurvey"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-300 focus:ring focus:ring-red-200 focus:ring-opacity-50"
          required
        >
          <option value="">Select a survey</option>
          <option v-for="survey in surveys" :key="survey" :value="survey">
            {{ survey }}
          </option>
        </select>
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Admin Password</label>
        <input
          type="password"
          id="password"
          v-model="adminPassword"
          placeholder="Enter password"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-red-300 focus:ring focus:ring-red-200 focus:ring-opacity-50"
          required
        />
      </div>

      <button
        type="submit"
        :disabled="isDeleting"
        class="w-full bg-red-600 text-white py-2 px-4 rounded-full hover:bg-red-700 transition duration-300 disabled:opacity-50"
      >
        {{ isDeleting ? 'Deleting...' : 'Delete Survey' }}
      </button>
    </form>

    <div 
      v-if="message" 
      :class="`mt-6 p-4 rounded-md ${alertColor === 'red' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`"
    >
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const config = useRuntimeConfig()

const selectedSurvey = ref('')
const adminPassword = ref('')
const message = ref('')
const alertColor = ref('')
const isDeleting = ref(false)
const surveys = ref([])

const fetchSurveys = async () => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/surveys`)
    const data = await response.json()
    surveys.value = data.surveys
  } catch (error) {
    message.value = "Error fetching surveys: " + error.message
    alertColor.value = 'red'
  }
}

const deleteSurvey = async () => {
  if (!confirm(`Are you sure you want to delete the survey "${selectedSurvey.value}"? This action cannot be undone.`)) {
    return
  }

  try {
    isDeleting.value = true
    const response = await fetch(`${config.public.backendUrl}/api/delete-survey/${selectedSurvey.value}?password=${encodeURIComponent(adminPassword.value)}`, {
      method: 'DELETE'
    })
    
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'An error occurred')
    
    message.value = data.message
    alertColor.value = 'green'
    selectedSurvey.value = ''
    adminPassword.value = ''
    
    // Refresh survey list
    await fetchSurveys()
  } catch (error) {
    message.value = "Error deleting survey: " + error.message
    alertColor.value = 'red'
  } finally {
    isDeleting.value = false
  }
}

onMounted(fetchSurveys)
</script>
