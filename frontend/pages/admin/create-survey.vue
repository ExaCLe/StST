<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">Create a New Survey</h1>
    <SurveyForm
      :initialData="{ adminPassword: '', surveyTitle: '', questions: [] }"
      submitButtonText="Create Survey"
      :onSubmit="createSurvey"
      @preview="handlePreview"
    />
  </div>
</template>

<script setup>
import { useRuntimeConfig } from '#imports';
import SurveyForm from '~/components/SurveyForm.vue';
import { useSurveyPreview } from '~/composables/useSurveyPreview';

const config = useRuntimeConfig();
const { openPreview } = useSurveyPreview();

const createSurvey = async (formData) => {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/create-survey`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        adminPassword: formData.adminPassword,
        title: formData.surveyTitle,
        questions: formData.questions,
      }),
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'An error occurred');

    alert('Survey created successfully!');
  } catch (error) {
    alert('Failed to create survey: ' + error.message);
  }
};

const handlePreview = (surveyData) => {
  openPreview(surveyData);
};
</script>
