<template>
  <q-form ref="form">
    <div>
      <div class="row">
        <div style="margin-left: 5px; margin-right: 5px; width: 410px">
          <q-select
            :label="$t('clinical_form_of_tuberculosis')"
            :options="clinicalforms"
            option-value="id"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.clinicalform"
            @input="onClinicalformSelected"
          />
        </div>
        <div class="input_div">
          <q-select
            :label="$t('right_lung_top')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.right_lung_top"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('right_lung_bottom')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.right_lung_bottom"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('left_lung_top')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.left_lung_top"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('left_lung_bottom')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.left_lung_bottom"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('infiltration')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.infiltration"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('decay')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.decay"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('seeding')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.seeding"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('resorption')"
            :options="$helper.yes_no_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.resorption"
          />
        </div>

        <div class="input_div">
          <q-select
            :label="$t('bk')"
            :options="$helper.plus_minus_options()"
            option-value="value"
            option-label="name"
            emit-value
            map-options
            v-model="primarydiagnose.bk"
          />
        </div>

        <div class="input_div" style="margin-top: 15px;">
          <q-checkbox v-model="primarydiagnose.status" :label="$t('status')" />
        </div>
        <div class="input_div">
          <q-input
            :label="$t('date')"
            v-model="primarydiagnose.date"
            type="date"
          />
        </div>
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "PrimaryDiagnose",
  props: ["primarydiagnose"],
  data: function() {
    return {
      clinicalforms: []
    };
  },
  methods: {
    async initialize() {
      let response = await this.$axios.get("/clinicalforms");
      this.clinicalforms = response.data;
      this.clinicalforms.push({
        name: this.$t("unknown"),
        id: null
      });
      // then default vaules to primary diagnose
      if (this.primarydiagnose.clinicalform == null)
        this.primarydiagnose.clinicalform = this.clinicalforms[
          this.clinicalforms.length - 1
        ].id;
    },
    hasError() {
      return this.$refs.form.validate();
    },
    onClinicalformSelected() {
      this.clinicalforms.map(item => {
        if (item.id == this.primarydiagnose.clinicalform) {
          this.primarydiagnose.clinicalform_name = item.name;
          return 0;
        }
      });
    }
  },
  mounted() {
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
