<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-5">
        <q-input
          v-model="soil_deep.from_deep"
          :label="$t('soil_deep_from').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('from_deep')]"
        />
      </div>

      <div class="col-5">
        <q-input
          v-model="soil_deep.to_deep"
          :label="$t('soil_deep_to').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('to_deep')]"
        />
      </div>

      <div class="col-5">
        <q-select
          :label="$t('select_soil_type').format_letter()"
          :options="soil_types"
          option-value="id"
          option-label="name"
          emit-value
          map-options
          v-model="soil_deep.soil_type"
          style="margin-right: 30px"
          :rules="[selected => selected != null]"
        />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "SoilDeep",
  props: ["soil_deep"],
  data: function() {
    return {
        soil_types: [],
    };
  },
  methods: {
    initialize() {
        this.$axios
        .get("soil_type_request")
        .then(response => {
            this.soil_types = response.data;
        })
    },
    required(name) {
      let value = this.soil_deep[name];
      if (!value && value != 0) return this.$t("required").format_letter();
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
