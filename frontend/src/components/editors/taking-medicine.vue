<template>
  <q-form ref="form">
    <div>
      <div class="row">
        <div class="input_div">
          <q-input
            :label="$t('from_date_of_taking_medicine')"
            v-model="takingmedicine.fromdate"
            type="date"
          />
        </div>
        <div class="input_div">
          <q-select
            :label="$t('streptomycin')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="takingmedicine.streptomycin"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('rifampicin')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="takingmedicine.rifampicin"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('isoniazid')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="takingmedicine.isoniazid"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('pyrazinamide')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="takingmedicine.pyrazinamide"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('ethambutol')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="takingmedicine.ethambutol"
          />
        </div>

        <div class="input_div">
          <q-checkbox
            v-model="takingmedicine.status"
            :label="$t('status')"
            style="margin-top: 15px"
          />
        </div>
        <div class="input_div">
          <q-input
            :label="$t('date')"
            v-model="takingmedicine.date"
            type="date"
          />
        </div>
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "TakingMedicine",
  props: ["takingmedicine"],
  methods: {
    initialize() {
      if (typeof this.takingmedicine.id == "undefined") {
        this.takingmedicine.date = this.$helper.GetCurrentDate();
        this.takingmedicine.fromdate = this.$helper.GetCurrentDate();
      }
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
<style scop>
div.input_div {
  margin-left: 5px;
  margin-right: 5px;
  width: 200px;
}
</style>
