<template>
  <q-form ref="form">
    <div>
      <div class="row">
        <div class="col-5">
          <q-input v-model="muster.depth" :label="$t('depth')" type="number" style="margin-right: 30px" :rules="[() => required('depth')]"/>
        </div>
        <div class="col-5">
          <q-input v-model="muster.degree_salt" :label="$t('degree_salt')" type="number" style="margin-right: 30px" :rules="[() => required('degree_salt')]"/>
        </div>
        <div class="col-5">
          <q-input v-model="muster.date" :label="$t('date')" type="date"/>
        </div>
        <div class="col-5">
          <q-input :label="$t('date')" type="time"/>
        </div>
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "Muster",
  props: ["muster"],
  data: function () {
    return {};
  },
  methods: {
    initialize() {},
    required(name) {
      let value = this.muster[name];
      if (!value) return this.$t("required");
      if (value < 0) return this.$t("not_higher_zero")
      return true;
    },
    hasError() {
      let error = false;
      this.labels.forEach((item) => {
        let res = this.required(item);
        if (typeof res == "string") {
          error = true;
          if (this.$refs[item].hasError) this.$refs[item].validate(true);
        }
      });
      return error;
    },
    hasError() {
      return this.$refs["form"].validate();
    },
  },
  beforeMount() {
    this.initialize();
  },
};
</script>

<style lang="scss" scoped>
</style>>
