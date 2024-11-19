<template>
  <div class="container mx-auto px-4 py-8">
    <div class="bg-yellow-100 border-l-4 border-yellow-500 p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <UIcon name="heroicons:information-circle" class="h-5 w-5 text-yellow-500"/>
        </div>
        <div class="ml-3">
          <p class="text-sm text-yellow-700">
            Dies ist eine Vorschau Ihrer Umfrage. Antworten werden nicht gespeichert.
          </p>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="text-center">
      <p>Loading preview...</p>
    </div>
    <Survey 
      v-else-if="surveyData"
      :survey="surveyData"
      :preview-mode="true"
    />
    <div v-else class="text-center">
      <p class="text-red-600">No preview data found. Please go back and try again.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useSurveyPreview } from '~/composables/useSurveyPreview';
import Survey from '~/pages/Survey.vue';

const surveyData = ref(null);
const loading = ref(true);
const { getPreviewData, clearPreviewData } = useSurveyPreview();

onMounted(async () => {
  try {
    surveyData.value = await getPreviewData();
  } catch (e) {
    console.error('Error loading preview:', e);
  } finally {
    loading.value = false;
  }
});

onUnmounted(async () => {
  await clearPreviewData();
});
</script>
