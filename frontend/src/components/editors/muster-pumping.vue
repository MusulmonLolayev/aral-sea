<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-5">
        <q-input
          v-model="muster_pumping.starting_pumping"
          :label="$t('starting_pumping').format_letter()"
          type="time"
          style="margin-right: 30px"
          :rules="[() => required('starting_pumping')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.finishing_pumping"
          :label="$t('finishing_pumping').format_letter()"
          type="time"
          style="margin-right: 30px"
          :rules="[() => required('finishing_pumping')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.count_gall"
          :label="$t('count_gall').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('count_gall')]"
          :suffix="$t('pieces')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.size_gall"
          :label="$t('size_gall').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('size_gall')]"
          :suffix="$t('liter')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.ugv_before_pumping"
          :label="$t('ugv_before_pumping').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('ugv_before_pumping')]"
          :suffix="$t('centimeter_abbr')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.ugv_after_pumping"
          :label="$t('ugv_after_pumping').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('ugv_after_pumping')]"
          :suffix="$t('centimeter_abbr')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.bottom"
          :label="$t('bottom').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('bottom')]"
          :suffix="$t('meter_abbr')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.speed_water"
          :label="$t('speed_water').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('speed_water')]"
          :suffix="$t('liter_second_abbr')"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.elevated"
          :label="$t('elevated').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('elevated')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.reduced"
          :label="$t('reduced').format_letter()"
          type="number"
          style="margin-right: 30px"
          :rules="[() => required('reduced')]"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.water_salinity"
          :label="$t('water_salinity').format_letter()"
          type="number"
          style="margin-right: 30px"
        />
      </div>
      <div class="col-5">
        <q-input
          v-model="muster_pumping.date"
          :label="$t('date').format_letter()"
          type="date"
        />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "Muster",
  props: ["muster_pumping"],
  data: function () {
    return {};
  },
  methods: {
    initialize() {},
    required(name) {
      let value = this.muster_pumping[name];
      if (!value) return this.$t("required").format_letter();
      if (value < 0) return this.$t("not_higher_zero").format_letter();
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
