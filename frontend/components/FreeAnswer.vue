<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <textarea
      v-model="answer"
      rows="4"
      class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-indigo-500"
      placeholder="Enter your answer here..."
    ></textarea>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: String,
});

const emit = defineEmits(['answer']);
const answer = ref('');

onMounted(() => {
  // Initialize with `initialAnswer` if provided
  answer.value = props.initialAnswer || '';
});

watch(answer, (newVal) => {
  emit('answer', newVal);
});
</script>
