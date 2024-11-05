<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8 text-indigo-800">Ergebnisse der Umfrage anfordern</h1>
    <form @submit.prevent="requestResults" class="space-y-6">
      <div>
        <UFormGroup label="Umfragename" class="block">
          <USelect
            v-model="selectedSurvey"
            :options="surveys.map(name => ({ id: name, name: name }))"
            option-attribute="name"
            value-attribute="id"
            required
            class="w-full"
            :loading="loadingSurveys"
          />
        </UFormGroup>
      </div>
      <div>
        <UFormGroup label="E-Mail Adresse" class="block">
          <UInput
            v-model="email"
            type="email"
            required
            placeholder="Ihre E-Mail-Adresse"
          />
        </UFormGroup>
      </div>
      <div>
        <UFormGroup label="Passwort" class="block">
          <UInput
            v-model="password"
            type="password"
            required
            placeholder="Ihr Passwort"
          />
        </UFormGroup>
      </div>
      <UButton
        type="submit"
        color="primary"
        variant="solid"
        class="w-full bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300 text-center"
        :loading="isLoading"
      >
        Ergebnisse Anfordern
      </UButton>
    </form>
    <UAlert
      v-if="message"
      :type="messageType"
      :text="message"
      class="mt-4"
    />
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
