<template>
  <UContainer class="upload-survey">
    <UCard class="upload-card" elevated>
      <h1>Umfrage Hochladen</h1>
      <form @submit.prevent="uploadSurvey">
        <div class="form-group">
          <label for="name">Umfragename:</label>
          <UInput v-model="name" type="text" required placeholder="Geben Sie den Namen der Umfrage ein" class="light-input" />
        </div>

        <div class="form-group">
          <label for="csv">CSV Datei:</label>
          <UInput type="file" @change="handleCSVUpload" accept=".csv" required class="light-input" />
        </div>

        <div class="form-group">
          <label for="images">Bilder:</label>
          <UInput type="file" multiple @change="handleImageUpload" accept="image/*" class="light-input" />
        </div>

        <div class="form-group">
          <label for="password">Passwort:</label>
          <UInput v-model="password" type="password" required placeholder="Ihr Passwort" class="light-input" />
        </div>

        <UButton type="submit" color="primary" size="large" elevated class="submit-button">
          Umfrage Hochladen
        </UButton>
      </form>

      <UAlert v-if="message" :color="alertColor" elevated class="response-alert">
        {{ message }}
      </UAlert>
    </UCard>
  </UContainer>
</template>

<script>
import { ref } from 'vue';
const config = useRuntimeConfig();

export default {
  setup() {
    const name = ref('');
    const csvFile = ref(null);
    const images = ref([]);
    const password = ref('');
    const message = ref('');
    const alertColor = ref(''); // Color for the alert: 'success' for green, 'error' for red

    const handleCSVUpload = (event) => {
      csvFile.value = event.target.files[0];
    };

    const handleImageUpload = (event) => {
      images.value = Array.from(event.target.files);
    };

    const uploadSurvey = async () => {
      const formData = new FormData();
      formData.append('name', name.value);
      formData.append('password', password.value);
      formData.append('csv_file', csvFile.value);
      images.value.forEach((image) => {
        formData.append('images', image);
      });

      try {
        const response = await fetch(`${config.public.backendUrl}/api/upload-survey`, {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Ein Fehler ist aufgetreten');
        }
        message.value = data.message || 'Umfrage erfolgreich hochgeladen';
        alertColor.value = 'success'; // Green alert for success
      } catch (error) {
        message.value = error.message || 'Ein Fehler ist aufgetreten';
        alertColor.value = 'error'; // Red alert for failure
      }
    };

    return {
      name,
      csvFile,
      images,
      password,
      message,
      alertColor,
      handleCSVUpload,
      handleImageUpload,
      uploadSurvey,
    };
  },
};
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
