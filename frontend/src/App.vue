<template>
  <div id="q-app">
    <q-ajax-bar ref="bar" size="3px" color="green" :delay="delay" />
    <router-view v-on:startAjaxBar="onStartAjaxBar" v-on:stopAjaxBar="onStopAjaxBar" />
  </div>
</template>
<script>
export default {
  name: 'App',
  data: function(){
    return {
      title: '',
      delay: 0
    }
  },
  methods: {
    initialize(){
      this.title = this.$t('app_name')
    },
    onStartAjaxBar () {
      console.log('started')
      this.$refs.bar.start()
    },
    onStopAjaxBar () {
      console.log('stopped')
      this.$refs.bar.stop()
    }
  },

  meta() {
    return {
      title: this.$t('app_name'),
    };
  },
  mounted: function(){
    this.initialize()
  }
}
</script>
