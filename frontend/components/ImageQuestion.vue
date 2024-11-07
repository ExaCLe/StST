<template>
  <div class="image-question">
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <div class="relative fullscreen-container" ref="imageContainer">
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
          left: `calc(${coord.x}px + ${offset.left}px - 12px)`,
          top: `calc(${coord.y}px + ${offset.top}px - 24px)`
        }"
        class="absolute transform"
        @click="removeMarker(index)"
      >
        <MapPin class="w-6 h-6 text-red-500" />
      </div>

      <!-- Desktop Toolbar -->
      <div
        v-if="!isMobile"
        class="toolbar-container"
        ref="toolbarRef"
        :style="{
          top: `${toolbarPosition.y}px`,
          left: `${toolbarPosition.x}px`,
          cursor: isDragging ? 'grabbing' : 'grab'
        }"
        @mousedown.stop="startDragging"
        @touchstart.stop.prevent="startDragging"
      >
        <div class="toolbar mt-4 flex space-x-2" @click.stop>
          <div class="drag-handle flex items-center px-2 text-gray-400">
            <GripVertical class="w-4 h-4" />
          </div>
          <button
            @click.stop="toggleFullScreen"
            @touchend.stop.prevent="handleButtonTouch($event, toggleFullScreen)"
            class="bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 transition duration-300"
            :title="isFullScreen ? 'Exit full screen' : 'Enter full screen'"
          >
            <Maximize2 v-if="!isFullScreen" class="w-5 h-5" />
            <Minimize2 v-else class="w-5 h-5" />
          </button>
          <button
            @click.stop="setTool('stamp')"
            @touchend.stop.prevent="handleButtonTouch($event, () => setTool('stamp'))"
            class="bg-green-500 text-white p-2 rounded-full hover:bg-green-600 transition duration-300"
            :class="{ 'ring-2 ring-offset-2 ring-green-500': currentTool === 'stamp' }"
            title="Add marker"
          >
            <MapPin class="w-5 h-5" />
          </button>
          <button
            @click.stop="setTool('eraser')"
            @touchend.stop.prevent="handleButtonTouch($event, () => setTool('eraser'))"
            class="bg-yellow-500 text-white p-2 rounded-full hover:bg-yellow-600 transition duration-300"
            :class="{ 'ring-2 ring-offset-2 ring-yellow-500': currentTool === 'eraser' }"
            title="Erase marker"
          >
            <Eraser class="w-5 h-5" />
          </button>
          <button
            @click.stop="clearAllMarkers"
            @touchend.stop.prevent="handleButtonTouch($event, clearAllMarkers)"
            class="bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition duration-300"
            title="Clear all markers"
          >
            <Trash2 class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Mobile Toolbar -->
      <div v-else class="mt-4 flex space-x-2 justify-center">
        <div class="toolbar">
          <button
            @click.stop="setTool('stamp')"
            @touchend.stop.prevent="handleButtonTouch($event, () => setTool('stamp'))"
            class="bg-green-500 text-white p-2 rounded-full hover:bg-green-600 transition duration-300"
            :class="{ 'ring-2 ring-offset-2 ring-green-500': currentTool === 'stamp' }"
            title="Add marker"
          >
            <MapPin class="w-5 h-5" />
          </button>
          <button
            @click.stop="setTool('eraser')"
            @touchend.stop.prevent="handleButtonTouch($event, () => setTool('eraser'))"
            class="bg-yellow-500 text-white p-2 rounded-full hover:bg-yellow-600 transition duration-300"
            :class="{ 'ring-2 ring-offset-2 ring-yellow-500': currentTool === 'eraser' }"
            title="Erase marker"
          >
            <Eraser class="w-5 h-5" />
          </button>
          <button
            @click.stop="clearAllMarkers"
            @touchend.stop.prevent="handleButtonTouch($event, clearAllMarkers)"
            class="bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition duration-300"
            title="Clear all markers"
          >
            <Trash2 class="w-5 h-5" />
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, nextTick } from 'vue';
import { Maximize2, Minimize2, MapPin, Eraser, Trash2, GripVertical } from 'lucide-vue-next';

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
const offset = ref({ top: 0, left: 0 });
const fullscreenTrigger = ref(0);
const imageAspectRatio = ref(0);
const screenAspectRatio = ref(0);
const currentImageWidth = ref(0);
const currentImageHeight = ref(0);
const isMobile = ref(false);

const displayCoordinates = computed(() => {
  fullscreenTrigger.value;
  if (!imageRef.value) return [];

  return coordinates.value.map(coord => ({
    x: (coord.x / originalImageDimensions.value.width) * currentImageWidth.value,
    y: (coord.y / originalImageDimensions.value.height) * currentImageHeight.value,
  }));
});

const handleImageLoad = async () => {
  const img = imageRef.value;
  originalImageDimensions.value = {
    width: img.naturalWidth,
    height: img.naturalHeight,
  };
  imageAspectRatio.value = originalImageDimensions.value.width / originalImageDimensions.value.height;
  calculateCurrentImageHeightAndWidth();

  // Wait for DOM to update
  await nextTick();

  // Move toolbar positioning here
  if (!isMobile.value) {
    // Position the toolbar for desktop devices
    const rect = imageContainer.value.getBoundingClientRect();
    const toolbarRect = toolbarRef.value.getBoundingClientRect();

    toolbarPosition.value = {
      x: rect.left + rect.width / 2 - toolbarRect.width / 2,
      y: rect.top + rect.height - toolbarRect.height - 10,
    };
  }
};

const handleClick = event => {
  if (currentTool.value !== 'stamp') return;

  const rect = imageRef.value.getBoundingClientRect();

  if (!isFullScreen.value) {
    const relativeX = event.clientX - rect.left;
    const relativeY = event.clientY - rect.top;

    const x = Math.round((relativeX / rect.width) * originalImageDimensions.value.width);
    const y = Math.round((relativeY / rect.height) * originalImageDimensions.value.height);

    if (
      x >= 0 &&
      x <= originalImageDimensions.value.width &&
      y >= 0 &&
      y <= originalImageDimensions.value.height
    ) {
      coordinates.value.push({ x, y });
      emit('answer', coordinates.value);
    }
  } else {
    if (
      event.clientX < offset.value.left ||
      event.clientX > offset.value.left + currentImageWidth.value ||
      event.clientY < offset.value.top ||
      event.clientY > offset.value.top + currentImageHeight.value
    ) {
      return;
    }

    const relativeX = event.clientX - offset.value.left;
    const relativeY = event.clientY - offset.value.top;

    const x = Math.round((relativeX / currentImageWidth.value) * originalImageDimensions.value.width);
    const y = Math.round((relativeY / currentImageHeight.value) * originalImageDimensions.value.height);

    if (
      x >= 0 &&
      x <= originalImageDimensions.value.width &&
      y >= 0 &&
      y <= originalImageDimensions.value.height
    ) {
      coordinates.value.push({ x, y });
      emit('answer', coordinates.value);
    }
  }
};

const setTool = tool => {
  currentTool.value = tool;
};

const removeMarker = index => {
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

const calculateCurrentImageHeightAndWidth = () => {
  const rect = imageRef.value.getBoundingClientRect();
  if (!isFullScreen.value) {
    currentImageHeight.value = rect.height;
    currentImageWidth.value = rect.width;
    return;
  }

  screenAspectRatio.value = rect.width / rect.height;
  if (screenAspectRatio.value > imageAspectRatio.value) {
    currentImageWidth.value = rect.height * imageAspectRatio.value;
    currentImageHeight.value = rect.height;
  } else {
    currentImageHeight.value = rect.width / imageAspectRatio.value;
    currentImageWidth.value = rect.width;
  }
  fullscreenTrigger.value++;
};

const handleFullScreenChange = () => {
  isFullScreen.value = !!document.fullscreenElement;
  document.body.classList.toggle('fullscreen-mode', isFullScreen.value);

  if (isFullScreen.value) {
    offset.value = { top: 0, left: 0 };
  }

  setTimeout(() => {
    calculateCurrentImageHeightAndWidth();
    const rect = imageRef.value.getBoundingClientRect();
    if (isFullScreen.value) {
      if (screenAspectRatio.value > imageAspectRatio.value) {
        offset.value.top = 0;
        offset.value.left = (rect.width - currentImageWidth.value) / 2;
      } else {
        offset.value.left = 0;
        offset.value.top = (rect.height - currentImageHeight.value) / 2;
      }
    } else {
      offset.value = { top: 0, left: 0 };
    }
  }, 100);
};

const toolbarRef = ref(null);
const toolbarPosition = ref({ x: 20, y: 20 });
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

const movementThreshold = 10; // pixels
let startX = 0;
let startY = 0;
let moved = false;

const handleButtonTouch = (event, callback) => {
  event.preventDefault();
  if (!isDragging.value && !moved) {
    callback();
  }
  moved = false;
};

const startDragging = event => {
  if (isMobile.value) return;

  isDragging.value = false;
  moved = false;
  event.preventDefault();

  const pos = event.type.startsWith('touch') ? event.touches[0] : event;

  dragOffset.value = {
    x: pos.clientX - toolbarPosition.value.x,
    y: pos.clientY - toolbarPosition.value.y,
  };

  startX = pos.clientX;
  startY = pos.clientY;

  document.addEventListener('mousemove', handleDragging);
  document.addEventListener('mouseup', stopDragging);
  document.addEventListener('touchmove', handleDragging, { passive: false });
  document.addEventListener('touchend', stopDragging);
};

const handleDragging = event => {
  const pos = event.type.startsWith('touch') ? event.touches[0] : event;
  const deltaX = pos.clientX - startX;
  const deltaY = pos.clientY - startY;
  const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

  if (distance > movementThreshold && !isDragging.value) {
    isDragging.value = true;
    moved = true;
  }

  if (isDragging.value) {
    event.preventDefault();

    toolbarPosition.value = {
      x: pos.clientX - dragOffset.value.x,
      y: pos.clientY - dragOffset.value.y,
    };
  }
};

const stopDragging = () => {
  isDragging.value = false;
  document.removeEventListener('mousemove', handleDragging);
  document.removeEventListener('mouseup', stopDragging);
  document.removeEventListener('touchmove', handleDragging);
  document.removeEventListener('touchend', stopDragging);
  moved = false;
};

onMounted(() => {
  coordinates.value = props.initialAnswer || [];
  document.addEventListener('fullscreenchange', handleFullScreenChange);

  isMobile.value = /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );

  console.log(toolbarPosition.value);
});

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullScreenChange);
  document.removeEventListener('mousemove', handleDragging);
  document.removeEventListener('mouseup', stopDragging);
  document.removeEventListener('touchmove', handleDragging);
  document.removeEventListener('touchend', stopDragging);
});
</script>

<style scoped>
.fullscreen-container {
  position: relative;
  width: 100%;
  overflow: visible; /* Ensure overflow is visible */
}

.fullscreen-container:fullscreen {
  background: white;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  overflow: visible; /* Ensure overflow is visible */
}

.fullscreen-container:fullscreen img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.toolbar-container {
  position: absolute; /* Changed from fixed to absolute */
  z-index: 9999;
  user-select: none;
  touch-action: none;
}

.toolbar {
  display: flex;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.5rem;
  border-radius: 9999px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  pointer-events: auto;
  touch-action: none;
}

.drag-handle {
  cursor: grab;
  touch-action: none;
  pointer-events: auto;
}

.drag-handle:active {
  cursor: grabbing;
}
</style>
