<template>
  <div>
    <p>{{ question.text }}</p>
    <div
      v-for="(image, index) in question.images"
      :key="index"
      @click="handleClick"
      class="image-container"
    >
      <img :src="'data:image/png;base64,' + image.data" :alt="image.name" />
      <div
        v-for="(coord, coordIndex) in coordinates"
        :key="coordIndex"
        :style="{
          top: `${coord.y}px`,
          left: `${coord.x}px`,
        }"
        class="dot"
      ></div>
    </div>
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
