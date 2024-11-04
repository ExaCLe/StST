<template>
  <div>
    <h1>Available Surveys</h1>
    <ul>
      <li v-for="survey in surveys" :key="survey">
        <NuxtLink
          :to="{ path: '/survey', query: { name: survey } }"
          class="survey-link"
        >
          {{ survey }}
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRuntimeConfig } from '#app';

const config = useRuntimeConfig();
const surveys = ref([]);

onMounted(async () => {
  try {
    const response = await $fetch(`${config.public.backendUrl}/api/surveys`);
    surveys.value = response.surveys;
  } catch (error) {
    console.error(error);
  }
});
</script>
