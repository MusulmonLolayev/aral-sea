<template>
  <div>
    <q-table
      :data="items"
      :columns="headers"
      dense
      selection="single"
      :selected.sync="selectedItems"
      :no-data-label="$t('nothingtoshow')"
      :rows-per-page-label="$t('rows_per_page_label') + ':'"
      :selected-rows-label="$helper.getSelectedString"
      :pagination-label="$helper.get_pagination_label"
    >
      <template v-slot:top>
        <q-btn icon="add" color="primary" @click="btnNewItem" dense />
        <q-btn
          icon="edit"
          class="q-ml-sm"
          color="primary"
          :disable="!IsSelectedItem"
          @click="editItem"
          dense
        />
        <q-btn
          icon="remove"
          class="q-ml-sm"
          color="primary"
          :disable="!IsSelectedItem"
          @click="deleteItem"
          dense
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
          <muster-pumping :muster_pumping="editedItem" ref="refMuster" />
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
import MusterPumping from "../editors/muster-pumping";

export default {
  name: "MusterTable",
  data: () => ({
    dialog: false,
    headers: [],
    items: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: null,
    selectedItems: [],
    request_url: "/muster_pumping_request",
  }),
  props: ["well_id"],
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

  beforeMount() {
    this.initialize();
  },
  methods: {
    initialize() {
      this.headers = [
        {
          label: this.$t("starting_pumping"),
          field: "starting_pumping",
        },
        {
          label: this.$t("finishing_pumping"),
          field: "finishing_pumping",
        },
        {
          label: this.$t("count_gall"),
          field: "count_gall",
        },
        {
          label: this.$t("size_gall"),
          field: "size_gall",
        },
        {
          label: this.$t("ugv_before_pumping"),
          field: "ugv_before_pumping",
        },
        {
          label: this.$t("ugv_after_pumping"),
          field: "ugv_after_pumping",
        },
        {
          label: this.$t("bottom"),
          field: "bottom",
        },
        {
          label: this.$t("speed_water"),
          field: "speed_water",
        },
        {
          label: this.$t("elevated"),
          field: "elevated",
        },
        {
          label: this.$t("reduced"),
          field: "reduced",
        },
        { label: this.$t("date"), field: "date" },
      ];

      let well_id = this.well_id;
      this.$axios.get(this.request_url + "/" + well_id).then((respone) => {
        respone.data.map((item) => {
          this.items.push(this.toTemplate(item));
        });
      });
    },
    toTemplate(obj) {
      let res = Object.assign({}, obj)
      res['well'] = this.well_id
      return res;
    },
    toObject(obj) {
      let res = Object.assign({}, obj)
      res['well'] = this.well_id
      return res;
    },

    editItem() {
      let item = this.selectedItems[0];
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = this.toObject(item);
      this.dialog = true;
    },
    async deleteItem(item) {
      this.$q
        .dialog({
          title: this.$t("confirm"),
          message: this.$t("would_like_delete"),
          cancel: true,
          persistent: true,
        })
        .onOk(async () => {
          let item = this.selectedItems[0];
          const index = this.items.indexOf(item);
          let response = await this.$helper.deleteInstance(
            item,
            this.request_url
          );
          if (response == true) {
            this.items.splice(index, 1);
            this.selectedItems = [];
          }

          if (response == true) {
            this.$q.notify({
              message: this.$t("deleted"),
              color: "blue",
              icon: "success",
              actions: [{ label: this.$t("close"), color: "white" }],
            });
          } else {
            this.$q.notify({
              message: this.$t("notdeleted"),
              color: "red",
              icon: "error",
              actions: [{ label: this.$t("close"), color: "white" }],
            });
          }
        })
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
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
        this.editedItem,
        this.request_url
      );
      if (response == true) {
        if (this.editedIndex > -1) {
          Object.assign(
            this.items[this.editedIndex],
            this.toTemplate(this.editedItem)
          );
        } else {
          this.items.push(this.toTemplate(this.editedItem));
        }
        this.close();
      }
      this.$helper.DealSavingRespone(response);
    },
    btnNewItem() {
      this.defaultItem = {
        well: this.well_id,
      };
      var d = new Date();

      this.defaultItem.starting_pumping = d.toTimeString().substring(0, 8);
      d.addMins(10);
      this.defaultItem.finishing_pumping = d.toTimeString().substring(0, 8);

      this.defaultItem.count_gall = 0;
      this.defaultItem.size_gall = 0;
      this.defaultItem.ugv_before_pumping = 0;
      this.defaultItem.ugv_after_pumping = 0;
      this.defaultItem.bottom = 0;
      this.defaultItem.speed_water = 0;
      this.defaultItem.elevated = 0;
      this.defaultItem.reduced = 0;
      this.defaultItem.date = this.$helper.GetCurrentDate();

      this.editedItem = Object.assign({}, this.defaultItem);
      this.dialog = true;
    },
  },
  components: {
    MusterPumping,
  },
  mounted: function () {},
};
</script>

<style>
</style>