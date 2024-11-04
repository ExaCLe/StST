<template>
    <div>
      <h1>Available Surveys</h1>
      <ul>
        <li v-for="survey in surveys" :key="survey">
          <nuxt-link :to="`/survey/${survey}`">{{ survey }}</nuxt-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        surveys: [],
      };
    },
    async mounted() {
      try {
        const response = await this.$axios.get(
          `${process.env.BACKEND_URL}/api/surveys`
        );
        this.surveys = response.data.surveys;
      } catch (error) {
        console.error(error);
      }
    },
  };
  </script>
  