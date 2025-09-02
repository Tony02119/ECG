<script setup>
import {ref} from 'vue';
import {analyzeECG} from '@/services/apiService';
import Hero from "@/components/Hero.vue";
import {useRouter} from "vue-router";

import ecgGreen from '../assets/img/ecg_green_heart.png';
import ecgYellow from '../assets/img/ecg_yellow_heart.png';
import ecgRed from '../assets/img/ecg_red_heart.png';

const router = useRouter();

const selectedHeart = ref(null);  // Store the selected color (default null)
const modelChoice = ref('cnn');  // Store choice of model (default “cnn”)
const showOptions = ref(false);  // Variable to show or hide model options
const uploadedFile = ref(null);  // Variable for storing the uploaded file
const showTooltip = ref(false); // Variable for storing the visibility of the tooltip

const result = ref(null);  // Store the results returned by the API
const loading = ref(false);  // Load indicator
const error = ref(null);  // Store error messages

const heartOptions = {
  green: {
    img: ecgGreen,
    alt: 'Low Risk Heart',
    label: 'Low Risk'
  },
  yellow: {
    img: ecgYellow,
    alt: 'Mid Risk Heart',
    label: 'Mid Risk'
  },
  red: {
    img: ecgRed,
    alt: 'High Risk Heart',
    label: 'High Risk'
  }
}

// Function for displaying/hiding AI model options
const toggleOptions = () => {
  showOptions.value = !showOptions.value;
};

// Function for selecting the color by clicking on a heart
const selectHeart = (heartColor) => {
  selectedHeart.value = heartColor;
  uploadedFile.value = null;
};

// File upload management function
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file && file.name.endsWith('.csv')) {
    uploadedFile.value = file;
    selectedHeart.value = null;
    error.value = null;
  } else {
    uploadedFile.value = null;
    error.value = 'Please upload a valid CSV file.';
  }
};

// Function to analyze the ECG via the API
const analyze = async () => {
  if (!uploadedFile.value && !selectedHeart.value) {
    error.value = 'Please upload a CSV file or select a category.';
    return;
  }

  loading.value = true;
  error.value = null;
  result.value = null;

  const formData = new FormData();
  if (uploadedFile.value) formData.append('file', uploadedFile.value);
  formData.append('color_choice', selectedHeart.value);
  formData.append('model_choice', modelChoice.value);

  try {
    // API call with file and parameters
    const response = await analyzeECG(formData);

    // Redirect to the results page
    localStorage.setItem('diagnosisResults', JSON.stringify(response));
    await router.push({name: 'diagnostic-results'});
  } catch (err) {
    error.value = "Failed to analyze ECG. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <Hero/>

  <div class="w-full lg:w-3/4 xl:w-2/3 mx-auto px-8 space-y-6">
    <!-- Try it with section -->
    <div>
      <h1 class="text-3xl font-bold mb-2">Try it with</h1>
      <span class="text-sm text-gray-600 font-medium">These ECG are from physionet.org, click on one to try our program:</span>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <div
            v-for="(item, color) in heartOptions"
            :key="color"
            :class="['p-2 rounded border cursor-pointer flex flex-col items-center',
                   selectedHeart === color ? 'border-red-800' : 'border-gray-300']"
            @click="selectHeart(color)"
        >
          <img :src="item.img" :alt="item.alt" class="w-30 h-20"/>
          <span class="font-semibold mt-2">{{ item.label }}</span>
        </div>
      </div>
    </div>

    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-600 font-medium">Or try uploading your own ECG file:</span>

      <div class="relative">
        <button
            @click="toggleOptions"
            class="w-10 h-10 flex items-center justify-center bg-gray-200 rounded-full hover:bg-gray-300 transition"
        >
          <i class="fas fa-cog text-base"></i>
        </button>

        <div
            v-if="showOptions"
            class="absolute right-0 mt-2 bg-white border rounded p-4 shadow-lg z-20 "
        >
          <label for="model-choice" class="block mb-1 font-semibold">Model Choice</label>
          <span class="block mb-2 text-justify">Select the model you want to use for the ECG analysis.</span>
          <select
              id="model-choice"
              v-model="modelChoice"
              class="bg-white px-3 py-2 border rounded"
          >
            <option value="cnn">Convolutional Neural Networks (CNN)</option>
            <option value="deep">Deep Learning</option>
            <option value="rnn">Recurrent Neural Networks (RNN)</option>
            <option value="lstm">Long Short-Term Memory (LSTM)</option>
            <option value="gbm">Gradient Boosting Machines (GBM)</option>
            <option value="svm">Support Vector Machines (SVM)</option>
            <option value="rf">Random Forest</option>
            <option value="knn">K-Nearest Neighbors (KNN)</option>
          </select>
        </div>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-6 relative">
      <!-- File Upload -->
      <div class="relative w-full border-2 border-dashed border-red-600 rounded-lg p-6 h-48 flex flex-col justify-center items-center text-center bg-white">
        <span v-if="!uploadedFile" class="text-gray-500 mb-2">Drag and drop CSV files here or click to select.</span>
        <div v-else class="flex items-center mt-2">
          <img src="../assets/img/csv_icon.png" alt="CSV Icon" class="w-12 h-12 mr-3"/>
          <span>{{ uploadedFile.name }}</span>
        </div>

        <input
            type="file"
            @change="handleFileUpload"
            @drop="handleFileUpload"
            class="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
            accept=".csv"
        />
        <div class="absolute top-2 right-2 group">
          <i @click="() => showTooltip = !showTooltip" class="fas fa-info-circle text-blue-600"></i>
          <div
              class="absolute z-10 top-6 right-0 bg-white border p-2 rounded shadow-lg text-sm text-gray-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300 w-60"
              :class="[showTooltip ? 'opacity-100' : 'opacity-0']"
          >
            Please upload a CSV file. Other formats will be rejected.
            Visit the Help section to learn more.
          </div>
        </div>
      </div>
    </div>

    <!-- Error message -->
    <div v-if="error" class="text-center text-red-500 font-semibold mt-6">
      <span>{{ error }}</span>
    </div>

    <!-- Analyze button -->
    <div class="w-full flex justify-center">
      <button
          @click="analyze"
          :disabled="(!uploadedFile && !selectedHeart) || loading"
          class="px-6 py-4 bg-red-800 text-white rounded hover:bg-red-600 transition disabled:opacity-70"
      >
        Analyze ECG
      </button>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="text-center mt-6">
      <i class="fas fa-spinner fa-spin text-4xl text-red-800"></i>
      <p class="text-xl mt-4">Loading...</p>
    </div>

    <div class="items-center">
      <span class="block mb-12 font-semibold text-white bg-white">|</span>
    </div>
  </div>
</template>
