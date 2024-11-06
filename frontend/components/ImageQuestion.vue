<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="relative inline-block">
      <img
        :src="'data:image/png;base64,' + question.images[0].data"
        :alt="question.images[0].name"
        @click="handleClick"
        @load="handleImageLoad"
        class="max-w-full h-auto rounded-lg shadow-md"
        ref="imageRef"
      />
      <div
        v-for="(coord, index) in displayCoordinates"
        :key="index"
        :style="{
          left: `${coord.x}%`,
          top: `${coord.y}%`
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
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
  question: Object,
  initialAnswer: Array,
});

const emit = defineEmits(['answer']);
const coordinates = ref([]); // Store absolute coordinates
const imageRef = ref(null);
const originalImageDimensions = ref({ width: 0, height: 0 });

// Convert absolute to percentage coordinates for display
const displayCoordinates = computed(() => {
  return coordinates.value.map(coord => ({
    x: (coord.x / originalImageDimensions.value.width) * 100,
    y: (coord.y / originalImageDimensions.value.height) * 100
  }));
});

const handleImageLoad = () => {
  const img = imageRef.value;
  originalImageDimensions.value = {
    width: img.naturalWidth,
    height: img.naturalHeight
  };
};

onMounted(() => {
  coordinates.value = props.initialAnswer || [];
});

const handleClick = (event) => {
  const rect = imageRef.value.getBoundingClientRect();
  const scale = originalImageDimensions.value.width / rect.width;
  
  // Calculate absolute coordinates based on original image dimensions
  const x = Math.round((event.clientX - rect.left) * scale);
  const y = Math.round((event.clientY - rect.top) * scale);

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
