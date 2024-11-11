<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="flex space-x-4">
      <label class="inline-flex items-center">
        <input 
          type="radio" 
          :value="true" 
          :checked="localAnswer === true"
          @change="handleChange(true)" 
          class="form-radio text-indigo-600"
        >
        <span class="ml-2">Ja</span>
      </label>
      <label class="inline-flex items-center">
        <input 
          type="radio" 
          :value="false" 
          :checked="localAnswer === false"
          @change="handleChange(false)" 
          class="form-radio text-indigo-600"
        >
        <span class="ml-2">Nein</span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: String,
});

const emit = defineEmits(['answer']);
const localAnswer = ref(null);

// Initialize answer when component is created
watch(() => props.initialAnswer, (newVal) => {
  localAnswer.value = newVal === 'True' ? true : newVal === 'False' ? false : null;
}, { immediate: true });

const handleChange = (value) => {
  localAnswer.value = value;
  emit('answer', value ? 'True' : 'False');
};
</script>