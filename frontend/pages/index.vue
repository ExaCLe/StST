<template>
    <div>
      <h1>Welcome to the Survey Application</h1>
      <p>Choose an option below:</p>
      
      <ul>
        <li>
          <NuxtLink to="/surveys">Go to Surveys</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/admin/RequestResults">Admin: Request Results</NuxtLink>
        </li>
        <li>
          <NuxtLink to="/admin/UploadSurvey">Admin: Upload Survey</NuxtLink>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  // No script setup required for static links
  </script>
  
  <style scoped>
  h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 0.5rem;
  }
  </style>
  