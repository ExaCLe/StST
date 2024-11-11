<template>
  <div class="survey-creator bg-white p-6 rounded-lg shadow-lg">
    <div class="mb-6">
      <label for="admin-password" class="block text-sm font-medium text-gray-700 mb-2">Admin Password</label>
      <div class="relative">
        <input
          id="admin-password"
          v-model="formData.adminPassword"
          :type="showPassword ? 'text' : 'password'"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 pr-10"
          placeholder="Enter admin password"
        >
        <button 
          @click="togglePasswordVisibility" 
          type="button" 
          class="absolute inset-y-0 right-0 pr-3 flex items-center"
        >
          <UIcon :name="showPassword ? 'heroicons-outline:eye-off' : 'heroicons-outline:eye'" class="h-5 w-5 text-gray-400" />
        </button>
      </div>
    </div>
    
    <div class="mb-6">
      <label for="survey-title" class="block text-sm font-medium text-gray-700 mb-2">Survey Title</label>
      <input
        id="survey-title"
        v-model="formData.surveyTitle"
        type="text"
        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        placeholder="Enter survey title"
      >
    </div>

    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-700">Questions</h2>
      <TransitionGroup name="list" tag="ul" class="space-y-4">
        <li v-for="(question, index) in formData.questions" :key="question.id" class="bg-gray-50 p-4 rounded-md shadow">
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-lg font-medium text-gray-800">
              #{{ question.internal_id }} - {{ question.type }} Question
            </h3>
            <button @click="removeQuestion(index)" class="text-red-500 hover:text-red-700" title="Remove question">
              <UIcon name="heroicons-outline:trash" class="w-5 h-5" />
            </button>
          </div>
          <!-- Question Text Input -->
          <input
            v-if="question.type !== 'Header'"
            v-model="question.text"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 mb-2"
            placeholder="Enter question text"
          >
          <!-- Add this inside the question loop after the question text input -->
          <div v-if="showConditionOptions(index)" class="mt-2 p-2 bg-gray-100 rounded">
            <label class="block text-sm font-medium text-gray-700 mb-2">Condition</label>
            <div class="flex gap-2">
              <select
                v-model="question.condition.questionId"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">No condition</option>
                <option
                  v-for="q in getPreviousTrueFalseQuestions(index)"
                  :key="q.internal_id"
                  :value="q.internal_id"
                >
                  #{{q.internal_id}} - {{q.text}}
                </option>
              </select>
              <select
                v-if="question.condition.questionId"
                v-model="question.condition.expectedAnswer"
                class="w-24 px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="true">True</option>
                <option value="false">False</option>
              </select>
            </div>
          </div>
          <!-- Multiple Choice Options -->
          <div v-if="question.type === 'MultipleChoice'" class="mt-2">
            <div v-for="(option, optionIndex) in question.options" :key="optionIndex" class="flex items-center mb-2">
              <input
                v-model="question.options[optionIndex]"
                type="text"
                class="flex-grow px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Enter option"
              >
              <button @click="removeOption(question, optionIndex)" class="ml-2 text-red-500 hover:text-red-700" title="Remove option">
                <UIcon name="heroicons-outline:x" class="w-5 h-5" />
              </button>
            </div>
            <button @click="addOption(question)" class="text-indigo-600 hover:text-indigo-800 font-medium">
              Add Option
            </button>
          </div>
          <!-- Image Question Upload -->
          <div v-if="question.type === 'ImageQuestion'" class="mt-2">
            <div class="flex items-center justify-center w-full">
              <label class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                <div class="flex flex-col items-center justify-center pt-5 pb-6" v-if="!question.image">
                  <UIcon name="heroicons-outline:upload" class="w-10 h-10 mb-3 text-gray-400" />
                  <p class="mb-2 text-sm text-gray-500"><span class="font-semibold">Click to upload</span> or drag and drop</p>
                  <p class="text-xs text-gray-500">PNG, JPG or GIF (MAX. 800x400px)</p>
                </div>
                <div v-else class="relative w-full h-full">
                  <img :src="question.image" alt="Uploaded image" class="w-full h-full object-cover rounded-lg" />
                  <button @click.prevent="removeImage(question)" class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition duration-300">
                    <UIcon name="heroicons-outline:x" class="w-4 h-4" />
                  </button>
                </div>
                <input type="file" class="hidden" @change="handleImageUpload($event, question)" accept="image/*" />
              </label>
            </div>
          </div>
          <!-- Likert Scale Points -->
          <div v-if="question.type === 'LikertScale'" class="mt-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">Scale Points</label>
            <input
              v-model.number="question.scalePoints"
              type="number"
              min="2"
              max="10"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter number of scale points"
            >
          </div>
          <!-- For FreeAnswer and TrueFalse, no additional inputs needed -->
        </li>
      </TransitionGroup>
    </div>

    <div class="mb-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-700">Add New Question</h2>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="type in questionTypes"
          :key="type"
          @click="addQuestion(type)"
          class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition duration-300"
        >
          Add {{ type }}
        </button>
      </div>
    </div>

    <div class="flex justify-end">
      <button 
        @click="handleSubmit" 
        class="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition duration-300"
      >
        {{ submitButtonText }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';

const props = defineProps({
  initialData: {
    type: Object,
    required: true
  },
  submitButtonText: {
    type: String,
    default: 'Save Survey'
  },
  onSubmit: {
    type: Function,
    required: true
  }
});

const showPassword = ref(false);
const questionTypes = ['MultipleChoice', 'ImageQuestion', 'LikertScale', 'FreeAnswer', 'TrueFalse'];

// Add counter for internal IDs
const internalIdCounter = ref(1);

// Initialize counter and formData
onMounted(() => {
  // Find highest internal_id in existing questions
  const maxId = props.initialData.questions.reduce((max, q) => 
    q.internal_id ? Math.max(max, q.internal_id) : max, 0);
  internalIdCounter.value = maxId + 1;
});

const formData = reactive({
  adminPassword: props.initialData.adminPassword,
  surveyTitle: props.initialData.surveyTitle,
  questions: props.initialData.questions.map(q => ({
    ...q,
    internal_id: q.internal_id || 0, // Preserve existing IDs
    condition: q.condition || {
      questionId: '',
      expectedAnswer: 'true'
    }
  }))
});

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const addQuestion = (type) => {
  const question = {
    id: Date.now(),
    type,
    text: '',
    internal_id: internalIdCounter.value,
    condition: {
      questionId: '',
      expectedAnswer: 'true'
    }
  };
  
  if (type === 'MultipleChoice') {
    question.options = [''];
  } else if (type === 'ImageQuestion') {
    question.image = null;
    question.imageName = '';
  } else if (type === 'LikertScale') {
    question.scalePoints = 5;
  }
  
  formData.questions.push(question);
  internalIdCounter.value++;
};

const removeQuestion = (index) => {
  formData.questions.splice(index, 1);
};

const addOption = (question) => {
  question.options.push('');
};

const removeOption = (question, index) => {
  question.options.splice(index, 1);
};

const handleImageUpload = (event, question) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = (e) => {
    question.image = e.target.result;
    question.imageName = file.name; // Make sure to set the imageName
  };
  reader.readAsDataURL(file);
};

const removeImage = (question) => {
  question.image = null;
  question.imageName = '';
};

const handleSubmit = () => {
  if (!formData.adminPassword || !formData.surveyTitle || formData.questions.length === 0) {
    alert('Admin password, survey title, and at least one question are required');
    return;
  }

  // Sanitize questions before submitting
  const sanitizedQuestions = formData.questions.map(q => {
    const question = {
      text: q.text,
      type: q.type,
      condition: {
        questionId: q.condition.questionId || null,
        expectedAnswer: q.condition.expectedAnswer
      }
    };
    
    if (q.type === 'MultipleChoice') {
      question.options = q.options;
    } else if (q.type === 'ImageQuestion') {
      question.imageName = q.imageName;
      // Only include image data if it's a new or modified image (starts with data:image)
      if (q.image && q.image.startsWith('data:image')) {
        question.image = q.image;
      }
    } else if (q.type === 'LikertScale') {
      question.scale_points = parseInt(q.scalePoints) || 5;
    }
    return question;
  });

  props.onSubmit({
    ...formData,
    questions: sanitizedQuestions
  });
};

const showConditionOptions = (index) => {
  // Only show conditions for non-first questions that are not Headers
  return index > 0 && formData.questions[index].type !== 'Header';
};

const getPreviousTrueFalseQuestions = (currentIndex) => {
  return formData.questions
    .slice(0, currentIndex)
    .filter(q => q.type === 'TrueFalse')
    .map(q => ({ 
      ...q, 
      displayIndex: q.internal_id || formData.questions.indexOf(q) + 1 
    }));
};
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
