<script setup>
</script>

<template>
  <section class="bg-red-800 min-h-screen">
    <div class="container m-auto max-w-3xl py-24">
      <div class="bg-white px-4 md:px-8 py-8 mb-4 shadow-md rounded-md border">
        <!-- Titre du projet -->
        <h2 class="text-3xl text-center font-semibold mb-8">How to Use the ECG Analysis Tool</h2>

        <!-- Guide pour l'utilisation des outils d'analyse -->
        <div class="mb-6">
          <p class="text-gray-700 mb-4">
            This guide will help you understand how to use our ECG analysis service, powered by artificial intelligence (AI), to detect potential heart diseases.
          </p>
        </div>

        <!-- Méthode 1: Sélection d'un ECG prédéfini -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Method One: Select a Predefined ECG</h3>
          <ul class="list-disc list-inside text-gray-700 mb-4 space-y-2">
            <li>
              Select one of the colored hearts displayed on the left side of the page. The green heart represents a healthy ECG, the yellow heart a mildly unhealthy ECG, and the red heart indicates a critically unhealthy ECG.
            </li>
            <li>
              After selecting, click on the <strong>"Analyze ECG"</strong> button to start the AI analysis.
            </li>
            <li>
              A loading circle will appear while the AI processes the data.
            </li>
            <li>
              The results are displayed below the "ECG Analysis" button. An <strong>"Expert"</strong> button can be clicked to show more information for medical professionals, such as doctors, to facilitate the diagnosis of cardiac diseases.
            </li>
          </ul>
        </div>

        <!-- Méthode 2: Upload d'un fichier CSV -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold text-gray-900 mb-2">Method Two: Upload a CSV File</h3>
          <ul class="list-disc list-inside text-gray-700 mb-4 space-y-2">
            <li>
              You can also upload your own ECG data by dragging and dropping a CSV file into the provided area.
            </li>
            <li>
              Please note that <strong>only CSV files</strong> are accepted. If you try to upload another file type, the system will reject it and display an error message.
            </li>
            <li>
              After uploading the file, click on the <strong>"Analyze ECG"</strong> button to start the analysis. The process will be the same as in Method 1.
            </li>
          </ul>
        </div>

        <!-- Avertissement sur l'utilisation -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold text-red-600 mb-2">Important Notice</h3>
          <p class="text-gray-700">
            This project is for demonstration purposes only and is <strong>not intended for medical use</strong>. The results provided by this tool may be inaccurate and should not be used as a substitute for professional medical diagnosis. Always consult a healthcare professional for an accurate assessment.
          </p>
        </div>

        <!-- Remerciements -->
        <div class="text-center">
          <p class="text-gray-700 font-semibold">Thank you for using our ECG analysis tool!</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
h2 {
  color: #333;
}

p, ul {
  line-height: 1.6;
}

label {
  display: block;
  margin-bottom: 8px;
}

.container {
  max-width: 72rem;
  padding-left: 0.5rem;
  padding-right: 0.5em;
  text-align: justify;
}
</style>
