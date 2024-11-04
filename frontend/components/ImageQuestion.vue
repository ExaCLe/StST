<template>
    <div>
      <p>{{ question.text }}</p>
      <div
        ref="imageContainer"
        @click="handleClick"
        style="position: relative; display: inline-block;"
      >
        <img :src="imageUrl" alt="Question Image" />
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
  
  <script>
  export default {
    props: ['question'],
    data() {
      return {
        coordinates: [],
      };
    },
    computed: {
      imageUrl() {
        return `${process.env.BACKEND_URL}/images/${this.question.imageName}`;
      },
    },
    methods: {
      handleClick(event) {
        const rect = this.$refs.imageContainer.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        this.coordinates.push({ x, y });
        this.$emit('answer', this.coordinates);
      },
    },
  };
  </script>
  