<template>
  <div>
    <p>{{ question.text }}</p>
    <UTextarea v-model="answer" @input="emitAnswer" placeholder="Type your answer..." />
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
