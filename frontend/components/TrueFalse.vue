<template>
    <div>
      <p>{{ question.text }}</p>
      <div>
        <input
          type="radio"
          id="true"
          value="True"
          v-model="selectedOption"
        />
        <label for="true">True</label>
  
        <input
          type="radio"
          id="false"
          value="False"
          v-model="selectedOption"
        />
        <label for="false">False</label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['question'],
    data() {
      return {
        selectedOption: null,
      };
    },
    watch: {
      selectedOption(newVal) {
        this.$emit('answer', newVal);
      },
    },
  };
  </script>
  