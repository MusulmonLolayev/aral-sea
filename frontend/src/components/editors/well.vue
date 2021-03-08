<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-5">
        <q-input
          v-model="well.number"
          :label="$t('number')"
          style="margin-right: 30px"
        />
      </div>

      <div class="col-5">
        <q-select
          :label="$t('select_farm')"
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
          :label="$t('built_year')"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('built_year')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.depth"
          :label="$t('depth')"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('depth')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.diameter"
          :label="$t('diameter')"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('diameter')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.area"
          :label="$t('area')"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('area')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="well.label"
          :label="$t('label')"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('label')]"
        />
      </div>
      <div class="col-7">
        {{ $t("material") }}: &ensp;
        <q-radio v-model="well.material" :val="true" :label="$t('polythene')" />
        <q-radio v-model="well.material" :val="false" :label="$t('metal')" />
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
      if (!value) return this.$t("required");
      if (value < 0) return this.$t("not_higher_zero");
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
