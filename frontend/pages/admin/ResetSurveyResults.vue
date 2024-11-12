<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 text-indigo-800">Ergebnisse Zurücksetzen</h1>
    
    <form @submit.prevent="resetResults" class="space-y-6">
      <div>
        <label for="survey" class="block text-sm font-medium text-gray-700">Umfrage auswählen</label>
        <select
          id="survey"
          v-model="selectedSurvey"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indogo-200 focus:ring-opacity-50"
          required
        >
          <option value="">Bitte wählen Sie eine Umfrage</option>
          <option v-for="survey in surveys" :key="survey" :value="survey">
            {{ survey }}
          </option>
        </select>
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Admin Passwort</label>
        <input
          type="password"
          id="password"
          v-model="adminPassword"
          placeholder="Passwort eingeben"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
        />
      </div>

      <button
        type="submit"
        :disabled="isResetting"
        class="w-full bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300 disabled:opacity-50"
      >
        {{ isResetting ? 'Zurücksetzen...' : 'Ergebnisse Zurücksetzen' }}
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
const isResetting = ref(false)
const surveys = ref([])

const fetchSurveys = async () => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/surveys`)
    const data = await response.json()
    surveys.value = data.surveys
  } catch (error) {
    message.value = "Fehler beim Abrufen der Umfragen: " + error.message
    alertColor.value = 'red'
  }
}

const resetResults = async () => {
  if (!confirm(`Sind Sie sicher, dass Sie die Ergebnisse der Umfrage "${selectedSurvey.value}" zurücksetzen möchten? Diese Aktion kann nicht rückgängig gemacht werden.`)) {
    return
  }

  try {
    isResetting.value = true
    const response = await fetch(`${config.public.backendUrl}/api/reset-survey-results/${selectedSurvey.value}?password=${encodeURIComponent(adminPassword.value)}`, {
      method: 'DELETE'
    })
    
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'Ein Fehler ist aufgetreten')
    
    message.value = data.message
    alertColor.value = 'green'
    selectedSurvey.value = ''
    adminPassword.value = ''
    
    // Optionally refresh survey list
    // await fetchSurveys()
  } catch (error) {
    message.value = "Fehler beim Zurücksetzen der Ergebnisse: " + error.message
    alertColor.value = 'red'
  } finally {
    isResetting.value = false
  }
}

onMounted(fetchSurveys)
</script>
