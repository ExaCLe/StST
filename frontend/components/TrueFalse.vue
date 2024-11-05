<template>
  <div>
    <p>{{ question.text }}</p>
    <URadioGroup v-model="selectedOption">
      <URadio label="True" value="True" />
      <URadio label="False" value="False" />
    </URadioGroup>
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
