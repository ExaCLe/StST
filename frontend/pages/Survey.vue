<template>
  <div>
    <h1>{{ survey?.name || "Loading..." }}</h1>
    <form @submit.prevent="submitSurvey">
      <div v-for="(question, index) in survey?.questions" :key="index">
        <!-- Render question components based on their type -->
        <component
          :is="getComponent(question.type)"
          :question="question"
          @answer="updateAnswer(index, $event)"
        />
      </div>
      <button type="submit">Submit Survey</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import MultipleChoice from '~/components/MultipleChoice.vue';
import TrueFalse from '~/components/TrueFalse.vue';
import FreeAnswer from '~/components/FreeAnswer.vue';
import LikertScale from '~/components/LikertScale.vue';
import ImageQuestion from '~/components/ImageQuestion.vue';

const survey = ref(null);
const answers = ref({});
const message = ref('');
const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();

const questionComponents = {
  MultipleChoice,
  TrueFalse,
  FreeAnswer,
  LikertScale,
  ImageQuestion,
};

const getComponent = (type) => {
  return questionComponents[type] || null;
};

const updateAnswer = (index, answer) => {
  answers.value[index] = answer;
};

const submitSurvey = async () => {
  try {
    const response = await $fetch(
      `${config.public.backendUrl}/api/survey/${route.query.name}/response`,
      {
        method: 'POST',
        body: JSON.stringify({ answers: answers.value }),
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    message.value = response.message;

    router.push('/');
  } catch (error) {
    console.error(error);
    message.value = error.message || 'An error occurred';
  }
};

onMounted(async () => {
  try {
    const response = await $fetch(
      `${config.public.backendUrl}/api/survey/${route.query.name}`
    );

    survey.value = {
      ...response,
      questions: response.questions.map((question) => {
        if (question.type === 'ImageQuestion') {
          return {
            ...question,
            images: response.images.filter(
              (image) => image.name === question.imageName
            ),
          };
        }
        return question;
      }),
    };
  } catch (error) {
    console.error(error);
  }
});
</script>
