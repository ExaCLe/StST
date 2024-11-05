<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <URadioGroup
      v-model="selectedOption"
      :options="[
        { label: 'True', value: 'True' },
        { label: 'False', value: 'False' }
      ]"
      class="flex space-x-4"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: String,
});

const emit = defineEmits(['answer']);
const selectedOption = ref(null);

onMounted(() => {
  selectedOption.value = props.initialAnswer || null;
});

watch(selectedOption, (newVal) => {
  emit('answer', newVal);
});
</script>
