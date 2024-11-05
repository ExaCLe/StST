<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="relative inline-block">
      <img
        v-for="(image, index) in question.images"
        :key="index"
        :src="'data:image/png;base64,' + image.data"
        :alt="image.name"
        @click="handleClick"
        class="max-w-full h-auto rounded-lg shadow-md"
      />
      <div
        v-for="(coord, coordIndex) in coordinates"
        :key="coordIndex"
        :style="{
          top: `${coord.y}px`,
          left: `${coord.x}px`,
        }"
        class="absolute w-4 h-4 bg-indigo-600 rounded-full transform -translate-x-1/2 -translate-y-1/2"
      ></div>
    </div>
    <UButton
      @click="coordinates = []"
      color="red"
      :ui="{ rounded: 'rounded-full' }"
      class="mt-4"
    >
      Clear Markers
    </UButton>
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
.image-container {
  position: relative;
  display: inline-block;
}
.dot {
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: #e91e63;
  border-radius: 50%;
}
</style>
