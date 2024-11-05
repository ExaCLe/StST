<template>
  <div>
    <p>{{ question.text }}</p>
    <div v-for="(option, index) in question.options" :key="index">
      <UCheckbox :label="option" :value="option" v-model="selectedOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: Array,
});

const emit = defineEmits(['answer']);
const selectedOptions = ref([]);

onMounted(() => {
  console.log(props.initialAnswer);
  selectedOptions.value = props.initialAnswer || [];
});

watch(selectedOptions, (newVal) => {
  emit('answer', newVal);
});
</script>
