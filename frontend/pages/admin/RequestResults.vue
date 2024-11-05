<template>
  <UContainer class="request-results">
    <UCard class="request-card" elevated>
      <h1>Ergebnisse der Umfrage anfordern</h1>
      <form @submit.prevent="requestResults">
        <div class="form-group">
          <label for="surveyName">Umfragename:</label>
          <UInput v-model="surveyName" type="text" required placeholder="Geben Sie den Namen der Umfrage ein" class="light-input" />
        </div>
        
        <div class="form-group">
          <label for="email">E-Mail Adresse:</label>
          <UInput v-model="email" type="email" required placeholder="Ihre E-Mail-Adresse" class="light-input" />
        </div>
        
        <div class="form-group">
          <label for="password">Passwort:</label>
          <UInput v-model="password" type="password" required placeholder="Ihr Passwort" class="light-input" />
        </div>
        
        <UButton type="submit" color="primary" size="large" elevated class="submit-button">
          Ergebnisse Anfordern
        </UButton>
      </form>
      <p v-if="message" class="response-message">{{ message }}</p>
    </UCard>
  </UContainer>
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
    message.value = error.message || 'Ein Fehler ist aufgetreten';
  }
};
</script>

<style scoped>
.request-results {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.request-card {
  width: 100%;
  max-width: 500px;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.request-card h1 {
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
  background-color: #ffffff !important; /* Light background */
  color: #333 !important;              /* Dark text for readability */
  border: 1px solid #ccc !important;    /* Light border for input fields */
  border-radius: 5px;                   /* Rounded corners */
}

.submit-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
}

.response-message {
  margin-top: 1.5rem;
  font-size: 1rem;
  color: #00796b;
}
</style>
