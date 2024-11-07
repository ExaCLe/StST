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
          left: `calc(${coord.x}px + ${offset.left}px)`,
          top: `calc(${coord.y}px + ${offset.top}px)`
        }"
        class="absolute w-4 h-4 bg-red-500 rounded-full transform -translate-x-1/2 -translate-y-1/2"
        @click="removeMarker(index)"
      ></div>
      <div 
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
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
const offset = ref({top: 0, left: 0})
const fullscreenTrigger = ref(0)
const imageAspectRatio = ref(0)
const screenAspectRatio = ref(0)
const currentImageWidth = ref(0)
const currentImageHeight = ref(0)

const displayCoordinates = computed(() => {
  fullscreenTrigger.value // Trigger reactivity
  if (!imageRef.value) return [];
  
  return coordinates.value.map(coord => ({
    x: (coord.x / originalImageDimensions.value.width) * currentImageWidth.value,
    y: (coord.y / originalImageDimensions.value.height) * currentImageHeight.value,
  }));
});

const handleImageLoad = () => {
  const img = imageRef.value;
  originalImageDimensions.value = {
    width: img.naturalWidth,
    height: img.naturalHeight
  };
  imageAspectRatio.value = originalImageDimensions.value.width / originalImageDimensions.value.height
  calculateCurrentImageHeightAndWidth()
};

const handleClick = (event) => {
  if (currentTool.value !== 'stamp') return;
  
  const rect = imageRef.value.getBoundingClientRect();
  
  if (!isFullScreen.value){
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
  } else {

    // calculate if click is within image bounds
    if (event.clientX < offset.value.left || event.clientX > offset.value.left + currentImageWidth.value || 
        event.clientY < offset.value.top || event.clientY > offset.value.top + currentImageHeight.value) {
      return
    }

    // Calculate relative position within the image
    const relativeX = event.clientX - offset.value.left;
    const relativeY = event.clientY - offset.value.top;

    // Convert to percentage of original image dimensions
    const x = Math.round((relativeX / currentImageWidth.value) * originalImageDimensions.value.width);
    const y = Math.round((relativeY / currentImageHeight.value) * originalImageDimensions.value.height);

    // Only add marker if within image bounds
    if (x >= 0 && x <= originalImageDimensions.value.width && 
        y >= 0 && y <= originalImageDimensions.value.height) {
      coordinates.value.push({ x, y });
      emit('answer', coordinates.value);
    }

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

const calculateCurrentImageHeightAndWidth = () => {
  const rect = imageRef.value.getBoundingClientRect()
  if (!isFullScreen.value) {
    currentImageHeight.value = rect.height 
    currentImageWidth.value = rect.width
    return 
  }

  screenAspectRatio.value = rect.width / rect.height
  if (screenAspectRatio.value > imageAspectRatio.value) { // image takes full height, but not full width
    currentImageWidth.value = rect.height * imageAspectRatio.value
    currentImageHeight.value = rect.height
  } else { // image takes full width but not full height 
    currentImageHeight.value = rect.width / imageAspectRatio.value
    currentImageWidth.value = rect.width
  } 
  fullscreenTrigger.value++
}

const handleFullScreenChange = () => {
  isFullScreen.value = !!document.fullscreenElement;
  document.body.classList.toggle('fullscreen-mode', isFullScreen.value);

  // Reset offsets in fullscreen mode
  if (isFullScreen.value) {
    offset.value = { top: 0, left: 0 };
  }

  setTimeout(() => {
    calculateCurrentImageHeightAndWidth()
    const rect = imageRef.value.getBoundingClientRect()
    if (isFullScreen.value) {
      if (screenAspectRatio.value > imageAspectRatio.value) { // image takes full height, but not full width
        offset.value.top = 0
        offset.value.left = (rect.width - currentImageWidth.value) / 2 
      } else { // image takes full width but not full height 
        offset.value.left = 0
        offset.value.top = (rect.height - currentImageHeight.value) / 2
      }
    } else {
      offset.value = {top: 0, left: 0}
    }
  }, 100) // Small delay to ensure transition completed
};

const toolbarRef = ref(null);
const toolbarPosition = ref({ x: 20, y: 20 });
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

const startDragging = (event) => {
  isDragging.value = true;
  event.preventDefault();

  const pos = event.type.startsWith('touch') ? event.touches[0] : event;
  const rect = toolbarRef.value.getBoundingClientRect();

  dragOffset.value = {
    x: pos.clientX - rect.left,
    y: pos.clientY - rect.top,
  };

  document.addEventListener('mousemove', handleDragging);
  document.addEventListener('mouseup', stopDragging);
  document.addEventListener('touchmove', handleDragging);
  document.addEventListener('touchend', stopDragging);
};

const handleDragging = (event) => {
  if (!isDragging.value) return;
  event.preventDefault();

  const pos = event.type.startsWith('touch') ? event.touches[0] : event;

  const newX = pos.clientX - dragOffset.value.x;
  const newY = pos.clientY - dragOffset.value.y;

  // Constrain to viewport
  const toolbar = toolbarRef.value;
  const maxX = window.innerWidth - toolbar.offsetWidth;
  const maxY = window.innerHeight - toolbar.offsetHeight;

  toolbarPosition.value = {
    x: Math.min(Math.max(0, newX), maxX),
    y: Math.min(Math.max(0, newY), maxY),
  };
};

const stopDragging = () => {
  isDragging.value = false;
  document.removeEventListener('mousemove', handleDragging);
  document.removeEventListener('mouseup', stopDragging);
  document.removeEventListener('touchmove', handleDragging);
  document.removeEventListener('touchend', stopDragging);
};

onMounted(() => {
  coordinates.value = props.initialAnswer || [];
  document.addEventListener('fullscreenchange', handleFullScreenChange);

  // move the toolbar below the image
  const rect = imageContainer.value.getBoundingClientRect();
  toolbarPosition.value = {
    x: rect.x + rect.width / 2 - toolbarRef.value.offsetWidth / 2,
    y: rect.y + rect.height - 10,
  };
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
}

.fullscreen-container:fullscreen {
  background: white;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.fullscreen-container:fullscreen img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.toolbar-container {
  position: fixed;
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
