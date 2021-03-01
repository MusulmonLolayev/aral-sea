<template>
  <q-select
    v-model="lang"
    :options="$store.state.common.LangOptions"
    dense
    borderless
    emit-value
    map-options
    options-dense
    style="min-width: 80px"
  />
</template>

<script>
export default {
  data: function () {
    return {
      lang: this.$i18n.locale,
    }
  },
  watch: {
    lang (lang) {
      localStorage.setItem('lang', lang)
      this.$i18n.locale = lang
      this.$store.dispatch('common/setLangOptions')
    }
  },
  mounted: function () {
    this.lang = localStorage.getItem('lang') || this.$i18n.locale
    this.$store.dispatch('common/setLangOptions')
  }
}
</script>
