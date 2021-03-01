<template>
  <div class="q-pa-md">
    <q-table
      grid
      :title="$t('wells')"
      :data="data"
      :columns="$store.state.common.WellList_Colunms"
      row-key="name"
      :filter="filter"
      grid-header
      hide-header
      :no-data-label="$t('nothingtoshow')"
      :rows-per-page-label="$t('rows_per_page_label') + ':'"
      :selected-rows-label="$helper.getSelectedString"
      :pagination-label="$helper.get_pagination_label"
    >
      <template v-slot:top-right="props">
        <div class="row">
          <q-btn
            round
            icon="update"
            style="margin-right: 30px; margin-top: 5px"
            @click="updateDate"
          >
            <q-tooltip content-class="bg-accent">{{
              $t("update_data")
            }}</q-tooltip>
          </q-btn>
          <q-input
            dense
            debounce="300"
            v-model="filter"
            :placeholder="$t('search')"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </template>

      <template v-slot:item="props">
        <q-card style="margin: 5px; min-width: 220px">
          <q-card-section>
            <div class="row items-center no-wrap">
              <div class="col">
                <strong
                  >{{ props.row.farm_name }}&ensp;&ensp;{{
                    props.row.number
                  }}</strong
                >
              </div>

              <div class="col-auto">
                <q-btn color="grey-7" round flat icon="more_vert">
                  <q-menu cover auto-close>
                    <q-list>
                      <q-item clickable @click="goDetail(props.row)">
                        <q-item-section>{{ $t("detail") }}</q-item-section>
                      </q-item>
                      <q-item clickable @click="addMuster(props.row.id)">
                        <q-item-section>{{ $t("add_muster") }}</q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-btn>
              </div>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <table>
              <tr>
                <td>
                  <strong>X:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.x.toFixed(4) }}</td>
              </tr>
              <tr>
                <td>
                  <strong>Y:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.y.toFixed(4) }}</td>
              </tr>
              <tr>
                <td>
                  <strong>{{ $t("built_year") }}:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.built_year }}</td>
              </tr>
              <tr>
                <td>
                  <strong>{{ $t("depth") }}:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.depth }}</td>
              </tr>
              <tr>
                <td>
                  <strong>{{ $t("diameter") }}:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.diameter }}</td>
              </tr>
              <tr>
                <td>
                  <strong>{{ $t("material") }}:</strong>
                </td>
                <td>
                  &ensp;&ensp;{{
                    props.row.material ? $t("polythene") : $t("metal")
                  }}
                </td>
              </tr>
              <tr>
                <td>
                  <strong>{{ $t("area") }}:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.area }}</td>
              </tr>
              <tr>
                <td>
                  <strong>{{ $t("label") }}:</strong>
                </td>
                <td>&ensp;&ensp;{{ props.row.label }}</td>
              </tr>
            </table>
          </q-card-section>
        </q-card>
      </template>
    </q-table>
    <q-dialog v-model="dialog">
      <q-card>
        <q-card-section>
          <span class="headline">{{ formTitle }}</span>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-pt-none">
          <muster :muster="new_muster" ref="refMuster" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            color="blue darken-1"
            dense
            @click="close"
            :label="$t('cancel')"
          />
          <q-btn
            color="blue darken-1"
            dense
            @click="save"
            :label="$t('save')"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import Muster from "../components/editors/muster";
export default {
  name: "PatientList",
  data() {
    return {
      filter: "",
      data: [],
      dialog: false,
      new_muster: {},
    };
  },

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? this.$t("new_item") : this.$t("editing");
    },
    IsSelectedItem() {
      return this.selectedItems.length;
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
  },

  methods: {
    DealSavingRespone(response) {
      if (response == true) {
        this.$q.notify({
          message: this.$t("edited"),
          color: "blue",
          icon: "success",
          actions: [{ label: this.$t("close"), color: "white" }],
        });
      } else {
        this.$q.notify({
          message: this.$t("unedited"),
          color: "red",
          icon: "error",
          actions: [{ label: this.$t("close"), color: "white" }],
        });
      }
    },
    initialize() {
      this.updateDate();
    },

    goDetail(well) {
      this.$store.dispatch("well/setCurrentWell", {
        well: well,
      });
      this.$router.push("detail/" + well.id);
    },

    async updateDate() {
      await this.$axios.get("/well_request/0").then((response) => {
        this.data = response.data;
      });
    },

    editItem() {
      let item = this.selectedItems[0];
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = this.toObject(item);
      this.dialog = true;
    },

    async save() {
      let hasError = await this.$refs.refMuster.hasError().then((success) => {
        return success;
      });
      if (!hasError) {
        this.$q.notify({
          message: this.$t("fill_all_fields"),
          color: "red",
          icon: "error",
          actions: [{ label: this.$t("close"), color: "white" }],
        });
        return;
      }

      let response = await this.$helper.saveInstance(
        this.new_muster,
        "/muster_request"
      );
      if (response == true) {
        this.close();
      }
      this.DealSavingRespone(response);
    },
    
    addMuster(well_id) {
      this.new_muster = {
        depth: 0,
        degree_salt: 0,

        date: this.$helper.GetCurrentDate(),
        well: well_id,
      };
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
  },
  beforeMount() {
    this.initialize();
  },
  components: {
    Muster,
  },
};
</script>

<style scop>
</style>