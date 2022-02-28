<template>
  <div style="margin: 15px">
    <h4 style="margin: 10px">{{ $t("application_6a").format_letter() }}</h4>
    <q-separator color="orange" />
    <div class="row">
      <div class="col-5">
        <q-select
          :label="$t('select_district').format_letter()"
          :options="districts"
          option-value="id"
          option-label="name"
          emit-value
          map-options
          v-model="district"
          style="margin-right: 30px"
          :rules="[selected => selected != null]"
        />
      </div>

      <div class="col-2">
        <q-input
          v-model="selected_date"
          :label="$t('select_date').format_letter()"
          type="date"
        />
      </div>

      <div class="col-2" style="margin-top: 20px; margin-left:30px;">
        <q-btn @click="onReport6a" icon="leaderboard">
          {{ $t("report") }}
        </q-btn>
      </div>
    </div>

    <h4 style="margin: 10px">{{ $t("soil_analysis_report").format_letter() }}</h4>
    <q-separator color="orange" />
    <div class="row">
      <div class="col-5">
        <q-select
          :label="$t('select_district').format_letter()"
          :options="districts"
          option-value="id"
          option-label="name"
          emit-value
          map-options
          v-model="district"
          style="margin-right: 30px"
          :rules="[selected => selected != null]"
        />
      </div>

      <div class="col-2">
        <q-input
          v-model="selected_date"
          :label="$t('select_date').format_letter()"
          type="date"
        />
      </div>

      <div class="col-2" style="margin-top: 20px; margin-left:30px;">
        <q-btn @click="onReportSoilAnalysis" icon="leaderboard">
          {{ $t("report") }}
        </q-btn>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Report",
  data: function() {
    return {
      selected_date: this.$helper.GetCurrentDate(),
      district: 0,
      districts: []
    };
  },
  methods: {
    async initialize() {
      this.$axios.get("get_user_district").then(response => {
        this.districts = response.data;
        this.district = this.districts[0].id;
      });
    },

    IsPermission(val) {
      for (let i = 0; i < this.$store.state.auth.user_permissions.length; i++) {
        let item = this.$store.state.auth.user_permissions[i];
        if (item == val) return true;
      }
      return false;
    },

    onReport6a() {
      this.$axios
        .get("report-6a/" + this.district + "/" + this.selected_date, {responseType: 'blob'})
        .then(response => {
          var headers = response.headers;
          var blob = new Blob([response.data], {
            type: headers["content-type"]
          });
          var link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          link.download = this.districts.find(item => item.id == this.district).name + ".xlsx";
          link.click();
        });
    },
    onReportSoilAnalysis(){
      this.$axios
        .get("report-soil-analysis/" + this.district + "/" + this.selected_date, {responseType: 'blob'})
        .then(response => {
          var headers = response.headers;
          var blob = new Blob([response.data], {
            type: headers["content-type"]
          });
          var link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          link.download = this.districts.find(item => item.id == this.district).name + ".xlsx";
          link.click();
        });
    }
  },
  beforeMount() {
    this.initialize();
  },
  components: {}
};
</script>

<style lang="scss" scoped></style>>
