<template>
  <div>
    <div class="row">
      <div class="col" style="margin: 30px">
        <q-carousel
          animated
          v-model="slide"
          navigation
          infinite
          :autoplay="autoplay"
          arrows
          transition-prev="slide-right"
          transition-next="slide-left"
          @mouseleave="autoplay = true"
        >
          <q-carousel-slide :name="1" img-src="/index1.jpg" />
          <q-carousel-slide :name="2" img-src="/index2.jpg" />
          <q-carousel-slide :name="3" img-src="/index3.jpg" />
          <q-carousel-slide :name="4" img-src="/index4.png" />
          <q-carousel-slide :name="5" img-src="/index5.jpg" />
        </q-carousel>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  data: function() {
    return {
      slide: 1,
      autoplay: true
    };
  }
};
</script>
