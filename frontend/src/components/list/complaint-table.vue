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
          <Complaint :complaint="editedItem" />
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
import Complaint from "../editors/complaint";

export default {
  name: "ComplaintTable",
  data() {
    return {
      dialog: false,
      headers: [],
      items: [],
      editedIndex: -1,
      editedItem: this.$helper.defComplaintObject(),
      defaultItem: null,
      selectedItems: []
    };
  },
  props: ["patient"],
  computed: {
    formTitle() {
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

  beforeMount() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.headers = [
        {
          label: this.$t("diarrhea"),
          field: row => this.$helper.ToYesNoUnknown(row.diarrhea)
        },
        {
          label: this.$t("normal_stool"),
          field: row => this.$helper.ToYesNoUnknown(row.normal_stool)
        },
        {
          label: this.$t("constipation"),
          field: row => this.$helper.ToYesNoUnknown(row.constipation)
        },
        {
          label: this.$t("character"),
          field: row => this.$helper.ToCharacter(row.character)
        },
        {
          label: this.$t("flatulence"),
          field: row => this.$helper.ToYesNoUnknown(row.flatulence)
        },
        {
          label: this.$t("stomachache"),
          field: row => this.$helper.ToYesNoUnknown(row.stomachache)
        },
        {
          label: this.$t("stool_frequency"),
          field: "stool_frequency"
        },
        {
          label: this.$t("tolerance"),
          field: row => this.$helper.ToYesNoUnknown(row.tuberculosis_tolerance)
        },
        {
          label: this.$t("related_disease"),
          field: row => this.$helper.ToYesNoUnknown(row.related_disease)
        },
        {
          label: this.$t("nausea"),
          field: row => this.$helper.ToYesNoUnknown(row.nausea)
        },
        {
          label: this.$t("vomiting"),
          field: row => this.$helper.ToYesNoUnknown(row.vomiting)
        },
        {
          label: this.$t("headache"),
          field: row => this.$helper.ToYesNoUnknown(row.headache)
        },
        {
          label: this.$t("sweating"),
          field: row => this.$helper.ToYesNoUnknown(row.sweating)
        },
        {
          label: this.$t("weakness"),
          field: row => this.$helper.ToYesNoUnknown(row.weakness)
        },
        {
          label: this.$t("allergodermatosis"),
          field: row => this.$helper.ToYesNoUnknown(row.allergodermatosis)
        },
        {
          label: this.$t("weight_lose"),
          field: "weight_lose"
        },
        {
          label: this.$t("status"),
          field: row => this.$helper.ToYesNoUnknown(row.status)
        },
        { label: this.$t("date"), field: "date" }
      ];

      let patient_id = this.patient.id;
      if (typeof patient_id == "undefined" || patient_id == null) {
        patient_id = this.$route.params.id;
      }
      this.$axios.get("/complaint_request/" + patient_id).then(respone => {
        //console.log(respone);
        this.items = respone.data;

        for (let i = this.items.length - 1; i > -1; i--) {
          if (this.items[i].status == true) {
            this.$store.dispatch("patient/setCurrentComplaint", {
              complaint: this.items[i]
            });
            break;
          }
        }
      });
    },

    editItem() {
      let item = this.selectedItems[0];
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    async deleteItem() {
      this.$q
        .dialog({
          title: this.$t("confirm"),
          message: this.$t("would_like_delete"),
          cancel: true,
          persistent: true
        })
        .onOk(async () => {
          let item = this.selectedItems[0];
          const index = this.items.indexOf(item);
          let response = await this.$helper.deleteInstance(
            item,
            "/complaint_request"
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
              actions: [{ label: this.$t("close"), color: "white" }]
            });
          } else {
            this.$q.notify({
              message: this.$t("notdeleted"),
              color: "red",
              icon: "error",
              actions: [{ label: this.$t("close"), color: "white" }]
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
      let response = await this.$helper.saveInstance(
        this.editedItem,
        "/complaint_request"
      );
      if (response == true) {
        if (this.editedIndex > -1) {
          Object.assign(this.items[this.editedIndex], this.editedItem);
        } else {
          this.items.push(this.editedItem);
        }
        if (this.editedItem.status == true) {
          let editedItem = Object.assign({}, this.editedItem)
          this.$store.dispatch("patient/setCurrentComplaint", {
            complaint: editedItem
          });
        }
        this.close();
      }
      this.$helper.DealSavingRespone(response);
    },
    btnNewItem() {
      this.defaultItem = this.$helper.defComplaintObject();
      this.editedItem = Object.assign({}, this.defaultItem);
      this.editedItem.patient = this.patient.id;
      this.dialog = true;
    }
  },
  components: {
    Complaint
  },
  mounted: function() {}
};
</script>

<style></style>
