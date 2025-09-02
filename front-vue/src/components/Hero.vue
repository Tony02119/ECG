<script setup>
defineProps({
  title: {
    type: String,
    default: 'ECG prediction AI',
  },
  subtitle: {
    type: String,
    default: 'Heart disease detection with AI',
  },
});
</script>

<template>
  <section class="bg-red-800 py-4 mb-4">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col items-center">
      <h1 class="text-2xl font-extrabold text-white sm:text-3xl md:text-4xl">
        {{ title }}
      </h1>
      <p class="mt-4 text-l text-white">
        {{ subtitle }}
      </p>
    </div>
  </section>
</template>
