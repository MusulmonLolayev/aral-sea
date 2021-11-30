<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-5">
        <q-input
          v-model="soil_chemical_analysis.electric_wire"
          :label="'ec1'.format_letter('ABS')"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('electric_wire')]"
        />
      </div>
      
      <div class="col-5">
        <q-input
          v-model="soil_chemical_analysis.hco3"
          :label="'hco3'.format_letter('ABS')"
          type="number"
          style="margin-right: 30px"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="soil_chemical_analysis.cl"
          :label="'cl'.format_letter()"
          type="number"
          style="margin-right: 30px"
        />
      </div>

      <div class="col-5">
        <q-input
          v-model="soil_chemical_analysis.so4"
          :label="'so'.format_letter('ABS')"
          type="number"
          style="margin-right: 30px"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="soil_chemical_analysis.ca"
          :label="'ca'.format_letter()"
          type="number"
          style="margin-right: 30px"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="soil_chemical_analysis.mg"
          :label="'mg'.format_letter()"
          type="number"
          style="margin-right: 30px"
        />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "SoilChemicalAnalysis",
  props: ["soil_chemical_analysis"],
  data: function() {
    return {};
  },
  methods: {
    initialize() {},
    required(name) {
      let value = this.soil_chemical_analysis[name];
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