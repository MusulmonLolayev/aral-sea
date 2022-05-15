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

      <q-expansion-item
        expand-separator
        default-opened
        icon="live_help"
        :label="$t('the_last_info').format_letter()"
        dense
      >
        <div style="margin: 10px">
          {{$t('date_time').format_letter()}} : {{tool_data.date_time}} <br>
          {{$t('well_water_degree').format_letter()}} : {{tool_data.degree}} <br>
          {{$t('well_water_salinity').format_letter()}} : {{tool_data.salinity}} <br>
          {{$t('well_water_temperature').format_letter()}} : {{tool_data.temperature}} <br>
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
      tool_data: {
        date_time: '',
        degree: '',
        salinity: '',
        temperature: '',
      },
    };
  },

  methods: {
    initialize() {
      if (this.$store.state.well.well != null) {
        this.well = this.$store.state.well.well;
        this.title = this.well.number + " " + this.well.farm_name;
        this.get_tool_data()
        setInterval(this.get_tool_data, 60000)
      } else {
        this.$axios
          .get("/well_request/" + this.$route.params.id)
          .then(response => {
            this.well = response.data;
            this.title = this.well.number + " " + this.well.farm_name;
            this.get_tool_data()
            setInterval(this.get_tool_data, 60000)
          });
      }
    },
    get_tool_data(){
      if (this.well.imei != ''){
        this.$axios
          .get('/well_tool_data/' + this.well.imei)
          .then(response => {
            if (response.data != 'Not found'){
              this.tool_data.date_time = response.data['date_time']
              this.tool_data.degree = response.data['degree']
              this.tool_data.salinity = response.data['salinity']
              this.tool_data.temperature = response.data['temperature']
            }
          })
      }

      //setTimeout(this.get_tool_data(), 50000)
    }
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