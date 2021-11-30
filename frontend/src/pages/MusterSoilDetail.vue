<template>
  <div style="margin: 15px">
    <h4 style="margin: 10px">{{ $t("muster_soil").format_letter() }}</h4>
    <q-separator color="orange" />
    <div class="row" style="margin-left: 10px">
      <q-form ref="form">
        <div class="row">
          <div class="col-5">
            <q-select
              :label="$t('select_farm').format_letter()"
              :options="farms"
              option-value="id"
              option-label="name"
              emit-value
              map-options
              v-model="selected_farm"
              style="margin-right: 30px"
              :rules="[selected => selected != null]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>

          <div class="col-5">
            <q-select
              :label="$t('select_well').format_letter()"
              :options="wells"
              option-value="id"
              option-label="number"
              emit-value
              map-options
              v-model="muster_soil.well"
              style="margin-right: 30px"
              :rules="[selected => selected != null]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>

          <div class="col-5">
            <q-input
              v-model="muster_soil.contour_no"
              :label="$t('contour_no').format_letter()"
              type="number"
              style="margin-right: 30px"
              :rules="[() => required('contour_no')]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>

          <div class="col-5">
            <q-input
              v-model="muster_soil.pit_no"
              :label="$t('pit_no').format_letter()"
              type="number"
              style="margin-right: 30px"
              :rules="[() => required('pit_no')]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
          <div class="col-5">
            <q-input
              v-model="muster_soil.area_size"
              :label="$t('area_size').format_letter()"
              type="number"
              style="margin-right: 30px"
              :rules="[() => required('area_size')]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
          <div class="col-5">
            <q-select
              :label="$t('select_salt_degree').format_letter()"
              :options="salt_degrees"
              option-value="id"
              option-label="name"
              emit-value
              map-options
              v-model="muster_soil.salt_degree"
              style="margin-right: 30px"
              :rules="[selected => selected != null]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
          <div class="col-5">
            <q-input
              :label="$t('date').format_letter()"
              type="date"
              v-model="muster_soil.date"
              style="margin-right: 30px"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
          <div class="col-5">
            <q-select
              :label="$t('select_crop_type').format_letter()"
              :options="crop_types"
              option-value="id"
              option-label="name"
              emit-value
              map-options
              v-model="muster_soil.crop_type"
              style="margin-right: 30px"
              :rules="[selected => selected != null]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
          <div class="col-5">
            <q-input
              v-model="muster_soil.location_x"
              :label="$t('location_x').format_letter()"
              type="number"
              style="margin-right: 30px"
              :rules="[() => required('location_x')]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
          <div class="col-5">
            <q-input
              v-model="muster_soil.location_y"
              :label="$t('location_y').format_letter()"
              type="number"
              style="margin-right: 30px"
              :rules="[() => required('location_y')]"
              :readonly="!IsPermission('add_mustersoil')"
            />
          </div>
        </div>
      </q-form>
    </div>

    <div class="row" style="float:right; margin: 20px">
      <q-btn
        style="margin-right: 10px"
        :label="$t('cancel')"
        @click="$router.go(-1)"
        :disable="!IsPermission('add_mustersoil')"
      ></q-btn>
      <q-btn
        style="margin-right: 10px"
        :label="$t('save_and_back')"
        @click="onSaveAndBack"
        :disable="!IsPermission('add_mustersoil')"
      ></q-btn>
      <q-btn
        style="margin-right: 10px"
        :label="$t('save')"
        @click="onSave"
        :disable="!IsPermission('add_mustersoil')"
      ></q-btn>
    </div>
    <br />
    <h4 style="margin: 10px">
      {{ $t("soil_deep_analysis_list").format_letter() }}
    </h4>
    <q-separator color="orange" />
    <br />
    <soil-degree-table :muster_soil="muster_soil" :SaveMusterSoil="onSave" />
    <div :hidden="!IsPermission('add_analysissoil')">
      <h4 style="margin: 10px">
        {{ $t("soil_chemical_analysis").format_letter() }}
      </h4>
      <q-separator color="orange" />
      <br />
      <soil-chemical-analysis
        :soil_chemical_analysis="soil_chemical_analysis"
        style="margin-left: 10px"
        ref="refSoilChemicalAnalysis"
      />

      <div class="row" style="float:right; margin: 20px">
        <q-btn
          style="margin-right: 10px"
          :label="$t('cancel')"
          @click="$router.go(-1)"
        ></q-btn>
        <q-btn
          style="margin-right: 10px"
          :label="$t('save_and_back')"
          @click="onSaveAndBackChemicalAnalysis"
        ></q-btn>
        <q-btn
          style="margin-right: 10px"
          :label="$t('save')"
          @click="onSaveChemicalAnalysis"
        ></q-btn>
      </div>
    </div>
  </div>
</template>

<script>
import SoilDegreeTable from "../components/list/soil-deep-table.vue";
import SoilChemicalAnalysis from "../components/editors/soil-chemical-analysis.vue";

export default {
  name: "muster-soil",
  data: function() {
    return {
      muster_soil: {},
      farms: [],
      salt_degrees: [],
      crop_types: [],
      selected_farm: null,
      wells: [],
      soil_chemical_analysis: {}
    };
  },

  watch: {
    selected_farm: function(new_farm) {
      this.$axios.get("well_by_farm/" + new_farm).then(response => {
        //this.muster_soil.well = null;
        this.wells = response.data;
      });
    }
  },

  methods: {
    async initialize() {
      await this.$axios.get("/farms_by_user_district").then(response => {
        this.farms = response.data;
      });
      await this.$axios.get("/salt_degree_request").then(response => {
        this.salt_degrees = response.data;
      });
      await this.$axios.get("/crop_type_request").then(response => {
        this.crop_types = response.data;
      });

      if (this.$route.params.id == 0) {
        this.muster_soil = this.$helper.muster_soil();
      } else {
        this.$axios
          .get("/muster_soil_request/" + this.$route.params.id)
          .then(async response => {
            this.muster_soil = response.data;
            this.selected_well = await this.$helper.get_well(
              this.muster_soil.well
            );
            this.selected_farm = this.selected_well.farm;
          });
        this.$axios
          .get("analysis_soil_request/" + this.$route.params.id)
          .then(response => {
            this.soil_chemical_analysis = response.data[0];
          });
      }
    },
    required(name) {
      let value = this.muster_soil[name];
      if (!value) return this.$t("required").format_letter();
      if (value < 0) return this.$t("not_higher_zero").format_letter();
      return true;
    },
    hasError() {
      return this.$refs["form"].validate();
    },

    onSaveAndBack() {
      this.onSave();
      this.$router.go(-1);
    },
    onSave() {
      this.hasError().then(error_status => {
        if (error_status == true) {
          this.$helper.saveInstance(this.muster_soil, "muster_soil_request");
        }
      });
    },

    onSaveAndBackChemicalAnalysis() {
      this.onSaveChemicalAnalysis();
      this.$router.go(-1);
    },
    onSaveChemicalAnalysis() {
      this.$refs["refSoilChemicalAnalysis"].hasError().then(error_status => {
        if (error_status == true) {
          this.$helper.saveInstance(
            this.soil_chemical_analysis,
            "analysis_soil_request"
          );
        }
      });
    },

    required(name) {
      let value = this.muster_soil[name];
      if (!value) return this.$t("required").format_letter();
      if (value < 0) return this.$t("not_higher_zero").format_letter();
      return true;
    },
    IsPermission(val) {
      for (let i = 0; i < this.$store.state.auth.user_permissions.length; i++) {
        let item = this.$store.state.auth.user_permissions[i];
        if (item == val) return true;
      }
      return false;
    }
  },
  beforeMount() {
    this.initialize();
  },
  components: {
    SoilDegreeTable,
    SoilChemicalAnalysis
  }
};
</script>

<style lang="scss" scoped></style>>
