<script setup>
import {diseasesInfo, getRiskColor, getRiskMessage} from "@/utils/diagnosticUtil.js";

defineProps({
  results: {
    type: Object,
    required: true,
    default: {},
  },
});

const mainCategories = [
  'Sinus Rhythm',
  'Supraventricular',
  'Potentially Dangerous',
  'Threatening VT',
  'Special Form TdP',
  'Dangerous VFL/VF',
];
</script>

<template>
  <div class="text-justify">
    <!-- Global Risk Level Section -->
    <div class="mt-8 relative">
      <div class="text-center">
        <h3 class="text-white font-semibold bg-red-800 hover:bg-red-600 px-8 py-2 rounded-lg inline-block mb-4">
          Global Risk
        </h3>
      </div>

      <div class="bg-gray-400 shadow-lg rounded-lg p-6">
        <!-- Risk header with percentage -->
        <div class="flex items-center justify-between">
          <p class="text-lg font-semibold">Total Risk Percentage</p>
          <span class="text-lg font-bold">{{ parseFloat(results.danger_level).toFixed(2) }}%</span>
        </div>

        <!-- Risk progress bar -->
        <div class="w-full bg-gray-200 rounded-full h-4 mt-2">
          <div
              class="h-4 rounded-full"
              :style="{ width: results.danger_level + '%', backgroundColor: getRiskColor(results.danger_level) }"
          ></div>
        </div>

        <!-- Risk message with tooltip -->
        <div class="flex items-center justify-between mt-4">
          <p class="text-base font-semibold">
            {{ getRiskMessage(results.danger_level) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Individual Disease Category Risks -->
    <div v-if="results" class="mt-6">
      <div class="text-center">
        <h3 class="text-white font-semibold bg-red-800 hover:bg-red-600 px-8 py-2 rounded-lg inline-block mb-4">
          Risk Levels
        </h3>
      </div>

      <div class="grid grid-cols-1 gap-4">
        <div
            v-for="category in mainCategories"
            :key="category"
            class="bg-gray-400 p-4 rounded-lg"
        >
          <h1 class="font-semibold">{{ category }}:</h1>
          <span>{{ diseasesInfo[category] }}</span>

          <!-- Progress bar -->
          <div class="w-full bg-gray-300 rounded-full h-4 mt-4">
            <div class="bg-red-800 h-4 rounded-full"
                 :style="{ width: Math.round(results.mainCategoryProbabilities[category]) + '%' }"
            ></div>
          </div>

          <!-- Percentage label -->
          <p class="text-right mt-2 font-bold">
            {{ Math.round(results.mainCategoryProbabilities[category]) }}%
          </p>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <p class="text-black text-center text-sm mt-8 mb-32">
      This is a demo and needs further medical and technological refinement to be medically applicable.
    </p>
  </div>
</template>
