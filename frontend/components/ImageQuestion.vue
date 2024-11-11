<template>
  <div class="image-question">
    <h2 class="text-xl font-semibold mb-4">{{ question.text }}</h2>
    <!-- Separate image container for fullscreen -->
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
        v-for="(marker, index) in displayCoordinates"
        :key="index"
        class="absolute transform"
        :style="{
          left: `calc(${marker.x}px + ${offset.left}px - 12px)`,
          top: `calc(${marker.y}px + ${offset.top}px - 24px)`
        }"
        @click.stop="handleMarkerClick(index)"
      >
        <MapPin :class="`w-6 h-6 text-${marker.color}-500`" />
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
            class="bg-green-500 text-white p-2 rounded-full transition duration-300 tooltip-button"
            :class="{
              'ring-2 ring-offset-2 ring-green-500': currentTool === 'stamp',
              'hover:bg-green-600': hasAvailableColors,
              'opacity-50 cursor-not-allowed': !hasAvailableColors
            }"
            :disabled="!hasAvailableColors"
            :data-tooltip="hasAvailableColors ? 'Markierung hinzufügen' : 'Bitte entfernen Sie eine bestehende Markierung, um eine neue hinzuzufügen'"
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
            class="bg-green-500 text-white p-2 rounded-full transition duration-300 tooltip-button"
            :class="{
              'ring-2 ring-offset-2 ring-green-500': currentTool === 'stamp',
              'hover:bg-green-600': hasAvailableColors,
              'opacity-50 cursor-not-allowed': !hasAvailableColors
            }"
            :disabled="!hasAvailableColors"
            :data-tooltip="hasAvailableColors ? 'Markierung hinzufügen' : 'Bitte entfernen Sie eine bestehende Markierung, um eine neue hinzuzufügen'"
          >
            <MapPin class="w-5 h-5" />
          </button>
          <button
            @click.stop="setTool('eraser')"
            @touchend.stop.prevent="handleButtonTouch($event, () => setTool('eraser'))"
            class="bg-yellow-500 text-white p-2 mr-2 ml-2 rounded-full hover:bg-yellow-600 transition duration-300"
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

    <!-- Marker list moved outside fullscreen container -->
    <div class="mt-4 space-y-4">
      <div v-for="(marker, index) in coordinates" :key="marker.id" 
           class="flex items-start space-x-3 bg-white p-3 rounded-lg shadow-sm">
        <div class="flex-shrink-0 mt-1">
          <MapPin :class="`w-5 h-5 text-${marker.colorClass}-500`" />
        </div>
        <div class="flex-grow">
          <textarea
            v-model="marker.text"
            :placeholder="getPlaceholder(index)"
            class="w-full min-h-[80px] border rounded-md px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            @input="emitAnswer"
          ></textarea>
        </div>
        <button
          @click="removeMarker(index)"
          class="flex-shrink-0 text-red-500 hover:text-red-700 mt-1"
          title="Markierung entfernen"
        >
          <Trash2 class="w-5 h-5" />
        </button>
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

let nextMarkerId = 0;

const availableColors = [
  { name: 'blaue', class: 'blue' },    // #3B82F6
  { name: 'rote', class: 'red' },      // #EF4444
  { name: 'grüne', class: 'green' },   // #22C55E
  { name: 'lila', class: 'purple' },  // #9333EA
  { name: 'pinke', class: 'pink' },    // #EC4899
  { name: 'gelbe', class: 'yellow' },  // #EAB308
];

const displayCoordinates = computed(() => {
  fullscreenTrigger.value;
  if (!imageRef.value) return [];

  return coordinates.value.map(coord => ({
    x: (coord.x / originalImageDimensions.value.width) * currentImageWidth.value,
    y: (coord.y / originalImageDimensions.value.height) * currentImageHeight.value,
    color: coord.colorClass,
    text: coord.text
  }));
});

const hasAvailableColors = computed(() => {
  return availableColors.some(color => 
    !coordinates.value.some(marker => marker.colorClass === color.class)
  );
});

const handleImageLoad = async () => {
  const img = imageRef.value;
  originalImageDimensions.value = {
    width: img.naturalWidth,
    height: img.naturalHeight,
  };
  imageAspectRatio.value = originalImageDimensions.value.width / originalImageDimensions.value.height;
  calculateCurrentImageHeightAndWidth();

  await nextTick();

  if (!isMobile.value) {
    // Positions relative to the container
    setToolbarPosition();
  }
};

const setToolbarPosition = () => {
  if (isFullScreen.value) {
    // Position toolbar in fullscreen mode
    toolbarPosition.value = {
      x: (currentImageWidth.value / 2) - (toolbarRef.value.offsetWidth / 2),
      y: currentImageHeight.value + 10, // 10px below the image
    };
  } else {
    // Positions relative to the container
    const imageOffsetLeft = imageRef.value.offsetLeft;
    const imageOffsetTop = imageRef.value.offsetTop;

    toolbarPosition.value = {
      x: imageOffsetLeft + (imageRef.value.offsetWidth / 2) - (toolbarRef.value.offsetWidth / 2),
      y: imageOffsetTop + imageRef.value.offsetHeight + 10, // 10px below the image
    };
  }
};

const handleClick = event => {
  if (currentTool.value !== 'stamp') return;
  
  // Check all colors, including previously used ones that are now available
  const availableColor = availableColors.find(color => {
    const isUsed = coordinates.value.some(marker => marker.colorClass === color.class);
    return !isUsed;
  });
  
  if (!availableColor) return; // No colors left
  
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
      coordinates.value.push({ 
        id: nextMarkerId++,
        x, 
        y, 
        text: '',
        colorClass: availableColor.class,
        colorName: availableColor.name
      });
      emitAnswer();
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
      coordinates.value.push({ 
        id: nextMarkerId++,
        x, 
        y, 
        text: '',
        colorClass: availableColor.class,
        colorName: availableColor.name
      });
      emitAnswer();
    }
  }
};

const setTool = tool => {
  currentTool.value = tool;
};

const removeMarker = index => {
  if (currentTool.value === 'eraser' || currentTool.value === 'stamp') {
    const marker = coordinates.value[index];
    coordinates.value.splice(index, 1);
    emitAnswer();
  }
};

const clearAllMarkers = () => {
  coordinates.value = [];
  emitAnswer();
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

const handleFullScreenChange = async () => {
  isFullScreen.value = !!document.fullscreenElement;
  document.body.classList.toggle('fullscreen-mode', isFullScreen.value);

  if (isFullScreen.value) {
    offset.value = { top: 0, left: 0 };
  }

  setTimeout(async () => {
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

    // Reset toolbar position
    await nextTick();
    if (!isMobile.value) {
      setToolbarPosition();
    }
  }, 100);
};

const toolbarRef = ref(null);
const toolbarPosition = ref({ x: 0, y: 0 });
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

  const containerRect = imageContainer.value.getBoundingClientRect();

  dragOffset.value = {
    x: pos.clientX - toolbarPosition.value.x - containerRect.left,
    y: pos.clientY - toolbarPosition.value.y - containerRect.top,
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

    const containerRect = imageContainer.value.getBoundingClientRect();

    toolbarPosition.value = {
      x: pos.clientX - dragOffset.value.x - containerRect.left,
      y: pos.clientY - dragOffset.value.y - containerRect.top,
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

const emitAnswer = () => {
  emit('answer', coordinates.value.map(coord => ({
    x: coord.x,
    y: coord.y,
    color: coord.colorClass,
    text: coord.text
  })));
};

const getPlaceholder = (index) => {
  if (props.question.markerLabels?.[index]) {
    return props.question.markerLabels[index];
  }
  return `Notizen für ${coordinates.value[index].colorName} Markierung`;
};

const handleMarkerClick = (index) => {
  if (currentTool.value === 'eraser') {
    coordinates.value.splice(index, 1);
    emitAnswer();
  }
};

onMounted(() => {
  if (props.initialAnswer) {
    nextMarkerId = props.initialAnswer.length;
    coordinates.value = props.initialAnswer.map((answer, index) => ({
      id: index,
      x: answer.x,
      y: answer.y,
      text: answer.text,
      colorClass: answer.color,
      colorName: availableColors.find(c => c.class === answer.color)?.name
    }));
  } else {
    coordinates.value = [];
  }
  document.addEventListener('fullscreenchange', handleFullScreenChange);

  isMobile.value = /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
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
  overflow: visible;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fullscreen-container:fullscreen {
  background: white;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  overflow: hidden;
}

.fullscreen-container:fullscreen img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.toolbar-container {
  position: absolute;
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

/* Remove the marker-label class since we're not using it anymore */
.marker-label {
  display: none;
}

/* Add styles for textarea */
textarea {
  resize: vertical;
  min-height: 80px;
  font-size: 0.875rem;
  line-height: 1.5;
}

button[disabled] {
  pointer-events: auto !important; /* Enable hover for tooltip */
}

.tooltip-button {
  position: relative;
}

.tooltip-button::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding: 4px 8px;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  font-size: 12px;
  white-space: nowrap;
  border-radius: 4px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.1s ease;
  pointer-events: none;
  margin-bottom: 5px;
}

.tooltip-button:hover::after {
  opacity: 1;
  visibility: visible;
}
</style>
