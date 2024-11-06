<template>
  <div class="image-question">
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="relative" ref="imageContainer">
      <img
        :src="'data:image/png;base64,' + question.images[0].data"
        :alt="question.images[0].name"
        @click="handleClick"
        @load="handleImageLoad"
        :class="{ 'cursor-crosshair': currentTool === 'stamp' }"
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
        @click="removeMarker(index)"
      ></div>
    </div>
    <div class="toolbar mt-4 flex space-x-2">
      <button
        @click="toggleFullScreen"
        class="bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 transition duration-300"
        :title="isFullScreen ? 'Exit full screen' : 'Enter full screen'"
      >
        <Maximize2 v-if="!isFullScreen" class="w-5 h-5" />
        <Minimize2 v-else class="w-5 h-5" />
      </button>
      <button
        @click="setTool('stamp')"
        class="bg-green-500 text-white p-2 rounded-full hover:bg-green-600 transition duration-300"
        :class="{ 'ring-2 ring-offset-2 ring-green-500': currentTool === 'stamp' }"
        title="Add marker"
      >
        <MapPin class="w-5 h-5" />
      </button>
      <button
        @click="setTool('eraser')"
        class="bg-yellow-500 text-white p-2 rounded-full hover:bg-yellow-600 transition duration-300"
        :class="{ 'ring-2 ring-offset-2 ring-yellow-500': currentTool === 'eraser' }"
        title="Erase marker"
      >
        <Eraser class="w-5 h-5" />
      </button>
      <button
        @click="clearAllMarkers"
        class="bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition duration-300"
        title="Clear all markers"
      >
        <Trash2 class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { Maximize2, Minimize2, MapPin, Eraser, Trash2 } from 'lucide-vue-next';

const props = defineProps({
  question: Object,
  initialAnswer: Array,
});

const emit = defineEmits(['answer']);
const coordinates = ref([]);
const imageRef = ref(null);
const imageContainer = ref(null);
const originalImageDimensions = ref({ width: 0, height: 0 });
const currentTool = ref('stamp');
const isFullScreen = ref(false);

const displayCoordinates = computed(() => {
  if (!imageRef.value) return [];
  
  const rect = imageRef.value.getBoundingClientRect();
  const scaleWidth = rect.width / originalImageDimensions.value.width;
  const scaleHeight = rect.height / originalImageDimensions.value.height;
  
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

const handleClick = (event) => {
  if (currentTool.value !== 'stamp') return;
  
  const rect = imageRef.value.getBoundingClientRect();
  
  // Calculate relative position within the image
  const relativeX = event.clientX - rect.left;
  const relativeY = event.clientY - rect.top;
  
  // Convert to percentage of original image dimensions
  const x = Math.round((relativeX / rect.width) * originalImageDimensions.value.width);
  const y = Math.round((relativeY / rect.height) * originalImageDimensions.value.height);
  
  // Only add marker if within image bounds
  if (x >= 0 && x <= originalImageDimensions.value.width && 
      y >= 0 && y <= originalImageDimensions.value.height) {
    coordinates.value.push({ x, y });
    emit('answer', coordinates.value);
  }
};

const setTool = (tool) => {
  currentTool.value = tool;
};

const removeMarker = (index) => {
  if (currentTool.value === 'eraser') {
    coordinates.value.splice(index, 1);
    emit('answer', coordinates.value);
  }
};

const clearAllMarkers = () => {
  coordinates.value = [];
  emit('answer', coordinates.value);
};

const toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    imageContainer.value.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
};

const handleFullScreenChange = () => {
  isFullScreen.value = !!document.fullscreenElement;
};

onMounted(() => {
  coordinates.value = props.initialAnswer || [];
  document.addEventListener('fullscreenchange', handleFullScreenChange);
});

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullScreenChange);
});
</script>

<style scoped>
.image-question {
  transition: all 0.3s ease;
}

:fullscreen {
  background: white;
}

:fullscreen .image-question {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

:fullscreen .relative {
  position: relative;
  width: 100%;
  height: calc(100vh - 8rem);
  display: flex;
  align-items: center;
  justify-content: center;
}

:fullscreen img {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}

:fullscreen .toolbar {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 0.5rem;
  border-radius: 9999px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 9999;
}

.toolbar {
  z-index: 9999;
}
</style>
