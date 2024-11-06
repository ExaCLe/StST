<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <!-- Changed from max-w-2xl -->
    <h1 class="text-3xl font-bold mb-8 text-indigo-800">Request Survey Results</h1>
    <form @submit.prevent="requestResults" class="space-y-6">
      <div>
        <label for="survey" class="block text-sm font-medium text-gray-700">Survey Name</label>
        <select
          id="survey"
          v-model="selectedSurvey"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          :disabled="loadingSurveys"
        >
          <option value="" disabled>Select a survey</option>
          <option v-for="survey in surveys" :key="survey" :value="survey">
            {{ survey }}
          </option>
        </select>
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Admin Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
      </div>
      <button
        type="submit"
        class="w-full bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300 disabled:opacity-50"
        :disabled="isLoading"
      >
        <span v-if="isLoading">Loading...</span>
        <span v-else>Request Results</span>
      </button>
    </form>
    <div v-if="message" :class="`mt-4 p-4 rounded-md ${messageType === 'error' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`">
      {{ message }}
    </div>
    <div v-if="results" class="mt-8 space-y-4">
      <div class="flex space-x-4 flex-wrap gap-y-2">
        <button
          @click="downloadZip"
          v-if="results.has_images"
          class="bg-green-600 text-white py-2 px-4 rounded-full hover:bg-green-700 transition duration-300"
        >
          Download Results (ZIP)
        </button>
        <button
          @click="showTextResults = !showTextResults"
          class="bg-blue-600 text-white py-2 px-4 rounded-full hover:bg-blue-700 transition duration-300"
        >
          {{ showTextResults ? 'Hide' : 'Show' }} Text Results
        </button>
        <button
          @click="showHtmlResults = !showHtmlResults"
          class="bg-purple-600 text-white py-2 px-4 rounded-full hover:bg-purple-700 transition duration-300"
        >
          {{ showHtmlResults ? 'Hide' : 'Show' }} HTML Results
        </button>
      </div>
      
      <div v-if="showTextResults" class="mt-4 p-4 bg-gray-100 rounded-lg whitespace-pre-wrap font-mono">
        {{ results.text }}
      </div>

      <div v-if="showHtmlResults" class="mt-4 w-full">
        <div 
          class="bg-white rounded-lg shadow-md p-8 max-w-none overflow-x-auto min-w-full"
          v-html="results.html"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const config = useRuntimeConfig();

const surveys = ref([]);
const selectedSurvey = ref('');
const password = ref('');
const message = ref('');
const messageType = ref('info');
const isLoading = ref(false);
const loadingSurveys = ref(true);
const results = ref(null);
const showTextResults = ref(false);
const showHtmlResults = ref(false);

const fetchSurveys = async () => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/surveys`);
    if (!response.ok) {
      throw new Error('Failed to fetch surveys');
    }
    const data = await response.json();
    surveys.value = data.surveys;
  } catch (error) {
    message.value = 'Failed to load surveys';
    messageType.value = 'error';
  } finally {
    loadingSurveys.value = false;
  }
};

onMounted(() => {
  fetchSurveys();
});

const downloadZip = () => {
  console.log('Starting download process');
  if (!results.value?.zip_data) {
    console.error('No zip data available:', results.value);
    return;
  }
  
  try {
    console.log('Zip data length:', results.value.zip_data.length);
    
    // Create blob from base64
    const binaryString = window.atob(results.value.zip_data);
    console.log('Binary string length:', binaryString.length);
    
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    console.log('Byte array length:', bytes.length);
    
    const blob = new Blob([bytes], { type: 'application/zip' });
    console.log('Blob size:', blob.size);
    
    // Create and trigger download
    const url = window.URL.createObjectURL(blob);
    console.log('Created blob URL:', url);
    
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `survey_results_${selectedSurvey.value}.zip`;
    
    document.body.appendChild(a);
    console.log('Triggering click');
    a.click();
    
    // Cleanup
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    console.log('Download process complete');
  } catch (error) {
    console.error('Download failed:', error);
    message.value = 'Failed to download results';
    messageType.value = 'error';
  }
};

const requestResults = async () => {
  isLoading.value = true;
  try {
    const response = await fetch(`${config.public.backendUrl}/api/request-results`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        survey_name: selectedSurvey.value,
        password: password.value,
      }),
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();
    console.log('Received results:', {
      hasImages: data.has_images,
      textLength: data.text?.length,
      zipDataLength: data.zip_data?.length
    });
    
    results.value = data;
    message.value = "Results retrieved successfully!";
    messageType.value = 'success';
  } catch (error) {
    console.error('Request failed:', error);
    message.value = error.message || 'Ein Fehler ist aufgetreten';
    messageType.value = 'error';
    results.value = null;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Add these styles to ensure proper HTML rendering */
:deep(h1) {
  margin: 1rem 0;
}
:deep(h2) {
  margin: 1rem 0;
}
:deep(h3) {
  margin: 0.75rem 0;
}
:deep(.participant) {
  break-inside: avoid;
  max-width: 1400px; /* Added max-width */
  margin-left: auto;
  margin-right: auto;
}
:deep(img) {
  display: block;
  margin: 1rem auto;
  max-width: 1200px; /* Increased from 800px */
  width: 100%;
}
:deep(body) {
  max-width: 1400px; /* Added max-width */
  margin-left: auto;
  margin-right: auto;
}
</style>
