<script setup>
import {RouterLink, useRoute} from 'vue-router';
import logo from '@/assets/img/university_navbar_logo.png';
import {ref} from "vue";

const route = useRoute();
const isMenuOpen = ref(false);

const routes = [
  {
    path: '/',
    label: 'Home'
  },
  {
    path: '/project',
    label: 'Project'
  },
  {
    path: '/quiz',
    label: 'Quiz'
  },
  {
    path: '/help',
    label: 'Help'
  }
];

const isActiveLink = (routePath) => {
  return route.path === routePath;
};
</script>

<template>
  <nav class="bg-white border-b border-gray-300 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex h-20 items-center justify-between">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center space-x-2">
          <img class="h-10 w-auto" :src="logo" alt="ECG Logo" />
          <span class="hidden md:inline-block text-black text-2xl font-bold">ECG-prediction-IA</span>
        </RouterLink>

        <!-- Desktop Nav Links -->
        <div class="hidden md:flex space-x-3 ml-auto">
          <RouterLink
              v-for="link in routes"
              :key="link.path"
              :to="link.path"
              :aria-current="isActiveLink(link.path) ? 'page' : null"
              :class="[
              'px-4 py-2 rounded-md font-semibold transition-colors duration-150',
              isActiveLink(link.path)
                ? 'bg-gray-400 text-white'
                : 'text-black hover:bg-red-800 hover:text-white',
            ]"
          >
            {{ link.label }}
          </RouterLink>
        </div>

        <!-- External Link Icon (always visible on desktop, shown after menu in mobile) -->
        <a
            href="https://nightingaleheart.com/demos/healthview"
            target="_blank"
            rel="noopener noreferrer"
            class="hidden md:flex items-center text-black hover:text-red-600 px-3 py-2 ml-4"
            title="Return To Healthview"
        >
          <i class="fas fa-door-open mr-2"></i>
        </a>

        <!-- Mobile Burger Menu Button -->
        <button
            @click="isMenuOpen = !isMenuOpen"
            class="md:hidden inline-flex items-center justify-center p-2 rounded-md text-black hover:text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500"
            aria-label="Toggle menu"
        >
          <svg
              class="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
          >
            <path
                :class="{ hidden: isMenuOpen }"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
            />
            <path
                v-if="isMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu Dropdown -->
    <div v-if="isMenuOpen" class="md:hidden px-4 pb-4 space-y-2">
      <RouterLink
          v-for="link in routes"
          :key="link.path + '-mobile'"
          :to="link.path"
          @click="isMenuOpen = false"
          :class="[
          'block w-full text-left px-4 py-2 rounded-md font-semibold transition-colors duration-150',
          isActiveLink(link.path)
            ? 'bg-gray-400 text-white'
            : 'text-black hover:bg-red-800 hover:text-white',
        ]"
      >
        {{ link.label }}
      </RouterLink>

      <!-- External Link in mobile view -->
      <a
          href="https://nightingale.uni-mainz.de/#/demos"
          target="_blank"
          rel="noopener noreferrer"
          class="block px-4 py-2 text-black hover:text-red-600"
      >
        <i class="fas fa-door-open mr-2"></i>
      </a>
    </div>
  </nav>
</template>
