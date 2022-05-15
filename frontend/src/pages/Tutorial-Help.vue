<template>
  <div class="q-pa-md">
    <vue-pdf-app :pdf="src" listenToURL="true"></vue-pdf-app>
  </div>
</template>

<script>
import VuePdfApp from "vue-pdf-app";

export default {
  name: "Vidoe-Guide",
  data() {
    return {
      src: process.env.PROD
        ? `http://tub-aspergillosis.uz/static/docs/tutorial-${this.$i18n.locale}.pdf`
        : `docs/tutorial-${this.$i18n.locale}.pdf`
      //src: "http://tub-aspergillosis.uz/static/videos/tutorial-${this.$i18n.locale}.pdf",
    };
  },

  components: {
    VuePdfApp
  },
};
</script>
