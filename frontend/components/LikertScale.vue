<template>
    <div>
      <p>{{ question.text }}</p>
      <div>
        <label
          v-for="point in scalePoints"
          :key="point"
          :for="`likert-${point}`"
        >
          <input
            type="radio"
            :id="`likert-${point}`"
            :value="point"
            v-model="selectedPoint"
          />
          {{ point }}
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['question'],
    data() {
      return {
        selectedPoint: null,
      };
    },
    computed: {
      scalePoints() {
        return this.question.scale === 5
          ? [1, 2, 3, 4, 5]
          : [1, 2, 3, 4, 5, 6, 7];
      },
    },
    watch: {
      selectedPoint(newVal) {
        this.$emit('answer', newVal);
      },
    },
  };
  </script>
  