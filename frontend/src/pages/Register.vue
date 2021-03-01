<template>
  <q-card class="card">
    <q-layout>
      <span v-show="IsError" style="color: red">
        {{ $t("username_or_password_incorrect") }}
      </span>
      <span
        v-show="$store.state.common.IsRefreshingTokenExpired"
        style="color: red"
      >
        {{ $t("token_has_expired") }} <br />
        {{ $t("please_relogin") }}
      </span>
      <span v-show="IsNotFilled" style="color: red">
        {{ $t("fill_all_fields") }}
      </span>
      <q-input
        v-model="username"
        :label="$t('user_or_email')"
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
        :label="$t('password')"
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

      <q-input
        v-model="password2"
        :type="isPwd ? 'password' : 'text'"
        :label="$t('reenter_password')"
        style="margin: 5px"
        @keydown.enter.prevent="login"
        :rules="[() => password == password2 ? true : $t('passwords_not_compatible')]"
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
        @click="register"
        :disabled="IsDisabled || password != password2"
      >
        {{ $t("register") }}
      </q-btn>
    </q-layout>
  </q-card>
</template>

<script>
export default {
  data: function () {
    return {
      isPwd: true,
      username: "",
      password: "",
      password2: "",
      IsError: false,
      IsNotFilled: false,
    };
  },
  computed: {
    IsDisabled() {
      return !this.username || !this.password;
    },
  },
  methods: {
    register() {
      if (this.IsDisabled) {
        this.IsNotFilled = true;
        return;
      }
      this.IsNotFilled = false;
      this.IsError = false;
      this.$axios
        .post("/register/", {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          
          this.$router.go(-1);
        })
        .catch((error) => {
          this.IsError = true;
        });
    },
  },
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
  max-height: 300px;
}
</style>