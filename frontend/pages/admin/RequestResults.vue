<template>
  <div>
    <h1>Request Survey Results</h1>
    <form @submit.prevent="requestResults">
      <div>
        <label for="surveyName">Survey Name:</label>
        <input type="text" v-model="surveyName" required />
      </div>
      <div>
        <label for="email">Email Address:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Request Results</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const config = useRuntimeConfig();

const surveyName = ref('');
const email = ref('');
const password = ref('');
const message = ref('');

const requestResults = async () => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/request-results`, {
      method: 'POST',
      headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
      survey_name: surveyName.value,
      email: email.value,
      password: password.value,
      }),
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();
    message.value = data.message;
  } catch (error) {
    message.value = error.message || 'An error occurred';
  }
};
</script>
