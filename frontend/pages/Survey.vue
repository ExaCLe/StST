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
      
      <div v-if="showConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="text-center bg-white rounded-lg shadow-md p-6 max-w-md mx-4">
          <h2 class="text-2xl font-bold mb-4 text-indigo-800">Möchten Sie die Umfrage abschließen?</h2>
          <p class="text-gray-600 mb-6">Sie haben alle Fragen beantwortet. Klicken Sie auf 'Absenden' um Ihre Antworten zu übermitteln.</p>
          <div class="flex justify-center space-x-4">
            <button
              @click="showConfirmation = false"
              class="bg-gray-300 text-gray-700 hover:bg-gray-400 transition duration-300 py-2 px-4 rounded-full"
            >
              Zurück
            </button>
            <button
              @click="submitSurvey"
              :disabled="isSubmitting"
              class="bg-indigo-600 text-white hover:bg-indigo-700 transition duration-300 py-2 px-4 rounded-full disabled:opacity-50"
            >
              {{ isSubmitting ? 'Wird gesendet...' : 'Absenden' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="submitted" class="text-center bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-bold mb-4 text-green-600">Vielen Dank für Ihre Teilnahme!</h2>
        <p class="text-gray-600 mb-8">Ihre Antworten wurden erfolgreich gespeichert.</p>
        <NuxtLink
          to="/surveys"
          class="inline-block bg-indigo-600 text-white py-2 px-4 rounded-full hover:bg-indigo-700 transition duration-300"
        >
          Zurück zur Übersicht
        </NuxtLink>
      </div>

      <div v-else-if="currentIndex < (survey?.questions?.length || 0)">
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
            :key="`${currentIndex}-${currentQuestion?.internal_id}`"
            @answer="updateAnswer(currentIndex, $event)"
          />
          <!-- Display reference image if available -->
          <div v-if="currentQuestion?.referenceImage" class="mt-4">
            <img :src="'data:image/jpeg;base64,' + currentQuestion.referenceImage" alt="Reference Image" class="w-full h-auto rounded-md" />
          </div>
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
            class="bg-indigo-600 text-white hover:bg-indigo-700 transition duration-300 py-2 px-4 rounded-full tooltip-button"
            :class="{ 
              'ml-auto': currentIndex === 0,
              'opacity-50 cursor-not-allowed': !isCurrentQuestionAnswered
            }"
            :disabled="!isCurrentQuestionAnswered"
            :data-tooltip="!isCurrentQuestionAnswered ? `Diese Frage muss beantwortet werden` : ''"
          >
            {{ isLastQuestion ? 'Review & Submit' : 'Next' }}
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

// Add to props
const props = defineProps({
  survey: {
    type: Object,
    default: null
  },
  previewMode: {
    type: Boolean,
    default: false
  }
});

const survey = ref(null);
const answers = ref({});
const message = ref('');
const currentIndex = ref(0);
const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();
const loading = ref(true);
const showConfirmation = ref(false);
const isSubmitting = ref(false);
const submitted = ref(false);

const questionComponents = {
  MultipleChoice,
  TrueFalse,
  FreeAnswer,
  LikertScale,
  ImageQuestion,
};

// Remove the 'nuxt-color-mode' entry from local storage
if (typeof window !== 'undefined') {
  localStorage.removeItem('nuxt-color-mode');
}

const getComponent = (type) => questionComponents[type] || null;

const currentQuestion = computed(() => survey.value?.questions?.[currentIndex.value]);

const isLastQuestion = computed(() => currentIndex.value === (survey.value?.questions?.length || 1) - 1);

const updateAnswer = (index, answer) => {
  answers.value[index] = answer;
};

const nextQuestion = () => {
  let nextIndex = currentIndex.value + 1;
  while (nextIndex < survey.value.questions.length) {
    const nextQuestion = survey.value.questions[nextIndex];
    if (!nextQuestion.condition) {
      currentIndex.value = nextIndex;
      return;
    }
    
    const conditionQuestion = survey.value.questions.find(
      q => q.internal_id === nextQuestion.condition.questionId
    );
    const conditionQuestionIndex = survey.value.questions.indexOf(conditionQuestion);
    const answer = answers.value[conditionQuestionIndex];
    
    if (answer?.toLowerCase() === nextQuestion.condition.expectedAnswer?.toLowerCase()) {
      currentIndex.value = nextIndex;
      return;
    }
    nextIndex++;
  }
  // If we get here, we've reached the end
  showConfirmation.value = true;
};

const prevQuestion = () => {
  let prevIndex = currentIndex.value - 1;
  while (prevIndex >= 0) {
    const prevQuestion = survey.value.questions[prevIndex];
    if (!prevQuestion.condition) {
      currentIndex.value = prevIndex;
      return;
    }
    
    const conditionQuestion = survey.value.questions.find(
      q => q.internal_id === prevQuestion.condition.questionId
    );
    const conditionQuestionIndex = survey.value.questions.indexOf(conditionQuestion);
    const answer = answers.value[conditionQuestionIndex];
    
    if (answer?.toLowerCase() === prevQuestion.condition.expectedAnswer?.toLowerCase()) {
      currentIndex.value = prevIndex;
      return;
    }
    prevIndex--;
  }
  // If we get here, we've reached the start
  currentIndex.value = 0;
};

const submitSurvey = async () => {
  if (isSubmitting.value) return;
  
  isSubmitting.value = true;
  try {
    let response = null;
    if (!props.previewMode) {
      response = await $fetch(
        `${config.public.backendUrl}/api/survey/${route.query.name}/response`,
        {
          method: 'POST',
          body: JSON.stringify({ answers: answers.value }),
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      
    } else {
      response = { message: 'Preview mode: Antworten wurden aufgrund der Vorschau nicht gespeichert, aber die Umfrage wurde erfolgreich beendet.' };
    }
    showConfirmation.value = false;
    submitted.value = true;
    message.value = response.message || 'Ihre Antworten wurden gespeichert.';
  } catch (error) {
    console.error(error);
    message.value = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.';
  } finally {
    isSubmitting.value = false;
  }
};

// Modify handleNextOrSubmit
const handleNextOrSubmit = () => {
  if (!isCurrentQuestionAnswered.value) return;
  
  if (isLastQuestion.value) {
    showConfirmation.value = true;
  } else {
    nextQuestion();
  }
};

// Modify onMounted
onMounted(async () => {
  if (props.previewMode && props.survey) {
    // Set survey data directly from props in preview mode
    survey.value = props.survey;
    loading.value = false;
    return;
  }

  try {
    const response = await $fetch(
      `${config.public.backendUrl}/api/survey/${route.query.name}`
    );

    survey.value = {
      ...response,
      questions: response.questions.map((question) => {
        // Attach reference image if present
        if (question.referenceImage) {
          question.referenceImage = question.referenceImage;
        }
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

const isCurrentQuestionAnswered = computed(() => {
  // If question is not required, always return true
  if (!currentQuestion.value?.required) return true;
  
  const answer = answers.value[currentIndex.value];
  if (!answer) return false;

  switch (currentQuestion.value?.type) {
    case 'MultipleChoice':
      return Array.isArray(answer) ? answer.length > 0 : !!answer;
    case 'TrueFalse':
      return answer === "True" || answer === "False";
    case 'FreeAnswer':
      return !!answer && answer.trim().length > 0;
    case 'LikertScale':
      return typeof answer === 'number';
    case 'ImageQuestion':
      return Array.isArray(answer) && answer.length > 0 && answer.every(a => a.text?.trim().length > 0);
    default:
      return false;
  }
});
</script>

<style>
/* CSS für den Spinner */
.spinner {
  border-width: 4px;
}

.fixed {
  position: fixed;
}

.inset-0 {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.z-50 {
  z-index: 50;
}

.tooltip-button {
  position: relative;
}

.tooltip-button[disabled]::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding: 4px 8px;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  font-size: 12px;
  white-space: nowrap;
  border-radius: 4px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.1s ease;
  pointer-events: none;
  margin-bottom: 5px;
}

.tooltip-button[disabled]:hover::after {
  opacity: 1;
  visibility: visible;
}
</style>
