<template>
  <div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 text-indigo-800">Upload Survey</h1>
    
    <form @submit.prevent="uploadSurvey" class="space-y-6">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700">Survey Name</label>
        <input
          type="text"
          id="name"
          v-model="surveyName"
          placeholder="Enter survey name"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
        />
      </div>

      <div>
        <label for="csv" class="block text-sm font-medium text-gray-700">CSV File</label>
        <input
          type="file"
          id="csv"
          @change="handleCSVUpload"
          accept=".csv"
          class="mt-1 block w-full"
          required
        />
      </div>

      <div>
        <label for="images" class="block text-sm font-medium text-gray-700">Image Files</label>
        <input
          type="file"
          id="images"
          @change="handleImageUpload"
          accept="image/*"
          multiple
          class="mt-1 block w-full"
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
        :disabled="isUploading"
        class="w-full bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300 disabled:opacity-50"
      >
        {{ isUploading ? 'Uploading...' : 'Upload Survey' }}
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
import { ref } from 'vue'
const config = useRuntimeConfig()

const surveyName = ref('')
const adminPassword = ref('')
const csvFile = ref(null)
const imageFiles = ref([])
const message = ref('')
const alertColor = ref('')
const isUploading = ref(false)

const handleCSVUpload = (event) => {
  csvFile.value = event.target.files[0]
}

const handleImageUpload = (event) => {
  imageFiles.value = Array.from(event.target.files)
}

const uploadSurvey = async () => {
  try {
    if (!surveyName.value || !adminPassword.value || !csvFile.value) {
      throw new Error('Name, password and CSV file are required')
    }

    isUploading.value = true
    const formData = new FormData()
    
    formData.append('name', surveyName.value)
    formData.append('password', adminPassword.value)
    formData.append('csv_file', csvFile.value)
    imageFiles.value.forEach((image) => {
        formData.append('images', image)
    })

    const response = await fetch(`${config.public.backendUrl}/api/upload-survey`, {
      method: 'POST',
      body: formData,
    })
    
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'An error occurred')
    
    message.value = data.message || 'Survey uploaded successfully'
    alertColor.value = 'green'
    
    // Reset form
    surveyName.value = ''
    adminPassword.value = ''
    csvFile.value = null
    imageFiles.value = []
    
  } catch (error) {
    message.value = "Fehler beim Hochladen der Umfrage: " + error.message
    alertColor.value = 'red'
  } finally {
    isUploading.value = false
  }
}
</script>
