<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="flex justify-between mb-2">
      <div class="flex justify-between w-full">
        <label v-for="option in options" :key="option.value" class="flex flex-col items-center">
          <input
            type="radio"
            :value="option.value"
            :checked="selectedPoint === option.value"
            @change="handleChange(option.value)"
            class="form-radio text-indigo-600"
          />
          <span>{{ option.label }}</span>
        </label>
      </div>
    </div>
    <div class="flex justify-between text-sm text-gray-600">
      <span>Strongly Disagree</span>
      <span>Strongly Agree</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: [Number, null],
});

const emit = defineEmits(['answer']);
const selectedPoint = ref(null);

// Initialize answer when component is created
watch(() => props.initialAnswer, (newVal) => {
  selectedPoint.value = typeof newVal === 'number' ? newVal : null;
}, { immediate: true });

const handleChange = (value) => {
  selectedPoint.value = value;
  emit('answer', value);
};

const options = props.question.scale_points === 5
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
