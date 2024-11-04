<template>
    <div>
      <p>{{ question.text }}</p>
      <div v-for="(option, index) in question.options" :key="index">
        <input
          type="checkbox"
          :id="`option-${index}`"
          :value="option"
          v-model="selectedOptions"
        />
        <label :for="`option-${index}`">{{ option }}</label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['question'],
    data() {
      return {
        selectedOptions: [],
      };
    },
    watch: {
      selectedOptions(newVal) {
        this.$emit('answer', newVal);
      },
    },
  };
  </script>
  