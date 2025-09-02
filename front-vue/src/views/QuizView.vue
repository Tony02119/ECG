<script setup>
import QuestionCard from "@/components/QuestionCard.vue";
import {onBeforeUnmount, onMounted, ref, watch} from "vue";
import {getAverageScore, getRandomPlot, saveScore} from "@/services/apiService.js";

// Temporary questions
const questions = ref([
  {
    label: "Does ECG help diagnose arrhythmias ?",
    answers: ["True", "False"],
    correctAnswerIndex: 0,
    answerDetails: "Yes ECG helps diagnose arrhythmias and other conditions.",
  },
  {
    label: "P wave represents the depolarization of :",
    answers: ["Ventricular", "Atria", "Artery"],
    correctAnswerIndex: 1,
    answerDetails: "P wave represents  depolarization of the atria (contraction of the atria)."
  },
  {
    label: "Atrial Fibrillation (AFIB) is characterized by slow and irregular electrical activity in the atria ?",
    answers: ["True", "False"],
    correctAnswerIndex: 1,
    answerDetails: "It's false, AFIB is characterized by a fast and irregular electrical activity in the atria. Not a slow activity."
  }
]);

const loading = ref(true);
const currentIndex = ref(0); // Index of the current question
const key = ref(0); // Key use to refresh the QuestionCard component
const userAnswers = ref(Array(10).fill(-1)); // Variable storing user answers
const pendingQuestions = ref("1, 2, 3, 4, 5, 6, 7, 8, 9, 10"); // Variable storing the pending questions
const isValid = ref(false); // Variable to check that all questions have been answered
const submitted = ref(false); // Variable storing the status of the quiz
const stats = ref({}); // Variable storing the stats of the quiz
const score = ref(0); // Variable storing the final score of the quiz

onMounted(async () => {
  window.addEventListener('keydown', handleKeyDown);

  try {
    stats.value = await getAverageScore();

    for (let i = 0; i < 7; i++) {
      const response = await getRandomPlot();

      questions.value.push({
        label: "This electrocardiogram is a risk factor:",
        plotBase64: response.plot_url,
        answers: ["Low", "Mid", "High"],
        correctAnswerIndex: getAnswerIndex(response.color_choice),
        answerDetails: getAnswerDetails(response.color_choice)
      });
    }
    loading.value = false;
  } catch (err) {
    console.error(err)
  }
});

onBeforeUnmount(() => window.removeEventListener('keydown', handleKeyDown));

watch(userAnswers.value, (newUserAnswers) => {
  pendingQuestions.value = newUserAnswers.map((val, i) => val === -1 ? i + 1 : null)
      .filter(num => num !== null)
      .join(", ");
});

// Handle key down for navigating through questions
const handleKeyDown = (e) => {
  switch (e.key) {
    case "ArrowLeft":
      previous();
      break;
    case "ArrowRight":
      next();
      break;
  }
}

// Get answer index for a plot
const getAnswerIndex = (colorChoice) => {
  let answerIndex;
  switch (colorChoice) {
    case "green":
      answerIndex = 0;
      break;
    case "yellow":
      answerIndex = 1;
      break;
    case "red":
      answerIndex = 2;
      break;
  }
  return answerIndex;
}

const getAnswerDetails = (colorChoice) => {
  let answerDetails;
  switch (colorChoice) {
    case "green":
      answerDetails = `Possible Indicators of Low Risk:

      1. Normal Amplitude and Shape
         - The ECG waveform closely follows the standard P-QRS-T pattern.
         - Amplitudes and segment durations fall within normal physiological ranges.

      2. Regular Rhythm
         - Heartbeats are evenly spaced with consistent intervals.
         - No signs of arrhythmia or conduction delays are present.

      3. No Abnormal Segment Changes
         - ST segments and T waves appear normal.
         - No elevation, depression, or unusual waveforms detected.`;
      break;
    case "yellow":
      answerDetails = `Possible Indicators of Moderate Risk:

      1. Slightly Abnormal Amplitude or Shape
         - The ECG shows mild deviations from the normal waveform, such as unusual peak sizes or irregular segment shapes.
         - These changes may suggest early signs of electrical conduction issues or structural heart conditions.

      2. Irregular Timing or Rhythm
         - The spacing between heartbeats (intervals) might be slightly shorter or longer than normal.
         - This could indicate mild arrhythmias or heart rate variability that warrants observation.

      3. Non-Specific ECG Changes
         - The ECG may include non-specific ST segment or T wave changes, which can appear in a range of conditions.
         - While not definitive for a particular disease, such changes can signal the need for preventive measures or lifestyle adjustments.`;
      break;
    case "red":
      answerDetails = `Possible Indicators of High Risk:

      1. Severe Abnormalities in Amplitude or Waveform
         - Extremely high or low peaks that deviate significantly from normal ECG values.
         - Distorted or absent P, QRS, or T waves may indicate acute myocardial infarction or severe arrhythmias.

      2. Dangerous Rhythm Patterns
         - Irregular or chaotic rhythms such as ventricular fibrillation or tachycardia.
         - Presence of abnormal sequences like prolonged QT intervals or frequent premature beats.

      3. ST Segment Elevation or Depression
         - Significant ST elevation or depression may signal acute ischemia or infarction.
         - Immediate clinical attention is often required for such patterns.`;
      break;
  }
  return answerDetails;
}

// Go to the previous question
const previous = () => {
  currentIndex.value = currentIndex.value > 0 ? currentIndex.value - 1 : 0;
  key.value++;
}

// Go to the next question
const next = () => {
  currentIndex.value = currentIndex.value < questions.value.length - 1 ? currentIndex.value + 1 : questions.value.length - 1;
  key.value++;
}

// Save answer before submitting
const saveAnswer = (answer) => {
  userAnswers.value[currentIndex.value] = answer;
  isValid.value = userAnswers.value.length === questions.value.length && !userAnswers.value.includes(-1);
}

// Submit the quiz
const submit = async () => {
  submitted.value = true;
  questions.value.forEach((item, index) => {
    if (item.correctAnswerIndex === userAnswers.value[index]) score.value++;
  });

  try {
    await saveScore(score.value);
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <section class="bg-red-800 min-h-screen">
    <div class="container m-auto max-w-3xl py-24">
      <div class="bg-white px-4 md:px-8 py-8 mb-4 shadow-md rounded-md border">
        <!-- Quiz title -->
        <h1 class="text-3xl text-center font-semibold mb-8">Quiz</h1>

        <!-- Description -->
        <div class="mb-6">
          <p class="text-gray-700 mb-4">
            This quiz contains ten questions to test your knowledge of Electrocardiograms (ECGs). You can return to a
            question at any time before submitting the quiz. Your final score will be displayed at the end.
          </p>

          <span v-if="stats.numberOfUsers > 0"><b>{{ stats.numberOfUsers }}</b> user(s) have already completed the quiz, with an average score of <b>{{ stats.average.toFixed(2) }}/10</b></span>
        </div>

        <!-- Loading indicator -->
        <div v-if="loading" class="text-center mt-6">
          <i class="fas fa-spinner fa-spin text-4xl text-red-800"></i>
        </div>

        <div v-if="!submitted && !loading">
          <!-- Questions -->
          <div class="flex flex-col items-center space-y-4 mb-6">
            <QuestionCard
                :key="key"
                :questionIndex="currentIndex"
                :question="questions[currentIndex]"
                :answerIndex="userAnswers[currentIndex]"
                @answer-selected="saveAnswer"
                class="w-full"
            />
            <div
                v-if="currentIndex === questions.length - 1"
                class="flex flex-col items-center"
            >
              <span v-if="!isValid" class="mb-2">You must answer the following question(s) to validate the quiz: {{ pendingQuestions }}</span>
              <button
                  @click="submit"
                  :disabled="!isValid"
                  class="px-6 py-4 bg-red-800 text-white rounded hover:bg-red-600 transition disabled:opacity-70"
              >
                Submit
              </button>
            </div>
            <span>{{ currentIndex + 1 }} / {{ questions.length }}</span>
          </div>

          <!-- Previous/Next buttons -->
          <div class="flex justify-around">
            <i
                @click="previous"
                class="fas fa-angle-left cursor-pointer text-3xl"
                :class="[currentIndex !== 0 ? 'opacity-100' : 'opacity-0']"
            />
            <i
                @click="next"
                class="fas fa-angle-right cursor-pointer text-3xl"
                :class="[currentIndex !== questions.length - 1 ? 'opacity-100' : 'opacity-0']"
            />
          </div>
        </div>
        <div v-if="submitted" class="text-center">
          <h2 class="text-2xl text-center font-extrabold mb-2 mt-12">Congratulations !</h2>
          <span class="text-xl">Your score is : {{ score }} / {{ questions.length }}</span>

          <div
              v-for="(question, index) in questions"
              :key="index"
              class="mt-4"
          >
            <QuestionCard
                :key="key"
                :questionIndex="index"
                :question="question"
                :answerIndex="userAnswers[index]"
                show-answer
                class="w-full"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.container {
  max-width: 72rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  text-align: justify;
}
</style>