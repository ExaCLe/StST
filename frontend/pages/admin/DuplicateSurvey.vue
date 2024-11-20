<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 text-indigo-800">Duplicate Survey</h1>
    
    <form @submit.prevent="duplicateSurvey" class="space-y-6">
      <div>
        <label for="survey" class="block text-sm font-medium text-gray-700">Select Survey to Duplicate</label>
        <select
          id="survey"
          v-model="selectedSurvey"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
        >
          <option value="">Select a survey</option>
          <option v-for="survey in surveys" :key="survey" :value="survey">
            {{ survey }}
          </option>
        </select>
      </div>

      <div>
        <label for="newName" class="block text-sm font-medium text-gray-700">New Survey Name</label>
        <input
          type="text"
          id="newName"
          v-model="newName"
          placeholder="Enter new survey name"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
        />
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Admin Password</label>
        <input
          type="password"
          id="password"
          v-model="adminPassword"
          placeholder="Enter password"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
        />
      </div>

      <button
        type="submit"
        :disabled="isDuplicating"
        class="w-full bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300 disabled:opacity-50"
      >
        {{ isDuplicating ? 'Duplicating...' : 'Duplicate Survey' }}
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
const config = useRuntimeConfig()

const selectedSurvey = ref('')
const newName = ref('')
const adminPassword = ref('')
const message = ref('')
const alertColor = ref('')
const isDuplicating = ref(false)
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

const duplicateSurvey = async () => {
  try {
    isDuplicating.value = true
    const formData = new FormData()
    formData.append('password', adminPassword.value)
    formData.append('new_name', newName.value)

    const response = await fetch(
      `${config.public.backendUrl}/api/duplicate-survey/${selectedSurvey.value}`, 
      {
        method: 'POST',
        body: formData
      }
    )
    
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'An error occurred')
    
    message.value = data.message
    alertColor.value = 'green'
    selectedSurvey.value = ''
    newName.value = ''
    adminPassword.value = ''
    
    // Refresh survey list
    await fetchSurveys()
  } catch (error) {
    message.value = "Error duplicating survey: " + error.message
    alertColor.value = 'red'
  } finally {
    isDuplicating.value = false
  }
}

onMounted(fetchSurveys)
</script> 