<template>
    <div>
      <h1>{{ survey.name }}</h1>
      <form @submit.prevent="submitSurvey">
        <div v-for="(question, index) in survey.questions" :key="index">
          <component
            :is="getComponent(question.type)"
            :question="question"
            @answer="updateAnswer(index, $event)"
          ></component>
        </div>
        <button type="submit">Submit Survey</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import MultipleChoice from '@/components/MultipleChoice.vue';
  import TrueFalse from '@/components/TrueFalse.vue';
  import FreeAnswer from '@/components/FreeAnswer.vue';
  import LikertScale from '@/components/LikertScale.vue';
  import ImageQuestion from '@/components/ImageQuestion.vue';
  
  export default {
    components: {
      MultipleChoice,
      TrueFalse,
      FreeAnswer,
      LikertScale,
      ImageQuestion,
    },
    data() {
      return {
        survey: null,
        answers: {},
        message: '',
      };
    },
    methods: {
      getComponent(type) {
        switch (type) {
          case 'MultipleChoice':
            return 'MultipleChoice';
          case 'TrueFalse':
            return 'TrueFalse';
          case 'FreeAnswer':
            return 'FreeAnswer';
          case 'LikertScale':
            return 'LikertScale';
          case 'ImageQuestion':
            return 'ImageQuestion';
          default:
            return null;
        }
      },
      updateAnswer(index, answer) {
        this.answers[index] = answer;
      },
      async submitSurvey() {
        try {
          const response = await this.$axios.post(
            `${process.env.BACKEND_URL}/api/survey/${this.$route.params.name}/response`,
            { answers: this.answers }
          );
          this.message = response.data.message;
        } catch (error) {
          this.message = error.response.data.detail || 'An error occurred';
        }
      },
    },
    async mounted() {
      try {
        const response = await this.$axios.get(
          `${process.env.BACKEND_URL}/api/survey/${this.$route.params.name}`
        );
        this.survey = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  };
  </script>
  