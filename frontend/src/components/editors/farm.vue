<template>
  <q-form ref="form">
    <div class="row">
      <div class="col-12">
        <q-input
          v-model="farm.name"
          :label="$t('farm_name').format_letter()"
          style="margin-right: 30px"
          :rules="[val => val != '']"
        />
      </div>
      <div class="col-12">
        <q-select
          :label="$t('select_district').format_letter()"
          :options="districts"
          option-value="id"
          option-label="name"
          emit-value
          map-options
          v-model="farm.district"
          style="margin-right: 30px"
          :rules="[selected => selected != null]"
        />
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "Farm",
  props: ["farm"],
  data: function() {
    return {
        districts: []
    };
  },
  methods: {
    initialize() {
        this.$axios
        .get("/get_user_district")
        .then(response => {
            this.districts = response.data
            this.farm.district = this.districts[0].id
        })
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
