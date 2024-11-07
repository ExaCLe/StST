<template>
  <div class="max-w-3xl mx-auto">
    <!-- Replace loading indicator -->
    <div v-if="loading" class="flex flex-col items-center justify-center mt-8">
      <svg class="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
      </svg>
      <p class="mt-4 text-indigo-600">Bitte warten Sie ein paar Sekunden, es ist normal, dass es eine Weile dauert.</p>
    </div>
    <div v-else>
      <h1 class="text-3xl font-bold mb-8 text-indigo-800">{{ survey?.name || "Lade Umfrage..." }}</h1>
      
      <div v-if="currentIndex < (survey?.questions?.length || 0)">
        <!-- Progress Bar -->
        <div class="w-full bg-gray-200 rounded-full h-2.5 mb-8">
          <div
            class="bg-indigo-600 h-2.5 rounded-full transition-all duration-300 ease-in-out"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>

        <div class="mb-8 bg-white rounded-lg shadow-md p-6">
          <component
            :is="getComponent(currentQuestion?.type)"
            :question="currentQuestion"
            :initialAnswer="answers[currentIndex]"
            @answer="updateAnswer(currentIndex, $event)"
          />
        </div>

        <div class="flex justify-between">
          <button
            v-if="currentIndex > 0"
            @click="prevQuestion"
            :disabled="currentIndex === 0"
            class="bg-gray-300 text-gray-700 hover:bg-gray-400 transition duration-300 disabled:opacity-50 py-2 px-4 rounded-full"
          >
            Previous
          </button>
          <button
            @click="handleNextOrSubmit"
            class="bg-indigo-600 text-white hover:bg-indigo-700 transition duration-300 py-2 px-4 rounded-full"
            :class="{ 'ml-auto': currentIndex === 0 }"
          >
            {{ isLastQuestion ? 'Submit' : 'Next' }}
          </button>
        </div>
      </div>

      <div v-else class="text-center">
        <h2 class="text-2xl font-bold mb-4 text-indigo-800">Vielen Dank für das Ausfüllen der Umfrage!</h2>
        <p class="text-gray-600 mb-8">{{ 'Ihre Antworten wurden gespeichert.' }}</p>
        <NuxtLink
          to="/surveys"
          class="inline-block bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300"
        >
          Zurück zu den Umfragen
        </NuxtLink>
      </div>
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
const loading = ref(true);

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
    message.value = response.message || 'Ihre Antworten wurden gespeichert.';
    // Weiter zur Abschlussanzeige
    currentIndex.value++;
  } catch (error) {
    console.error(error);
    message.value = error.message || 'Ein Fehler ist aufgetreten';
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
  } finally {
    loading.value = false;
  }
});

// Calculate progress percentage starting from 0% and reaching 100% for the last question
const progressPercentage = computed(() => {
  if (!survey.value?.questions?.length) return 0;
  return Math.round((currentIndex.value / (survey.value.questions.length - 1)) * 100);
});
</script>

<style>
/* CSS für den Spinner */
.spinner {
  border-width: 4px;
}
</style>
