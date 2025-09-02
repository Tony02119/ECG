<script setup>
import {onMounted, ref} from "vue";

const props = defineProps({
  questionIndex: {
    type: Number,
    required: true
  },
  question: {
    type: Object,
    required: true,
  },
  answerIndex: {
    required: true,
  },
  showAnswer: {
    type: Boolean,
    default: false
  }
});

const emits = defineEmits(['answerSelected']);

const selectedIndex = ref(-1); // Variable storing the index of the selected answer

onMounted(() => {
  // Reselect the previous answer while mounting the component
  selectedIndex.value = props.answerIndex;
});

// Select a value in the answer list
const selectAnswer = (index) => {
  selectedIndex.value = index;
  emits("answerSelected", index);
}

</script>

<template>
  <div class="border border-black border-opacity-40 rounded-lg p-4">
    <span class="text-xl font-semibold">{{ questionIndex + 1 }}) {{ question.label }}</span>

    <div v-if="question.plotBase64" class="bg-gray-400 shadow-lg rounded-lg p-4 sm:p-6 my-4">
      <img
          :src="`data:image/png;base64,${question.plotBase64}`"
          alt="ECG Signal"
          class="mx-auto rounded-lg w-full max-w-3xl"
      />
    </div>

    <ul v-if="!showAnswer" class="mt-2">
      <li
          v-for="(answer, index) in question.answers" :key="index"
          class="rounded-xl cursor-pointer text-lg py-2 px-4 mb-2"
          :class="selectedIndex === index ? 'bg-red-700 text-white' : 'bg-white hover:bg-gray-200 hover:text-black'"
          @click="selectAnswer(index)"
      >
        {{ answer }}
      </li>
    </ul>
    <ul v-else class="mt-2">
      <li
          v-for="(answer, index) in question.answers" :key="index"
          class="rounded-xl text-lg py-2 px-4 mb-2"
          :class="[question.correctAnswerIndex === index ? 'bg-green-700 text-white'
              : selectedIndex === index ? 'bg-red-700 text-white' : 'bg-white']"
      >
        <span>
          {{ selectedIndex === index && question.correctAnswerIndex !== index  ? '❌' : '' }}
          {{ selectedIndex === index && question.correctAnswerIndex === index  ? '✅' : '' }}
          {{ answer }}
        </span>
      </li>
    </ul>
    <br>
    <p v-if="showAnswer" class="whitespace-pre-wrap text-justify">
      <i>{{ question.answerDetails }}</i>
    </p>
  </div>
</template>
