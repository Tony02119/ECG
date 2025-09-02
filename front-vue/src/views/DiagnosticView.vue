<script setup>
import {onMounted, ref} from "vue";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import {useRouter} from "vue-router";
import Hero from "@/components/Hero.vue";
import SimpleDiagnostic from "@/components/SimpleDiagnostic.vue";
import AdvancedDiagnostic from "@/components/AdvancedDiagnostic.vue";
import {diseasesInfo, getRiskMessage} from "@/utils/diagnosticUtil.js";

const router = useRouter();

const simpleView = ref(true);
const showDropdown = ref(false);
const top3Predictions = ref([]);  // Store the first 3 predictions
const diagnosisResults = ref([]);  // Store results for all classes
const mainCategoryProbabilities = ref({
  'Sinus Rhythm': 0,
  'Supraventricular': 0,
  'Potentially Dangerous': 0,
  'Threatening VT': 0,
  'Special Form TdP': 0,
  'Dangerous VFL/VF': 0
});
const results = ref(null);

// Class names for display
const classNames = [
  "AFIB", "B", "BBB", "BI", "HGEA", "N", "NOD", "Ne", "SBR", "SVTA", "VER", "VF", "VFL", "VTHR", "VTLR", "VTTdP"
];

// Retrieving results from localStorage
onMounted(() => {
  const diagnosisResultsStorage = JSON.parse(localStorage.getItem('diagnosisResults'));
  if (diagnosisResultsStorage) {
    // Fill in the top 3 predictions
    top3Predictions.value = diagnosisResultsStorage.top_3_classes.map((className, index) => ({
      name: className,
      percentage: (diagnosisResultsStorage.top_3_probabilities[index] * 100).toFixed(2)
    }));

    // Fill in results by class
    diagnosisResults.value = diagnosisResultsStorage.class_probabilities.map((probability, index) => ({
      name: classNames[index],
      percentage: (probability * 100).toFixed(2),
      info: diseasesInfo[classNames[index]]
    }));

    // Update the probabilities of the 6 main classes
    mainCategoryProbabilities.value = diagnosisResultsStorage.main_category_probabilities;

    diagnosisResultsStorage.mainCategoryProbabilities = mainCategoryProbabilities;
    diagnosisResultsStorage.top3Predictions = top3Predictions;
    diagnosisResultsStorage.diagnosisResults = diagnosisResults;
    results.value = diagnosisResultsStorage;
  } else {
    router.push({name: 'home'}); // Redirect if no results
  }
});

const toggleView = () => {
  simpleView.value = !simpleView.value;
};

const retry = () => {
  router.push({name: 'home'});
}

// Function to download results in PDF format
const downloadPDF = () => {
  const doc = new jsPDF();

  // Add title and results
  doc.setFontSize(18);
  doc.text("Diagnosis Results", 14, 20);

  // Add overall risk level
  doc.setFontSize(12);
  doc.text(`Global Risk Level: ${parseFloat(results.value.danger_level).toFixed(2)}%`, 14, 30);

  // Add the message associated with the risk level
  const riskMessage = getRiskMessage(results.value.danger_level);
  doc.text(`Risk Message: ${riskMessage}`, 14, 36);

  // Add ECG trace image
  if (results.value.ecg_plot_base64) {
    // Convert base64 to image
    const imgData = `data:image/png;base64,${results.value.ecg_plot_base64}`;
    // Adjust image size if necessary
    doc.addImage(imgData, 'PNG', 14, 42, 180, 90); // x, y, largeur, hauteur
  }

  // Vertical position after image
  let currentY = results.value.ecg_plot_base64 ? 140 : 42;

  // Add the probabilities of the 6 main classes
  doc.setFontSize(14);
  doc.text("Main Categories Probabilities:", 14, currentY);
  currentY += 6;

  const mainCategories = Object.keys(mainCategoryProbabilities.value);
  const mainCategoriesData = mainCategories.map(category => [
    category,
    `${parseFloat(mainCategoryProbabilities.value[category]).toFixed(2)}%`
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Category', 'Probability']],
    body: mainCategoriesData,
    theme: 'grid',
    margin: {left: 14, right: 14},
    styles: {fontSize: 12},
  });

  currentY = doc.lastAutoTable.finalY + 10;

  // Add Top 3 Predictions
  doc.setFontSize(14);
  doc.text("Top 3 Predictions:", 14, currentY);
  currentY += 6;

  const top3Data = top3Predictions.value.map((prediction, index) => [
    `${index + 1}`,
    prediction.name,
    `${prediction.percentage}%`
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Rank', 'Class', 'Probability']],
    body: top3Data,
    theme: 'grid',
    margin: {left: 14, right: 14},
    styles: {fontSize: 12},
  });

  currentY = doc.lastAutoTable.finalY + 10;

  // Add detailed probabilities for all classes
  doc.setFontSize(14);
  doc.text("Detailed Class Probabilities:", 14, currentY);
  currentY += 6;

  const detailedData = diagnosisResults.value.map(disease => [
    disease.name,
    `${disease.percentage}%`,
    disease.info
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Class', 'Probability', 'Description']],
    body: detailedData,
    theme: 'grid',
    margin: {left: 14, right: 14},
    styles: {fontSize: 10},
    columnStyles: {
      2: {cellWidth: 60} // Adjust column width Description
    },
  });

  // Generate and download the PDF file
  doc.save('ecg_results.pdf');
};

// Function to download results as a CSV file
const downloadCSV = () => {
  if (!results.value) return;
  const rows = [];

  // Add main diagnostic information
  rows.push(["Diagnosis Results"]);
  rows.push(["Global Risk Level", parseFloat(results.value.danger_level).toFixed(2) + "%"]);
  rows.push(["Risk Message", getRiskMessage(results.value.danger_level)]);
  rows.push([]);

  // Add the probabilities of the 6 main classes
  rows.push(["Main Categories Probabilities"]);
  rows.push(["Category", "Probability"]);
  const mainCategories = Object.keys(mainCategoryProbabilities.value);
  mainCategories.forEach(category => {
    rows.push([category, `${parseFloat(mainCategoryProbabilities.value[category]).toFixed(2)}%`]);
  });
  rows.push([]);

  // Add the 3 best predictions
  rows.push(["Top 3 Predictions"]);
  rows.push(["Rank", "Class", "Probability"]);
  top3Predictions.value.forEach((prediction, index) => {
    rows.push([`${index + 1}`, prediction.name, `${prediction.percentage}%`]);
  });
  rows.push([]);

  // Add detailed probabilities for all classes
  rows.push(["Detailed Class Probabilities"]);
  rows.push(["Class", "Probability", "Description"]);
  diagnosisResults.value.forEach(disease => {
    // Escape line breaks and commas in descriptions
    const description = disease.info.replace(/(\r\n|\n|\r)/gm, " ").replace(/,/g, ";");
    rows.push([disease.name, `${disease.percentage}%`, description]);
  });
  rows.push([]);

  // Add additional information (e.g. size of data analyzed, analysis time, etc.).
  rows.push(["Additional Information"]);
  if (results.value.analysis_time) {
    rows.push(["Analysis Time", `${results.value.analysis_time} seconds`]);
  }
  if (results.value.data_size) {
    rows.push(["Data Size", `${results.value.data_size} data points`]);
  }
  rows.push([]);

  // Add a Disclaimer section if needed
  rows.push(["Disclaimer"]);
  rows.push([diseasesInfo['Disclaimer']]);

  // Generate the CSV content
  let csvContent = "data:text/csv;charset=utf-8,"
      + rows.map(e => e.join(",")).join("\n");

  // Download the CSV file
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "ecg_results.csv");
  document.body.appendChild(link);
  link.click();
  link.parentNode.removeChild(link);
};

// Function to toggle the drop-down menu display
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};
</script>

<template>
  <Hero />
  <div class="w-full px-8 xl:w-3/4 mx-auto">
    <div class="py-4 sm:py-8 mx-auto relative">
      <div class="flex flex-wrap items-center justify-between gap-4">

        <!-- Download buttons -->
        <div class="relative inline-block text-left">
          <div class="relative group inline-block">
            <button @click="toggleDropdown"
                    class="flex items-center gap-2 bg-red-800 text-white px-3 py-2 sm:px-4 sm:py-3 rounded shadow hover:bg-red-600 transition text-sm sm:text-base">
              <i class="fas fa-download"></i>
              <i class="fas fa-chevron-right"></i>
            </button>
            <div
                class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 absolute left-1/2 transform -translate-x-1/2 bottom-full mb-2 w-40 bg-red-700 text-white text-xs sm:text-sm rounded-md p-2 text-center z-40">
              Download Results
            </div>
          </div>

          <!-- Dropdown -->
          <div v-if="showDropdown"
               class="z-50 origin-top-left absolute top-12 left-0 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
            <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
              <a
                  @click="downloadPDF"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 cursor-pointer"
              >
                <i class="fas fa-file-pdf mr-2"></i> Download PDF
              </a>
              <a
                  @click="downloadCSV"
                  class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 cursor-pointer"
              >
                <i class="fas fa-file-csv mr-2"></i> Download CSV
              </a>
            </div>
          </div>
        </div>

        <!-- Title -->
        <h2 class="flex-1 text-center text-xl sm:text-3xl font-extrabold tracking-wide text-black">
          Diagnosis Results
        </h2>

        <div class="flex items-center gap-2">

          <!-- Toggle view -->
          <div class="relative group inline-block">
            <button @click="toggleView"
                    class="bg-red-800 text-white p-2 sm:p-3 rounded shadow hover:bg-red-600 transition text-sm sm:text-base">
              <i class="fas fa-exchange-alt"></i>
            </button>
            <div
                class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 absolute left-1/2 transform -translate-x-1/2 bottom-full mb-2 w-44 bg-red-700 text-white text-xs sm:text-sm rounded-md p-2 text-center z-40">
              Simple / Advanced View
            </div>
          </div>

          <!-- Retry -->
          <div class="relative group inline-block">
            <button
                @click="retry"
                class="bg-red-800 text-white p-2 sm:p-3 rounded shadow hover:bg-red-600 transition text-sm sm:text-base">
              <i class="fas fa-sync-alt"></i>
            </button>
            <div
                class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 absolute left-1/2 transform -translate-x-1/2 bottom-full mb-2 w-20 bg-red-700 text-white text-xs sm:text-sm rounded-md p-2 text-center z-40">
              Retry
            </div>
          </div>
        </div>
      </div>

      <hr class="border-t-2 border-black my-4 opacity-70">
    </div>

    <!-- Analysis results -->
    <div v-if="results">
      <SimpleDiagnostic v-if="simpleView" :results="results" />
      <AdvancedDiagnostic v-else :results="results" />
    </div>
  </div>
</template>

<style scoped>

</style>