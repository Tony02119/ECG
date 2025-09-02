<script>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
import Footer from "@/components/Footer.vue";
import DisclaimerPopup from './components/DisclaimerPopup.vue';

export default {
  components: { DisclaimerPopup , Navbar},
  data() {
    return {
      showDisclaimer: false
    };
  },
  mounted() {
    const last = localStorage.getItem('disclaimerAcceptedAt');
    const now = Date.now();
    if (!last || now - parseInt(last, 10) > 86400000) {
      this.showDisclaimer = true;
    }
  },
  methods: {
    acceptDisclaimer() {
      localStorage.setItem('disclaimerAcceptedAt', Date.now().toString());
      this.showDisclaimer = false;
    }
  }
}
</script>

<template>
  <DisclaimerPopup v-if="showDisclaimer" @accepted="acceptDisclaimer" />
  <Navbar />
  <RouterView />
  <Footer />
</template>
