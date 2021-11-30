<template>
  <div style="margin: 15px">
    <q-table
      :title="$t('soil_analysis_list').format_letter()"
      :data="items"
      :columns="headers"
      dense
      selection="single"
      :selected.sync="selectedItems"
      :no-data-label="$t('nothingtoshow').format_letter()"
      :rows-per-page-label="$t('rows_per_page_label') + ':'"
      :selected-rows-label="$helper.getSelectedString"
      :pagination-label="$helper.get_pagination_label"
    >
      <template v-slot:top-right>
        <div class="row">
          <q-btn-group style="margin-right: 30px; margin-top: 5px" flat>
            <q-btn icon="add" to="/soil/0" dense v-if="IsPermission('add_mgv')">
              <q-tooltip>{{ $t("new_item").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="edit"
              :disable="!IsSelectedItem"
              @click="onGoDetail"
              dense
              v-if="IsPermission('change_mgv') ||  IsPermission('view_mustersoil')"
            >
              <q-tooltip>{{ $t("go_detail").format_letter() }}</q-tooltip>
            </q-btn>

            <q-btn
              icon="remove"
              :disable="!IsSelectedItem"
              @click="deleteItem"
              v-if="IsPermission('delete_mgv')"
            >
              <q-tooltip>{{ $t("delete").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn icon="update" @click="onUpdate">
              <q-tooltip>{{ $t("update_data").format_letter() }}</q-tooltip>
            </q-btn>
          </q-btn-group>
          <q-input
            dense
            v-model="filter"
            :placeholder="$t('search').format_letter()"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </template>
    </q-table>
  </div>
</template>

<script>
export default {
  name: "MusterSoilList",
  data: () => ({
    dialog: false,
    headers: [],
    items: [],
    editedIndex: -1,
    editedItem: {},
    editItem: {},
    defaultItem: null,
    selectedItems: [],
    salt_degrees: [],
    crop_types: [],
    filter: "",
  }),
  computed: {
    IsSelectedItem() {
      return this.selectedItems.length;
    }
  },

  beforeMount() {
    this.initialize();
  },
  methods: {
    async initialize() {
      this.headers = [
        { label: this.$t("farm").format_letter(), field: row => row.farm.name },
        { label: this.$t("contour_no").format_letter(), field: "contour_no" },
        {
          label: this.$t("well_no").format_letter(),
          field: row => row.well.number
        },
        { label: this.$t("pit_no").format_letter(), field: "pit_no" },
        { label: this.$t("area_size").format_letter(), field: "area_size" },
        {
          label: this.$t("salt_degree").format_letter(),
          field: row => row.salt_degree.name
        },
        { label: this.$t("date").format_letter(), field: "date" },
        {
          label: this.$t("crop_type").format_letter(),
          field: row => row.crop_type.name
        },
        { label: this.$t("location_y").format_letter(), field: "location_x" },
        { label: this.$t("location_y").format_letter(), field: "location_y" }
      ];

      await this.$axios.get("salt_degree_request").then(response => {
        this.salt_degrees = response.data;
      });

      await this.$axios.get("crop_type_request").then(response => {
        this.crop_types = response.data;
      });

      this.Update();
    },

    async deleteItem(item) {
      this.$q
        .dialog({
          title: this.$t("confirm").format_letter(),
          message: this.$t("would_like_delete").format_letter(),
          cancel: true,
          persistent: true
        })
        .onOk(async () => {
          let item = this.selectedItems[0];
          const index = this.items.indexOf(item);
          let response = await this.$helper.deleteInstance(item, "mgv_request");
          if (response == true) {
            this.items.splice(index, 1);
            this.selectedItems = [];
          }

          if (response == true) {
            this.$q.notify({
              message: this.$t("deleted").format_letter(),
              color: "blue",
              icon: "success",
              actions: [
                { label: this.$t("close").format_letter(), color: "white" }
              ]
            });
          } else {
            this.$q.notify({
              message: this.$t("notdeleted").format_letter(),
              color: "red",
              icon: "error",
              actions: [
                { label: this.$t("close").format_letter(), color: "white" }
              ]
            });
          }
        });
    },

    IsPermission(val) {
      for (let i = 0; i < this.$store.state.auth.user_permissions.length; i++) {
        let item = this.$store.state.auth.user_permissions[i];
        if (item == val) return true;
      }
      return false;
    },
    onGoDetail(){
      let item = this.selectedItems[0];
      this.$router.push("soil/" + item.id);
    },
    onUpdate(){
      this.Update();
    },

    Update(){
      this.items = []
      this.$axios.get("muster_soil_request").then(respone => {
        respone.data.map(async item => {
          item["salt_degree"] = this.salt_degrees.find(
            x => x.id === item["salt_degree"]
          );
          item["crop_type"] = this.crop_types.find(
            x => x.id === item["crop_type"]
          );
          item["well"] = await this.$helper.get_well(item["well"]);
          item["farm"] = await this.$helper.get_farm(item["well"].farm);
          this.items.push(item);
        });
      });
    }
  },
  components: {},
  mounted: function() {}
};
</script>

<style></style>
