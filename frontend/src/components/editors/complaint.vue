<template>
  <q-form ref="form">
    <div class="row">
      <div class="input_div">
        <q-select
          :label="$t('diarrhea')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.diarrhea"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('normal_stool')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.normal_stool"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('constipation')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.constipation"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('flatulence')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.flatulence"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('stomachache')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.stomachache"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('character')"
          :options="characters"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.character"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('tolerance')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.tuberculosis_tolerance"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('related_disease')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.related_disease"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('nausea')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.nausea"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('vomiting')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.vomiting"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('headache')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.headache"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('sweating')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.sweating"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('weakness')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.weakness"
        />
      </div>

      <div class="input_div">
        <q-select
          :label="$t('allergodermatosis')"
          :options="$helper.yes_no_options()"
          option-value="value"
          option-label="name"
          emit-value
          map-options
          v-model="complaint.allergodermatosis"
        />
      </div>

      <div class="input_div">
        <q-input
          :label="$t('stool_frequency')"
          v-model="complaint.stool_frequency"
          type="number"
        />
      </div>

      <div class="input_div">
        <q-input
          :label="$t('weight_lose')"
          v-model="complaint.weight_loss"
          type="number"
        />
      </div>

      <div class="input_div">
        <q-checkbox
          v-model="complaint.status"
          :label="$t('status')"
          style="margin-top: 15px"
        />
      </div>
      <div class="input_div">
        <q-input :label="$t('date')" v-model="complaint.date" type="date" />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "Complaint",
  props: ["complaint"],
  data: function() {
    return {
      characters: []
    };
  },
  methods: {
    async initialize() {
      this.characters = [
        { name: "Полуоформленный", value: 0 },
        { name: "Неоформленный", value: 1 },
        { name: "Оформленный", value: 2 },
        { name: "Нет", value: 3 }
      ];
      this.characters.push({
        name: this.$t("unknown"),
        value: null
      });
      this.complaint.character = this.characters[this.characters.length - 1].value
    },
    hasError() {
      return this.$refs["form"].validate();
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
