<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="space-y-3">
      <div 
        v-for="(option, index) in question.options" 
        :key="index"
        class="flex items-center space-x-3"
      >
        <UCheckbox
          v-model="selectedOptions"
          :label="option"
          :value="option"
          :ui="{
            wrapper: 'flex items-center',
            label: 'ml-3 text-gray-700',
            input: {
              color: 'indigo',
              base: 'h-4 w-4 border border-gray-300 focus:ring-indigo-600 checked:bg-indigo-600'
            },
            color: 'indigo'
          }"
        />
      </div>
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
