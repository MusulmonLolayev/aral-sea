<template>
  <div>
    <q-list>
      <q-item clickable to='/'>
        <q-item-section avatar>
          <q-icon color="primary" name="home" />
        </q-item-section>
        <q-item-section>{{$t('home').format_letter()}}</q-item-section>
      </q-item>
      <div v-if="show_loggined_div">
        <q-expansion-item
          expand-separator
          icon="list"
          :label="$t('data').format_letter()"
          >
          <q-list>
            <q-item clickable to='wells' style="margin-left:20px">
              <q-item-section avatar>
                <q-icon color="primary"/>
              </q-item-section>
              <q-item-section>{{$t('my_wells').format_letter()}}</q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>
        <q-expansion-item
          expand-separator
          icon="person_outline"
          :label="$t('user').format_letter()"
          >
          <q-list>
            <q-item clickable @click="logout" style="margin-left:20px">
              <q-item-section avatar>
                <q-icon color="primary" name="fas fa-sign-out-alt"/>
              </q-item-section>
              <q-item-section>{{$t('logout').format_letter()}}</q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>
      </div>
    </q-list>
  </div>
</template>

<script>
export default {
  name: 'EssentialLink',
  computed: {
    show_loggined_div(){
      return this.$store.state.auth.IsLoggined;
    }
  },
  methods: {
    logout(){
      this.$store.dispatch('auth/logout')
      .then(() => {
        if (this.$router.currentRoute.path != "/"){
          this.$router.push("/")
        }
      })
    }
  },
}
</script>
