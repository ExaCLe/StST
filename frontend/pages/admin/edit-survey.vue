<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">Edit Survey</h1>

    <div v-if="loading" class="text-center">
      <p>Loading...</p>
    </div>
    <div v-else>
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Survey</label>
        <select
          v-model="selectedSurvey"
          @change="loadSurveyData"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="">Select a survey</option>
          <option v-for="survey in surveys" :key="survey" :value="survey">
            {{ survey }}
          </option>
        </select>
      </div>

      <SurveyForm
        v-if="surveyData"
        :initialData="surveyData"
        submitButtonText="Update Survey"
        :onSubmit="updateSurvey"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SurveyForm from '~/components/SurveyForm.vue';
import { useRuntimeConfig } from '#imports';

const config = useRuntimeConfig();
const loading = ref(true);
const surveys = ref([]);
const selectedSurvey = ref('');
const surveyData = ref(null);

const loadSurveys = async () => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/surveys`);
    const data = await response.json();
    surveys.value = data.surveys;
  } catch (error) {
    console.error('Failed to load surveys:', error);
  } finally {
    loading.value = false;
  }
};

const loadSurveyData = async () => {
  if (!selectedSurvey.value) return;
  
  try {
    loading.value = true;
    const response = await fetch(`${config.public.backendUrl}/api/survey/${selectedSurvey.value}`);
    const data = await response.json();
    
    // Create a map of image name to base64 data
    const imageMap = data.images.reduce((acc, img) => {
      acc[img.name] = `data:image/jpeg;base64,${img.data}`;
      return acc;
    }, {});

    // Attach images to their corresponding questions and add unique IDs
    const questionsWithImages = data.questions.map((q, index) => {
      const questionWithId = {
        ...q,
        id: Date.now() + index // Ensure unique ID for each question
      };
      
      if (q.type === 'ImageQuestion' && q.imageName && imageMap[q.imageName]) {
        return { ...questionWithId, image: imageMap[q.imageName] };
      }
      return questionWithId;
    });

    surveyData.value = {
      surveyTitle: data.name,
      questions: questionsWithImages,
      adminPassword: ''
    };
  } catch (error) {
    console.error('Failed to load survey data:', error);
  } finally {
    loading.value = false;
  }
};

const updateSurvey = async (formData) => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/update-survey/${selectedSurvey.value}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        adminPassword: formData.adminPassword,
        title: formData.surveyTitle,
        questions: formData.questions,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update survey');
    }

    alert('Survey updated successfully!');
  } catch (error) {
    alert(error.message);
  }
};

onMounted(loadSurveys);
</script>
