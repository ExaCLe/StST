<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="relative inline-block">
      <img
        :src="'data:image/png;base64,' + question.images[0].data"
        :alt="question.images[0].name"
        @click="handleClick"
        class="max-w-full h-auto rounded-lg shadow-md"
      />
      <div
        v-for="(coord, index) in coordinates"
        :key="index"
        :style="{
          left: `${coord.x}px`,
          top: `${coord.y}px`
        }"
        class="absolute w-4 h-4 bg-red-500 rounded-full transform -translate-x-1/2 -translate-y-1/2"
      ></div>
    </div>
    <button
      @click="coordinates = []"
      class="mt-4 bg-red-500 text-white py-2 px-4 rounded-full hover:bg-red-600 transition duration-300"
    >
      Clear Markers
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: Array,
});

const emit = defineEmits(['answer']);
const coordinates = ref([]);

onMounted(() => {
  coordinates.value = props.initialAnswer || [];
});

const handleClick = (event) => {
  const rect = event.currentTarget.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  coordinates.value.push({ x, y });
  emit('answer', coordinates.value);
};
</script>

<style scoped>
.relative {
  position: relative;
  display: inline-block;
}
</style>
