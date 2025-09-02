<script setup>
import { getDiseaseDescription, getRiskColor, getRiskMessage } from "@/utils/diagnosticUtil.js";

defineProps({
  results: {
    type: Object,
    required: true,
    default: {},
  },
});
</script>

<template>
  <div class="text-justify">
    <!-- ECG Signal Display -->
    <div class="mt-8 relative">
      <div class="text-center">
        <h3 class="text-white font-semibold bg-red-800 hover:bg-red-600 px-6 py-2 rounded-lg inline-block mb-4">
          ECG Signal
        </h3>
      </div>
      <div class="bg-gray-400 shadow-lg rounded-lg p-4 sm:p-6 mx-4">
        <img
            :src="`data:image/png;base64,${results.ecg_plot_base64}`"
            alt="ECG Signal"
            class="mx-auto rounded-lg w-full max-w-3xl"
        />
      </div>
    </div>

    <!-- Top 3 Predictions Table -->
    <div class="text-center">
      <h3 class="text-white font-semibold bg-red-800 hover:bg-red-600 px-6 py-2 rounded-lg inline-block mt-8 mb-4">
        Top 3 Predictions
      </h3>
    </div>
    <div class="overflow-x-auto mx-4">
      <table class="w-full table-auto border-collapse border border-gray-300 shadow-lg text-sm sm:text-base">
        <thead>
        <tr class="bg-gray-400">
          <th class="px-4 py-2 border border-black border-opacity-40">Rank</th>
          <th class="px-4 py-2 border border-black border-opacity-40">Class</th>
          <th class="px-4 py-2 border border-black border-opacity-40">Risk</th>
          <th class="px-4 py-2 border border-black border-opacity-40">Description</th>
        </tr>
        </thead>
        <tbody class="bg-gray-300 font-semibold">
        <tr v-for="(item, index) in results.top3Predictions" :key="index">
          <td class="px-4 py-2 border border-black border-opacity-40">
            {{ index === 0 ? '1st' : index === 1 ? '2nd' : '3rd' }}
          </td>
          <td class="px-4 py-2 border border-black border-opacity-40">{{ item.name }}</td>
          <td class="px-4 py-2 border border-black border-opacity-40">{{ item.percentage }}%</td>
          <td class="px-4 py-2 border border-black border-opacity-40 text-sm text-left">
            {{ getDiseaseDescription(item.name) }}
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Global Risk Section -->
    <div class="mt-8 relative px-4">
      <div class="text-center">
        <h3 class="text-white font-semibold bg-red-800 hover:bg-red-600 px-6 py-2 rounded-lg inline-block mb-4">
          Global Risk
        </h3>
      </div>

      <div class="bg-gray-400 shadow-lg rounded-lg p-6">
        <!-- Header with total risk -->
        <div class="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center gap-2">
          <p class="text-lg font-semibold">Total Risk Percentage</p>
          <span class="text-lg font-bold">{{ parseFloat(results.danger_level).toFixed(2) }}%</span>
        </div>

        <!-- Progress bar -->
        <div class="w-full bg-gray-200 rounded-full h-4 mt-2">
          <div
              class="h-4 rounded-full"
              :style="{ width: results.danger_level + '%', backgroundColor: getRiskColor(results.danger_level) }"
          ></div>
        </div>

        <!-- Risk message -->
        <div class="mt-4">
          <p class="text-base font-semibold">
            {{ getRiskMessage(results.danger_level) }}
          </p>
        </div>
      </div>
    </div>

    <!-- All Class Risk Probabilities -->
    <div class="text-center">
      <h3 class="text-white font-semibold bg-red-800 hover:bg-red-600 px-6 py-2 rounded-lg inline-block mt-6 mb-4">
        Risk Levels
      </h3>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 px-4">
      <div
          v-for="(disease, index) in results.diagnosisResults"
          :key="index"
          class="bg-gray-400 shadow-lg rounded-lg p-6"
      >
        <div class="flex justify-between items-start">
          <p class="text-lg font-semibold">{{ disease.name }}</p>
          <span class="text-lg font-bold">{{ disease.percentage }}%</span>
        </div>
        <p class="text-sm text-gray-800 mt-1">
          {{ disease.info }}
        </p>
        <div class="w-full bg-gray-200 rounded-full h-4 mt-2">
          <div class="bg-red-800 h-4 rounded-full" :style="{ width: disease.percentage + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <p class="text-black text-center text-sm mt-6 mb-24">
      This is a demo and needs further medical and technological refinement to be medically applicable.
    </p>
  </div>
</template>
