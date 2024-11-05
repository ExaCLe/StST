<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8 text-indigo-800">{{ survey?.name || "Loading Survey..." }}</h1>
    
    <div v-if="currentIndex < (survey?.questions?.length || 0)" class="space-y-8">
      <!-- Add Progress Bar -->
      <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div
          class="bg-indigo-600 h-2.5 rounded-full transition-all duration-300 ease-in-out"
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <component
          :is="getComponent(currentQuestion?.type)"
          :question="currentQuestion"
          :initialAnswer="answers[currentIndex]"
          @answer="updateAnswer(currentIndex, $event)"
        />
      </div>

      <div class="flex justify-between">
        <UButton
          v-if="currentIndex > 0"
          @click="prevQuestion"
          :ui="{ rounded: 'rounded-full' }"
          variant="ghost"
          class="text-gray-700 hover:bg-gray-100"
        >
          Previous
        </UButton>
        <UButton
          @click="handleNextOrSubmit"
          :ui="{ rounded: 'rounded-full' }"
          color="indigo"
          class="ml-auto"
        >
          {{ isLastQuestion ? 'Submit' : 'Next' }}
        </UButton>
      </div>
    </div>

    <div v-else class="text-center">
      <h2 class="text-2xl font-bold mb-4 text-indigo-800">Thank you for completing the survey!</h2>
      <p class="text-gray-600 mb-8">{{ message || 'Your responses have been recorded.' }}</p>
      <UButton
        to="/"
        :ui="{ rounded: 'rounded-full' }"
        color="indigo"
      >
        Back to Surveys
      </UButton>
    </div>
  </div>
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
  if (survey.value && currentIndex.value < survey.value.questions.length - 1) {
    currentIndex.value++;
  }
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

const handleNextOrSubmit = () => {
  if (isLastQuestion.value) {
    submitSurvey();
  } else {
    nextQuestion();
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
const progressPercentage = computed(() => {
  if (!survey.value?.questions?.length) return 0;
  return Math.round((currentIndex.value / (survey.value.questions.length - 1)) * 100);
});
</script>
