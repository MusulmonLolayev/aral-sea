<template>
  <q-card class="card">
    <q-layout>
      <span v-show="IsError" style="color: red">
        {{ $t("username_or_password_incorrect").format_letter() }}
      </span>
      <span
        v-show="$store.state.common.IsRefreshingTokenExpired"
        style="color: red"
      >
        {{ $t("token_has_expired").format_letter() }}, &ensp;
        {{ $t("please_relogin").format_letter() }}
      </span>
      <span v-show="IsNotFilled" style="color: red">
        {{ $t("fill_all_fields").format_letter() }}
      </span>
      <q-input
        v-model="username"
        :label="$t('user_or_email').format_letter()"
        style="margin: 5px"
        @keydown.enter.prevent="login"
      >
        <template v-slot:prepend>
          <q-icon name="person_outline" />
        </template>
      </q-input>
      <q-input
        v-model="password"
        :type="isPwd ? 'password' : 'text'"
        :label="$t('password').format_letter()"
        style="margin: 5px"
        @keydown.enter.prevent="login"
      >
        <template v-slot:prepend>
          <q-icon name="login" />
        </template>
        <template v-slot:append>
          <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
          />
        </template>
      </q-input>
      <q-btn
        flat
        class="full-width"
        style="margin: 5px"
        @click="login()"
        :disabled="IsDisabled"
      >
        {{ $t("login").format_letter() }}
      </q-btn>
    </q-layout>
  </q-card>
</template>

<script>
export default {
  data: function() {
    return {
      isPwd: true,
      username: "",
      password: "",
      IsError: false,
      IsNotFilled: false
    };
  },
  computed: {
    IsDisabled() {
      return !this.username || !this.password;
    }
  },
  methods: {
    login() {
      if (this.IsDisabled) {
        this.IsNotFilled = true;
        return;
      }
      this.IsNotFilled = false;
      this.IsError = false;
      this.$axios
        .post("/login", {
          username: this.username,
          password: this.password
        })
        .then(response => {
          this.$store.dispatch("auth/login", {
            access_token: response.data.access,
            refresh_token: response.data.refresh
          });
          this.$axios.defaults.headers.common[
            "Authorization"
          ] = `Bearer ${response.data.access}`;
          this.$router.go(-1);

          // Get user information
          this.$axios.get("/get_user_information").then(response => {
            this.$store.dispatch("auth/user_information", {
              user_information: response.data
            });
          });
        })
        .catch(() => {
          this.IsError = true;
        });
    }
  }
};
</script>

<style scoped>
.login {
  width: 300px;
  height: 180px;
  align-self: center;
}
.card {
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px;
  width: 100%;
  max-width: 350px;
  padding: 10px;
  max-height: 210px;
}
</style>
