<template>
  <UContainer class="survey-page">
    <!-- Survey Title -->
    <h1 class="survey-title">{{ survey?.name || "Loading Survey..." }}</h1>

    <UCard class="survey-card" elevated>
      <!-- NuxtUI Progress Bar -->
      <UProgress :value="progressPercentage" color="green" class="progress-bar" />

      <!-- Display Current Question -->
      <div v-if="currentQuestion" class="question-container">
        <component
          :is="getComponent(currentQuestion.type)"
          :question="currentQuestion"
          :initialAnswer="answers[currentIndex] || null" 
          @answer="updateAnswer(currentIndex, $event)"
        />
      </div>

      <!-- Navigation Buttons -->
      <div class="navigation-buttons">
        <UButton v-if="currentIndex > 0" @click="prevQuestion" variant="outline" class="previous-button">
          Previous
        </UButton>
        <UButton v-if="!isLastQuestion" @click="nextQuestion" class="action-button">
          Next
        </UButton>
        <UButton v-if="isLastQuestion" @click="submitSurvey" class="action-button">
          Submit Survey
        </UButton>
      </div>
    </UCard>

    <p v-if="message">{{ message }}</p>
  </UContainer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import MultipleChoice from '~/components/MultipleChoice.vue';
import TrueFalse from '~/components/TrueFalse.vue';
import FreeAnswer from '~/components/FreeAnswer.vue';
import LikertScale from '~/components/LikertScale.vue';
import ImageQuestion from '~/components/ImageQuestion.vue';

const survey = ref(null);
const answers = ref({});
const message = ref('');
const currentIndex = ref(0);
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

const getComponent = (type) => questionComponents[type] || null;

const currentQuestion = computed(() => survey.value?.questions?.[currentIndex.value]);

const isLastQuestion = computed(() => currentIndex.value === (survey.value?.questions?.length || 1) - 1);

const updateAnswer = (index, answer) => {
  answers.value[index] = answer;
};

const nextQuestion = () => {
  if (currentIndex.value < survey.value.questions.length - 1) currentIndex.value++;
};

const prevQuestion = () => {
  if (currentIndex.value > 0) currentIndex.value--;
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

// Calculate progress percentage starting from 0% and reaching 100% for the last question
const progressPercentage = computed(() => ((currentIndex.value) / (survey.value?.questions?.length - 1 || 1)) * 100);
</script>

<style scoped>
.survey-page {
  padding: 2rem;
}

.survey-title {
  font-size: 2rem;
  color: black;
  text-align: left;
  margin-bottom: 1rem;
  font-weight: bold;
}

.survey-card {
  padding: 2rem;
  background-color: #e0f7fa;
  color: #004d40;
  border-radius: 10px;
  text-align: center;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.progress-bar {
  margin-bottom: 1rem;
  color: #4caf50;  
}

.previous-button {
  color:#4caf50;  
  border-color: #4caf50;
}

/* Styling for Next and Submit Button */
.action-button {
  margin-left: auto;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 5px;
  background-color: #4caf50; /* Green color to match progress bar */
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
