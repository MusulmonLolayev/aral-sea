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
          <primary-diagnose :primarydiagnose="editedItem" />
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
import PrimaryDiagnose from "../editors/primary-diagnose";

export default {
  data() {
    return {
      dialog: false,
      headers: [],
      items: [],
      selectedItems: [],
      editedIndex: -1,
      editedItem: this.$helper.defPrimayObject(),
      defaultItem: null,
      CLINICAL_FORMS: []
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
    async initialize() {
      this.headers = [
        {
          label: this.$t("clinical_form_of_tuberculosis"),
          field: row =>
            row.clinicalform != null
              ? this.CLINICAL_FORMS.find(item => item.id == row.clinicalform)
                  .name
              : this.$t("unknown")
        },
        {
          label: this.$t("right_lung_top"),
          field: row => this.$helper.ToYesNoUnknown(row.right_lung_top)
        },
        {
          label: this.$t("right_lung_bottom"),
          field: row => this.$helper.ToYesNoUnknown(row.right_lung_bottom)
        },
        {
          label: this.$t("left_lung_top"),
          field: row => this.$helper.ToYesNoUnknown(row.left_lung_top)
        },
        {
          label: this.$t("left_lung_bottom"),
          field: row => this.$helper.ToYesNoUnknown(row.left_lung_bottom)
        },
        {
          label: this.$t("infiltration"),
          field: row => this.$helper.ToYesNoUnknown(row.infiltration)
        },
        {
          label: this.$t("decay"),
          field: row => this.$helper.ToYesNoUnknown(row.decay)
        },
        {
          label: this.$t("seeding"),
          field: row => this.$helper.ToYesNoUnknown(row.seeding)
        },
        {
          label: this.$t("resorption"),
          field: row => this.$helper.ToYesNoUnknown(row.resorption)
        },
        {
          label: this.$t("bk"),
          field: row => this.$helper.ToPlusMinus(row.bk)
        },
        {
          label: this.$t("status"),
          field: row => this.$helper.ToYesNoUnknown(row.status)
        },
        { label: this.$t("date"), field: "date" }
      ];
      await this.$axios.get("/clinicalforms").then(respone => {
        this.CLINICAL_FORMS = respone.data;
      });

      let patient_id = this.patient.id;
      if (typeof patient_id == "undefined" || patient_id == null) {
        patient_id = this.$route.params.id;
      }
      this.$axios.get("/primary_request/" + patient_id).then(respone => {
        this.items = respone.data;
        for (let i = this.items.length - 1; i > -1; i--) {
          if (this.items[i].status == true) {
            let primary_diagnose = Object.create(this.items[i]);
            primary_diagnose.clinicalform_name = this.CLINICAL_FORMS.find(
              element => element.id == primary_diagnose.clinicalform
            ).name;
            this.$store.dispatch("patient/setCurrentPrimary", {
              primary_diagnose: primary_diagnose
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
          let deletedItem = this.selectedItems[0];

          const index = this.items.indexOf(deletedItem);
          let response = await this.$helper.deleteInstance(
            deletedItem,
            "/primary_request"
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
        "/primary_request"
      );
      if (response == true) {
        if (this.editedIndex > -1) {
          Object.assign(this.items[this.editedIndex], this.editedItem);
        } else {
          this.items.push(this.editedItem);
        }
        if (this.editedItem.status == true) {
          let primary_diagnose = Object.create(this.editedItem);
          primary_diagnose.clinicalform_name = this.CLINICAL_FORMS.find(
            element => element.id == primary_diagnose.clinicalform
          ).name;
          this.$store.dispatch("patient/setCurrentPrimary", {
            primary_diagnose: primary_diagnose
          });
        }
        this.close();
      }

      if (response == true) {
        this.$q.notify({
          message: this.$t("saved"),
          color: "blue",
          icon: "success",
          actions: [{ label: this.$t("close"), color: "white" }]
        });
      } else {
        this.$q.notify({
          message: this.$t("unsaved"),
          color: "red",
          icon: "error",
          actions: [{ label: this.$t("close"), color: "white" }]
        });
      }
    },

    btnNewItem() {
      this.defaultItem = this.$helper.defPrimayObject();
      this.editedItem = Object.assign({}, this.defaultItem);
      this.editedItem.patient = this.patient.id;
      this.dialog = true;
    }
  },
  components: {
    PrimaryDiagnose
  },
  mounted: function() {}
};
</script>
