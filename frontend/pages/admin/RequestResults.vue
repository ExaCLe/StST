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
  
  <script>
  export default {
    data() {
      return {
        surveyName: '',
        email: '',
        password: '',
        message: '',
      };
    },
    methods: {
      async requestResults() {
        try {
          const response = await this.$axios.post(
            `${process.env.BACKEND_URL}/api/request-results`,
            {
              survey_name: this.surveyName,
              email: this.email,
              password: this.password,
            }
          );
          this.message = response.data.message;
        } catch (error) {
          this.message = error.response.data.detail || 'An error occurred';
        }
      },
    },
  };
  </script>
  