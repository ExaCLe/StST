<template>
  <div class="question-container">
    <p class="question-text">{{ question.text }}</p>
    <URadioGroup v-model="selectedPoint" :options="options" inline/>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: [Number, null],
});

const emit = defineEmits(['answer']);
const selectedPoint = ref(null);

onMounted(() => {
  selectedPoint.value = props.initialAnswer || null;
});

watch(selectedPoint, (newVal) => {
  emit('answer', newVal);
});

// Define options for the Likert scale based on the scale length in the question
const options = props.question.scale === 5
  ? [{ value: 1, label: '1' }, { value: 2, label: '2' }, { value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }]
  : [{ value: 1, label: '1' }, { value: 2, label: '2' }, { value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }, { value: 6, label: '6' }, { value: 7, label: '7' }];
</script>

<style scoped>
.question-text {
  text-align: left;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.question-container {
  align-items: left;
  display: flex;
}
</style>
