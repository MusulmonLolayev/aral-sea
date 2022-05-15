<template>
  <div style="margin: 15px">
    <div class="layout-padding">
      <q-table
        :data="items"
        :title="$t('soil_analysis_list').format_letter()"
        :columns="headers"
        row-key="id"
        :loading="loading"
        :filter="filter"
        :pagination.sync="pagination"
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
            <div class="col-4">
              <q-select
                :label="$t('select_district').format_letter()"
                :options="districts"
                option-value="id"
                option-label="name"
                emit-value
                map-options
                v-model="sel_district"
                style="margin-right: 30px"
                :rules="[selected => selected != null]"
                dense
                @input="onChangedDistrict"
              />
            </div>
            <div class="col-3">
              <q-btn-group style="margin-right: 30px; margin-top: 5px" flat>
                <q-btn
                  icon="add"
                  to="/soil/0"
                  dense
                  v-if="IsPermission('add_mgv')"
                >
                  <q-tooltip>{{ $t("new_item").format_letter() }}</q-tooltip>
                </q-btn>
                <q-btn
                  icon="edit"
                  :disable="!IsSelectedItem"
                  @click="onGoDetail"
                  dense
                  v-if="
                    IsPermission('change_mgv') ||
                      IsPermission('view_mustersoil')
                  "
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
            </div>
            <div class="col-3">
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
          </div>
        </template>

        <template v-slot:pagination>
          <q-btn
            icon="chevron_left"
            color="grey-8"
            round
            dense
            flat
            :disable="pagination.page == 1"
            @click="onPrevPage"
          />
          <q-btn
            icon="chevron_right"
            color="grey-8"
            round
            dense
            flat
            :disable="pagination.page == pagination.pagesCount"
            @click="onNextPage"
          />
        </template>
      </q-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "MusterSoilList",
  data: () => ({
    filter: "",
    loading: false,
    pagination: {
      sortBy: "desc",
      descending: false,
      page: 1,
      rowsPerPage: 50,
      rowsNumber: 10,
      pagesCount: 1
    },
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
    districts: [],
    sel_district: {}
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

      await this.$axios.get("/get_user_district").then(response => {
        this.districts = response.data;
        this.sel_district = this.districts[0].id;
      });

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
    onGoDetail() {
      let item = this.selectedItems[0];
      this.$router.push("soil/" + item.id);
    },
    onUpdate() {
      this.Update();
    },

    Update() {
      this.items = [];
      this.loading = true;
      this.$axios
        .get(
          "muster_soil_request/pagination/?page={0}&district={1}".format(
            this.pagination.page,
            this.sel_district
          )
        )
        .then(async respone => {
          this.pagination.pagesCount = respone.data["pagesCount"];

          let well_ids = [];

          respone.data.results.map(item => {
            well_ids.push(item["well"]);
          });

          let wells = await this.$helper.get_wells(well_ids);

          let farm_ids = [];
          wells.map(item => {
            farm_ids.push(item.farm);
          });
          let farms = await this.$helper.get_farms(farm_ids);

          await respone.data.results.map(async item => {
            item["salt_degree"] = this.salt_degrees.find(
              x => x.id === item["salt_degree"]
            );
            item["crop_type"] = this.crop_types.find(
              x => x.id === item["crop_type"]
            );
            item["well"] = await wells.find(well => well.id == item["well"]);
            item["farm"] = await farms.find(
              farm => farm.id == item["well"].farm
            );
            this.items.push(item);
          });

          this.loading = false;
        })
        .catch(error => {});
    },

    onPrevPage() {
      this.pagination.page--;
      this.Update();
    },

    onNextPage() {
      this.pagination.page++;
      this.Update();
    },

    onChangedDistrict(val) {
      this.Update();
    }
  },
  components: {},
  mounted: function() {}
};
</script>

<style></style>
