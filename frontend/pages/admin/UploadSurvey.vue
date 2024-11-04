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
  export default {
    data() {
      return {
        name: '',
        csvFile: null,
        images: [],
        password: '',
        message: '',
      };
    },
    methods: {
      handleCSVUpload(event) {
        this.csvFile = event.target.files[0];
      },
      handleImageUpload(event) {
        this.images = Array.from(event.target.files);
      },
      async uploadSurvey() {
        const formData = new FormData();
        formData.append('name', this.name);
        formData.append('password', this.password);
        formData.append('csv_file', this.csvFile);
        this.images.forEach((image) => {
          formData.append('images', image);
        });
  
        try {
          const response = await this.$axios.post(
            `${process.env.BACKEND_URL}/api/upload-survey`,
            formData
          );
          this.message = response.data.message;
        } catch (error) {
          this.message = error.response.data.detail || 'An error occurred';
        }
      },
    },
  };
  </script>
  