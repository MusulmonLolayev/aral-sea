<template>
  <div class="q-pa-md">
    <q-video
      :ratio="16/9"
      :src="src"
    />
  </div>
</template>

<script>
export default {
  name: 'Vidoe-Guide',
  data(){
    return{
      src: process.env.PROD ? "http://tub-aspergillosis.uz/static/videos/help.mp4" : "help.mp4"
      //src: "http://tub-aspergillosis.uz/static/videos/help.mp4",
    }
  },
}
</script>