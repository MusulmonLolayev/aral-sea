<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-5">
        <q-input
          v-model="mgv.degree"
          :label="$t('mgv_value').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('degree')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="mgv.date"
          :label="$t('date').format_letter()"
          type="date"
        />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "Mgv",
  props: ["mgv"],
  data: function() {
    return {};
  },
  methods: {
    initialize() {},
    required(name) {
      let value = this.mgv[name];
      if (!value) return this.$t("required").format_letter();
      if (value < 0) return this.$t("not_higher_zero").format_letter();
      return true;
    },
    hasError() {
      let error = false;
      this.labels.forEach(item => {
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
    }
  },
  beforeMount() {
    this.initialize();
  }
};
</script>

<style lang="scss" scoped></style>>
