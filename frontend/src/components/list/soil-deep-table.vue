<template>
  <div>
    <q-table
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
      <template v-slot:top>
        <q-btn
          icon="add"
          color="primary"
          @click="btnNewItem"
          dense
          v-if="IsPermission('add_soildeep')"
        />
        <q-btn
          icon="edit"
          class="q-ml-sm"
          color="primary"
          :disable="!IsSelectedItem"
          @click="editItem"
          dense
          v-if="IsPermission('change_soildeep')"
        />
        <q-btn
          icon="remove"
          class="q-ml-sm"
          color="primary"
          :disable="!IsSelectedItem"
          @click="deleteItem"
          dense
          v-if="IsPermission('delete_soildeep')"
        />
      </template>
    </q-table>

    <q-dialog v-model="dialog">
      <q-card>
        <q-card-section>
          <span class="headline">{{ formTitle }}</span>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-pt-none">
          <soil-deep :soil_deep="editedItem" ref="refSoilDeep" />
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
            :label="$t('save').format_letter()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import SoilDeep from "../editors/soil-deep.vue";

export default {
  name: "SoilDeepTable",
  props: ["muster_soil", "SaveMusterSoil"],
  data: () => ({
    dialog: false,
    headers: [],
    items: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: null,
    selectedItems: [],
    soil_types: []
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1
        ? this.$t("new_item").format_letter()
        : this.$t("editing").format_letter();
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

  beforeMount() {
    this.initialize();
  },
  methods: {
    initialize() {
      this.headers = [
        {
          label: this.$t("from_deep").format_letter(),
          field: "from_deep"
        },
        {
          label: this.$t("to_deep").format_letter(),
          field: "to_deep"
        },
        {
          label: this.$t("soil_type").format_letter(),
          field: row =>
            this.soil_types.find(item => item.id === row.soil_type).name
        }
      ];

      this.$axios.get("soil_type_request").then(response => {
        this.soil_types = response.data;
      });

      if (this.$route.params.id != 0) {
        this.$axios
          .get("/soil_deep_request/" + this.$route.params.id)
          .then(response => {
            this.items = response.data;
          });
      }
    },

    editItem() {
      let item = this.selectedItems[0];
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = item;
      this.dialog = true;
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
          let response = await this.$helper.deleteInstance(
            item,
            "soil_deep_request"
          );
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
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    async save() {
      let hasError = await this.$refs.refSoilDeep.hasError().then(success => {
        return success;
      });
      if (!hasError) {
        this.$q.notify({
          message: this.$t("fill_all_fields").format_letter(),
          color: "red",
          icon: "error",
          actions: [{ label: this.$t("close").format_letter(), color: "white" }]
        });
        return;
      }

      let response = await this.$helper.saveInstance(
        this.editedItem,
        "soil_deep_request"
      );
      if (response == true) {
        if (this.editedIndex > -1) {
          Object.assign(this.items[this.editedIndex], this.editedItem);
        } else {
          this.items.push(this.editedItem);
        }
        this.close();
      }
      this.$helper.DealSavingRespone(response);
    },

    btnNewItem() {
      if (this.muster_soil.id == 0) {
        let message_text =
          this.$t("please_save").format_letter() +
          ". " +
          this.$t("would_like_save").format_letter() +
          ". " +
          this.$t("re_add_again").format_letter();
        this.$q
          .dialog({
            title: this.$t("muster_soil_unsaved").format_letter(),
            message: message_text,
            cancel: true,
            persistent: true
          })
          .onOk(() => {
            this.SaveMusterSoil();
          });
        return 0;
      }
      this.defaultItem = this.$helper.soil_deep();
      this.defaultItem.muster_soil = this.muster_soil.id;
      this.editedItem = Object.assign({}, this.defaultItem);
      this.dialog = true;
    },

    IsPermission(val) {
      for (let i = 0; i < this.$store.state.auth.user_permissions.length; i++) {
        let item = this.$store.state.auth.user_permissions[i];
        if (item == val) return true;
      }
      return false;
    }
  },
  components: {
    SoilDeep
  },
  mounted: function() {}
};
</script>

<style></style>
