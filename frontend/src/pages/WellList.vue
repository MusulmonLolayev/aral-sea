<template>
  <div class="q-pa-md">
    <q-table
      :title="$t('wells').format_letter()"
      :data="filtered_items"
      :columns="$store.state.common.WellList_Colunms"
      row-key="id"
      :filter="filter"
      :no-data-label="$t('nothingtoshow').format_letter()"
      :rows-per-page-label="$t('rows_per_page_label') + ':'"
      :selected-rows-label="$helper.getSelectedString"
      :pagination-label="$helper.get_pagination_label"
      :selection="!IsPermission('change_well') ? 'single' : 'multiple'"
      :selected.sync="well_selected"
    >
      <template v-slot:top-right="props">
        <div class="row">
          <q-btn-group style="margin-right: 30px; margin-top: 5px" flat>
            <q-btn
              icon="add"
              @click="add_new_well"
              v-if="IsPermission('add_well')"
            >
              <q-tooltip>{{ $t("new_item").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="add"
              @click="addMuster"
              v-if="IsPermission('add_musterpumping')"
              :disable="well_selected.length != 1"
            >
              <q-tooltip>{{ $t("new_item").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="details"
              @click="goDetail"
              v-if="IsPermission('view_well')"
              :disable="well_selected.length != 1"
            >
              <q-tooltip>{{ $t("go_detail").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="edit"
              @click="editItem"
              v-if="IsPermission('change_well')"
              :disable="well_selected.length != 1"
            >
              <q-tooltip>{{ $t("edit").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="delete"
              @click="deleteItem"
              v-if="IsPermission('delete_well')"
              :disable="well_selected.length != 1"
            >
              <q-tooltip>{{ $t("delete").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="group_work"
              @click="attach_to_technician"
              v-if="IsPermission('change_well')"
              :disable="well_selected.length <= 0"
            >
              <q-tooltip>{{
                $t("attach_to_technician").format_letter()
              }}</q-tooltip>
            </q-btn>
            <q-btn icon="update" @click="updateDate">
              <q-tooltip>{{ $t("update_data").format_letter() }}</q-tooltip>
            </q-btn>
          </q-btn-group>
          <q-select
            v-if="user_role == 2"
            :options="farms"
            :display-value="$t('farms').format_letter()"
            v-model="selectedFarms"
            option-label="name"
            options-cover
            style="min-width: 150px; margin-right: 20px"
            @input="farmsChanged"
          />

          <q-select
            :options="farms"
            :label="$t('farms').format_letter()"
            v-model="selectedFarms"
            option-label="name"
            options-cover
            style="min-width: 150px; margin-right: 20px"
            @input="farmsChanged"
          />
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
    <q-dialog v-model="dialog">
      <q-card>
        <q-card-section>
          <span class="headline">{{ formTitle.format_letter() }}</span>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-pt-none">
          <well :well="new_well" ref="refWell" v-if="dialog_type == 0" />
          <muster-pumping
            :muster_pumping="new_muster"
            ref="refMuster"
            v-else-if="dialog_type == 1"
          />
          <q-select
            v-model="selected_technician"
            use-input
            input-debounce="0"
            :options="technician_options"
            :label="$t('choose_technician').format_letter()"
            @filter="filterFn"
            style="width: 350px; margin: 20px"
            v-else
            :option-label="
              item =>
                item.last_name + ` ` + item.first_name + ` ` + item.middle_name
            "
          >
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey"> No results </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            color="blue darken-1"
            dense
            @click="close"
            :label="$t('cancel').format_letter()"
          />
          <q-btn
            color="blue darken-1"
            dense
            @click="save"
            :label="
              dialog_type == 2
                ? $t('attach_to_technician').format_letter()
                : $t('save').format_letter()
            "
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import MusterPumping from "../components/editors/muster-pumping";
import Well from "../components/editors/well";
export default {
  name: "PatientList",
  data() {
    return {
      filter: "",
      items: [],
      filtered_items: [],
      dialog: false,
      new_muster: {},
      model_name: "well",
      app_name: "main",
      has_add_musterpump: false,
      // if 0 => edit, or new well, 1 => edit or mew pumpping muster, 2 => choose the techinician for attach well
      dialog_type: 0,
      new_well: {},
      user_role: this.$store.state.auth.user_role,
      selectedFarms: {},
      farms: [],
      well_selected: [],
      request_url: "well_request",
      technicians: [],
      selected_technician: {},
      technician_options: []
    };
  },

  computed: {
    formTitle() {
      if (this.dialog_type == 2) return this.$t("choose_technician");
      return this.editedIndex === -1 ? this.$t("new_item") : this.$t("editing");
    },
    IsSelectedItem() {
      return this.selectedItems.length;
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  methods: {
    initialize() {
      this.updateDate();
      this.$axios.get("/farm_request/0").then(response => {
        this.farms = response.data;
        this.selectedFarms = this.farms[0];
      });
    },

    farmsChanged(value) {
      this.filter = null;
      this.filtered_items = [];
      for (let i = 0; i < this.items.length; i++) {
        if (this.items[i].farm == value.id) {
          this.filtered_items.push(this.items[i]);
        }
      }
    },

    goDetail() {
      let well = this.well_selected[0];
      this.$store.dispatch("well/setCurrentWell", {
        well: well
      });
      this.$router.push("wells/" + well.id);
    },

    async updateDate() {
      await this.$axios.get("/well_request").then(response => {
        this.items = response.data;
        this.farmsChanged(this.selectedFarms);
      });
    },

    editItem() {
      let item = this.well_selected[0];
      this.editedIndex = this.filtered_items.indexOf(item);
      this.new_well = item;
      this.dialog = true;
    },

    async save() {
      if (this.dialog_type == 0) {
        let hasError = await this.$refs.refWell.hasError().then(success => {
          return success;
        });
        if (!hasError) {
          this.$q.notify({
            message: this.$t("fill_all_fields").format_letter(),
            color: "red",
            icon: "error",
            actions: [
              { label: this.$t("close").format_letter(), color: "white" }
            ]
          });
          return;
        }

        let response = await this.$helper.saveInstance(
          this.new_well,
          "/well_request"
        );
        if (response == true) {
          this.items.push(Object.assign({}, this.new_well));
          if (this.new_well.id == 0)
            this.filtered_items.push(Object.assign({}, this.new_well));
          this.close();
        }
        this.$helper.DealSavingRespone(response);
      } else if (this.dialog_type == 1) {
        let hasError = await this.$refs.refMuster.hasError().then(success => {
          return success;
        });
        if (!hasError) {
          this.$q.notify({
            message: this.$t("fill_all_fields").format_letter(),
            color: "red",
            icon: "error",
            actions: [
              { label: this.$t("close").format_letter(), color: "white" }
            ]
          });
          return;
        }

        let response = await this.$helper.saveInstance(
          this.new_muster,
          "/muster_pumping_request"
        );
        if (response == true) {
          this.close();
        }
        this.$helper.DealSavingRespone(response);
      } else {
        this.$axios
          .put("attach_well_to_technician", {
            technician: this.selected_technician.id,
            wells: this.well_selected.map(item => item.id)
          })
          .then(response => {
            this.$q.notify({
              message: this.$t("attached").format_letter(),
              color: "blue",
              icon: "success",
              actions: [
                { label: this.$t("close").format_letter(), color: "white" }
              ]
            });
            this.well_selected = [];
            this.dialog = false;
          })
          .catch(error => {});
      }
    },

    addMuster() {
      let well_id = this.well_selected[0].id;
      this.dialog_type = 1;
      this.new_muster = Object.assign({}, this.$helper.muster_pumping());

      this.new_muster.well = well_id;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },

    add_new_well() {
      this.dialog_type = 0;
      this.new_well = Object.assign({}, this.$helper.well());
      this.dialog = true;
    },

    async deleteItem() {
      let item = this.well_selected[0];
      this.$q
        .dialog({
          title: this.$t("confirm").format_letter(),
          message: this.$t("would_like_delete").format_letter(),
          cancel: true,
          persistent: true
        })
        .onOk(async () => {
          const index = this.filtered_items.indexOf(item);
          let response = await this.$helper.deleteInstance(
            item,
            this.request_url
          );
          if (response == true) {
            this.filtered_items.splice(index, 1);
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
            this.well_selected = [];
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

    attach_to_technician() {
      this.dialog_type = 2;
      this.new_well = Object.assign({}, this.$helper.well());
      if (this.technician_options.length == 0) {
        this.$axios.get("get_technicians").then(response => {
          this.technicians = response.data;
          this.selected_technician = response.data[0];
          this.technician_options = this.technicians;
          this.dialog = true;
        });
      } else {
        this.selected_technician = this.technician_options[0];
        this.technician_options = this.technicians;
        this.dialog = true;
      }
    },

    filterFn(val, update) {
      if (val === "") {
        update(() => {
          this.technician_options = this.technicians;
        });
        return;
      }

      update(() => {
        const needle = val.toLowerCase();
        this.technician_options = this.technicians.filter(
          v =>
            (v.last_name + " " + v.first_name + " " + v.middle_name)
              .toLowerCase()
              .indexOf(needle) > -1
        );
      });
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
    MusterPumping,
    Well
  }
};
</script>

<style scop></style>
