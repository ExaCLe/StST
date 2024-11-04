<template>
  <div>
    <h1>Upload Survey</h1>
    <form @submit.prevent="uploadSurvey">
      <div>
        <label for="name">Survey Name:</label>
        <input type="text" v-model="name" required />
      </div>
      <div>
        <label for="csv">CSV File:</label>
        <input type="file" @change="handleCSVUpload" accept=".csv" required />
      </div>
      <div>
        <label for="images">Images:</label>
        <input type="file" multiple @change="handleImageUpload" accept="image/*" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Upload Survey</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
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

      console.log("Here")

      try {
        const response = await fetch(`${config.public.backendUrl}/api/upload-survey`, {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        console.log(data)
        if (!response.ok) {
          throw new Error(data.detail || 'An error occurred');
        }
        message.value = data.message;
      } catch (error) {
        console.log(error)
        message.value = error.response || 'An error occurred';
      }
    };

    return {
      name,
      csvFile,
      images,
      password,
      message,
      handleCSVUpload,
      handleImageUpload,
      uploadSurvey,
    };
  },
};
</script>