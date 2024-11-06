<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="flex space-x-4">
      <label class="inline-flex items-center">
        <input 
          type="radio" 
          :value="true" 
          v-model="localAnswer" 
          class="form-radio text-indigo-600"
        >
        <span class="ml-2">True</span>
      </label>
      <label class="inline-flex items-center">
        <input 
          type="radio" 
          :value="false" 
          v-model="localAnswer" 
          class="form-radio text-indigo-600"
        >
        <span class="ml-2">False</span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: String,
});

const emit = defineEmits(['answer']);
const localAnswer = ref(null);

onMounted(() => {
  // Convert string 'True'/'False' to boolean
  if (props.initialAnswer) {
    localAnswer.value = props.initialAnswer === 'True';
  }
});

watch(localAnswer, (newVal) => {
  // Convert boolean back to string for emit
  emit('answer', newVal ? 'True' : 'False');
});
</script>
