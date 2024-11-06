<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="space-y-2">
      <label 
        v-for="(option, index) in question.options" 
        :key="index" 
        class="flex items-center"
      >
        <input 
          type="checkbox" 
          :value="option" 
          v-model="selectedOptions"
          class="form-checkbox text-indigo-600 h-4 w-4 border-gray-300 rounded"
        >
        <span class="ml-2">{{ option }}</span>
      </label>
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
  selectedOptions.value = props.initialAnswer || [];
});

watch(selectedOptions, (newVal) => {
  emit('answer', newVal);
});
</script>
