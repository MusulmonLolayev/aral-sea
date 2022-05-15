<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-5">
        <q-input
          v-model="well.number"
          :label="$t('number').format_letter()"
          style="margin-right: 30px"
        />
      </div>

      <div class="col-5">
        <q-select
          :label="$t('select_farm').format_letter()"
          :options="farms"
          option-value="id"
          option-label="name"
          emit-value
          map-options
          v-model="well.farm"
        />
      </div>

      <div class="col-5">
        <q-input
          v-model="well.x"
          label="x"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('x')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.y"
          label="y"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('y')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.built_year"
          :label="$t('built_year').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('built_year')]"
          :suffix="$t('year')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.depth"
          :label="$t('depth').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('depth')]"
          :suffix="$t('meter')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.diameter"
          :label="$t('diameter').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('diameter')]"
          :suffix="$t('meter')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.area"
          :label="$t('area').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('area')]"
          :suffix="$t('hectare')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.label"
          :label="$t('label').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('label')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.imei"
          :label="$t('imei').format_letter()"
          style="margin-right: 30px"
          :rules="[(value) => checkIMEI(value) ]"
        />
      </div>
      <div class="col-7">
        {{ $t("material").format_letter() }}: &ensp;
        <q-radio v-model="well.material" :val="true" :label="$t('polythene').format_letter()" />
        <q-radio v-model="well.material" :val="false" :label="$t('metal').format_letter()" />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "Well",
  props: ["well"],
  data: function () {
    return {
      farms: [],
    };
  },
  methods: {
    initialize() {
      this.$axios.get("/farm_request/0").then((response) => {
        this.farms = response.data;
        if (this.well.id == 0) {
          this.well.farm = this.farms[0].id;
        }
      });
    },
    required(name) {
      let value = this.well[name];
      if (!value) return this.$t("required").format_letter();
      if (value < 0) return this.$t("not_higher_zero").format_letter();
      return true;
    },
    checkIMEI(value){
      if (value != '' && ! value.match(/^([0-9]){15}/)){
        return this.$t('the_imei_15_digit')
      }
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
  mounted() {
    this.initialize();
  },
};
</script>

<style lang="scss" scoped>
</style>>
