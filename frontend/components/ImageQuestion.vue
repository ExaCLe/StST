<template>
  <div>
    <p>{{ question.text }}</p>
    <div
      v-for="(image, index) in question.images"
      :key="index"
      ref="imageContainer"
      @click="handleClick"
      style="position: relative; display: inline-block;"
    >
      <img :src="'data:image/png;base64,' + image.data" :alt="image.name" />
      <div
        v-for="(coord, index) in coordinates"
        :key="index"
        :style="{
          position: 'absolute',
          top: coord.y + 'px',
          left: coord.x + 'px',
          width: '10px',
          height: '10px',
          backgroundColor: 'red',
          borderRadius: '50%',
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps(['question']);
const emit = defineEmits(['answer']);

const coordinates = ref([]);

const handleClick = (event) => {
  // Get the position of the image container
  const rect = event.currentTarget.getBoundingClientRect();
  
  // Calculate the click position relative to the image
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  
  // Save the coordinates
  coordinates.value.push({ x, y });

  // Optionally emit the answer if you want to send the coordinates to the parent component
  emit('answer', coordinates.value);
};

const imageContainer = ref(null);
</script>
