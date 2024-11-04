<template>
    <div>
      <p>{{ question.text }}</p>
      <textarea v-model="answer" @input="emitAnswer"></textarea>
    </div>
  </template>
  
  <script>
  export default {
    props: ['question'],
    data() {
      return {
        answer: '',
      };
    },
    methods: {
      emitAnswer() {
        this.$emit('answer', this.answer);
      },
    },
  };
  </script>
  