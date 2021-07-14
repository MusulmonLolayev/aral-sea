<template>
  <div>
    <q-list bordered class="rounded-borders">
      <div class="row">
        <div class="col-5" style="margin: 20px">
          <strong>{{title}}</strong>
        </div>
      </div>
      <q-expansion-item
        expand-separator
        default-opened
        icon="live_help"
        :label="$t('musters').format_letter()"
        dense
      >
        <div style="margin: 10px">
          <muster-pumping-table :well_id="$route.params.id" />
        </div>
      </q-expansion-item>

      <q-expansion-item
        expand-separator
        default-opened
        icon="live_help"
        :label="$t('ugv').format_letter()"
        dense
      >
        <div style="margin: 10px">
          <ugv-table :well_id="$route.params.id" />
        </div>
      </q-expansion-item>

      <q-expansion-item
        expand-separator
        default-opened
        icon="live_help"
        :label="$t('mgv').format_letter()"
        dense
      >
        <div style="margin: 10px">
          <mgv-table :well_id="$route.params.id" />
        </div>
      </q-expansion-item>
    </q-list>
  </div>
</template>

<script>
import MusterPumpingTable from "../components/list/muster-pumping-table";
import UgvTable from "../components/list/ugv-table";
import MgvTable from "../components/list/mgv-table";
export default {
  data() {
    return {
      title: "",
      well: {},
    };
  },

  methods: {
    initialize() {
      if (this.$store.state.well.well != null) {
        this.well = this.$store.state.well.well;
        this.title = this.well.number + " " + this.well.farm_name;
      } else {
        this.$axios
          .get("/well_request/" + this.$route.params.id)
          .then(response => {
            this.well = response.data;
            this.title = this.well.number + " " + this.well.farm_name;
          });
      }
    },
  },

  beforeMount() {
    //this.initialize();
  },
  mounted() {
    this.initialize();
  },
  meta() {
    return {
      title: this.title,
    };
  },

  components: { MusterPumpingTable, UgvTable, MgvTable},
};
</script>

<style>
</style>