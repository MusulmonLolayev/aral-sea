<template>
  <q-form ref="form">
    <div>
      <div class="row">
        <div class="col-5">
          <q-input
            v-model="muster_pumping.starting_pumping"
            :label="$t('starting_pumping')"
            type="time"
            style="margin-right: 30px"
            :rules="[() => required('starting_pumping')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.finishing_pumping"
            :label="$t('finishing_pumping')"
            type="time"
            style="margin-right: 30px"
            :rules="[() => required('finishing_pumping')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.count_gall"
            :label="$t('count_gall')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('count_gall')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.size_gall"
            :label="$t('size_gall')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('size_gall')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.ugv_before_pumping"
            :label="$t('ugv_before_pumping')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('ugv_before_pumping')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.ugv_after_pumping"
            :label="$t('ugv_after_pumping')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('ugv_after_pumping')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.bottom"
            :label="$t('bottom')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('bottom')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.speed_water"
            :label="$t('speed_water')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('speed_water')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.elevated"
            :label="$t('elevated')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('elevated')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.reduced"
            :label="$t('reduced')"
            type="number"
            style="margin-right: 30px"
            :rules="[() => required('reduced')]"
          />
        </div>
        <div class="col-5">
          <q-input
            v-model="muster_pumping.date"
            :label="$t('date')"
            type="date"
          />
        </div>
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
  beforeMount() {
    this.initialize();
  },
};
</script>

<style lang="scss" scoped>
</style>>
