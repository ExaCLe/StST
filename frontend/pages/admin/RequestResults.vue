<template>
  <div class="max-w-2xl mx-auto">
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
        <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        />
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const config = useRuntimeConfig();

const surveys = ref([]);
const selectedSurvey = ref('');
const email = ref('');
const password = ref('');
const message = ref('');
const messageType = ref('info');
const isLoading = ref(false);
const loadingSurveys = ref(true);

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
        email: email.value,
        password: password.value,
      }),
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();
    message.value = data.message;
    messageType.value = 'success';
    
    // Reset form
    selectedSurvey.value = '';
    email.value = '';
    password.value = '';
  } catch (error) {
    message.value = error.message || 'Ein Fehler ist aufgetreten';
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};
</script>
