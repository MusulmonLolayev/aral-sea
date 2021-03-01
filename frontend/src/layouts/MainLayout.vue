<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <q-toolbar-title>
          {{ $t("app_name") }}
        </q-toolbar-title>

        <div
          style="float: right; margin-right: 20px"
          v-if="!$store.state.auth.IsLoggined"
        >
          <q-btn flat dense borderless :label="$t('login')" to="login" />
        </div>

        <div style="float: right">
          <select-localization />
        </div>

        <q-icon
          name="fas fa-signal"
          style="margin-left: 10px; margin-right: 10px"
          v-if="$store.state.common.IsOnline == true"
        />
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <essential-link />
    </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
    <q-ajax-bar
      ref="bar"
      position="bottom"
      color="accent"
      size="10px"
      skip-hijack
    />
  </q-layout>
</template>

<script>
import EssentialLink from "../components/EssentialLink.vue";
import SelectLocalization from "../components/SelectLocalization.vue";

export default {
  name: "MainLayout",
  data() {
    return {
      leftDrawerOpen: false,
      IsOnline: window.navigator.onLine,
    };
  },
  watch: {
    IsOnline: function(){
      return window.navigator.onLine
    }
  },
  mounted() {
    let store = this.$store
    window.addEventListener("offline", function (e) {
      store.dispatch('common/setConnectionStatus', {status: false})
    });

    window.addEventListener("online", function (e) {
      store.dispatch('common/setConnectionStatus', {status: true})
    });
  },
  components: { EssentialLink, SelectLocalization },
};
</script>
