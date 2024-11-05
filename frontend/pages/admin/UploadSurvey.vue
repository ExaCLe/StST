<template>
  <UContainer>
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-indigo-800">Upload Survey</h1>
      
      <form @submit.prevent="uploadSurvey" class="space-y-6">
        <UFormGroup label="Survey Name" class="block">
          <UInput
            v-model="name"
            placeholder="Enter survey name"
            required
          />
        </UFormGroup>

        <UFormGroup label="CSV File" class="block">
          <UInput
            type="file"
            @change="handleCSVUpload"
            accept=".csv"
            required
          />
        </UFormGroup>

        <UFormGroup label="Image Files" class="block">
          <UInput
            type="file"
            @change="handleImageUpload"
            accept="image/*"
            multiple
          />
        </UFormGroup>

        <UFormGroup label="Admin Password" class="block">
          <UInput
            v-model="password"
            type="password"
            placeholder="Enter password"
            required
          />
        </UFormGroup>

        <UButton
          type="submit"
          color="primary"
          variant="solid"
          class="w-full rounded-full"
          :loading="isUploading"
        >
          Upload Survey
        </UButton>
      </form>

      <UAlert
        v-if="message"
        :color="alertColor"
        class="mt-6"
      >
        {{ message }}
      </UAlert>
    </div>
  </UContainer>
</template>

<script setup>
import { ref } from 'vue'
const config = useRuntimeConfig()

const name = ref('')
const password = ref('')
const csvFile = ref(null)
const images = ref([])
const message = ref('')
const alertColor = ref('')
const isUploading = ref(false)

const handleCSVUpload = (files) => {
  csvFile.value = files[0]
}

const handleImageUpload = (files) => {
  images.value = Array.from(files);
};

const uploadSurvey = async () => {
  try {
    // Validate required fields
    if (!name.value || !password.value || !csvFile.value) {
      throw new Error('Name, password and CSV file are required')
    }

    isUploading.value = true
    const formData = new FormData()
    
    // Add required fields
    formData.append('name', name.value)
    formData.append('password', password.value)
    formData.append('csv_file', csvFile.value)
    images.value.forEach((image) => {
        formData.append('images', image);
    });

    const response = await fetch(`${config.public.backendUrl}/api/upload-survey`, {
      method: 'POST',
      body: formData,
    })
    
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'An error occurred')
    
    message.value = data.message || 'Survey uploaded successfully'
    alertColor.value = 'green'
    
    // Reset form after success
    name.value = ''
    password.value = ''
    csvFile.value = null
    images.value = []
    
  } catch (error) {
    message.value = error.message || 'An error occurred'
    alertColor.value = 'red'
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
.upload-survey {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.upload-card {
  width: 100%;
  max-width: 600px;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.upload-card h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #4a90e2;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: bold;
}

.light-input {
  background-color: #ffffff !important;
  color: #333 !important;
  border: 1px solid #ccc !important;
  border-radius: 5px;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.response-alert {
  margin-top: 1.5rem;
  font-size: 1rem;
  padding: 1rem;
  border-radius: 5px;
  color: #ffffff;
  background-color: var(--alert-background-color);
}

.response-alert[alert-color="success"] {
  background-color: #4caf50; /* Solid green for success */
}

.response-alert[alert-color="error"] {
  background-color: #f44336; /* Solid red for failure */
}
</style>
