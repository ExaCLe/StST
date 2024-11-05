<template>
  <UContainer class="available-surveys">
    <h1>Verfügbare Umfragen</h1>
    <UAlert v-if="message" :color="alertColor" elevated class="response-alert">
      {{ message }}
    </UAlert>
    <ul v-if="surveys.length > 0">
      <li v-for="survey in surveys" :key="survey">
        <NuxtLink
          :to="{ path: '/survey', query: { name: survey } }"
          class="survey-link"
        >
          {{ survey }}
        </NuxtLink>
      </li>
    </ul>
  </UContainer>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const config = useRuntimeConfig();
const surveys = ref([]);
const message = ref(''); // Message for success or failure
const alertColor = ref(''); // Alert color based on success or error

onMounted(async () => {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/surveys`);
    surveys.value = response.surveys;

    if (surveys.value.length === 0) {
      message.value = 'Keine Umfragen verfügbar'; // Message if no surveys are found
      alertColor.value = 'error';
    } else {
      message.value = 'Umfragen erfolgreich geladen';
      alertColor.value = 'success';
    }
  } catch (error) {
    message.value = 'Fehler beim Laden der Umfragen';
    alertColor.value = 'error';
    console.error(error);
  }
});
</script>

<style scoped>
.available-surveys {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #4a90e2;
}

.survey-link {
  color: #4a90e2;
  text-decoration: none;
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.survey-link:hover {
  text-decoration: underline;
}

.response-alert {
  margin-bottom: 1.5rem;
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
