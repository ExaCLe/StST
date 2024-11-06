<template>
  <div class="container mx-auto px-4 py-8">
    <p class="text-3xl font-bold mb-8 text-indigo-800">Verfügbare Umfragen</p>

    <div v-if="surveys.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="survey in formattedSurveys" 
        :key="survey.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300"
      >
        <div class="p-6">
          <h2 class="text-xl font-semibold mb-2 text-indigo-600">{{ survey.name }}</h2>
          <p class="text-gray-600 mb-4">Nehmen Sie an dieser Umfrage teil</p>
          <NuxtLink
            :to="{ path: '/survey', query: { name: survey.name } }"
            class="inline-block bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300"
          >
            Umfrage starten
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const config = useRuntimeConfig();
const surveys = ref([]);
const toast = useToast();

const formattedSurveys = computed(() => {
  return surveys.value.map((name, index) => ({
    id: index + 1,
    name: name
  }));
});

onMounted(async () => {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/surveys`);
    surveys.value = response.surveys;

    if (surveys.value.length === 0) {
      toast.add({
        title: 'Keine Umfragen verfügbar',
        description: 'Es sind derzeit keine Umfragen verfügbar.',
        color: 'yellow'
      });
    }
  } catch (error) {
    toast.add({
      title: 'Fehler beim Laden der Umfragen',
      description: 'Es ist ein Fehler beim Laden der Umfragen aufgetreten.',
      color: 'primary'
    })
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
