<template>
  <div>
    <q-table
      :data="items"
      :columns="headers"
      dense
      selection="single"
      :selected.sync="selectedItems"
      :no-data-label="$t('nothingtoshow')"
      :rows-per-page-label="$t('rows_per_page_label')+':'"
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
          <initial-questions :selected="editedItem" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn color="blue darken-1" dense @click="close" :label="$t('cancel')" />
          <q-btn color="blue darken-1" dense @click="save" :label="$t('save')" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import InitialQuestions from "../editors/init-questions";
export default {
  name: "v-intial-question-table",
  data: () => ({
    dialog: false,
    headers: [],
    items: [],
    editedIndex: -1,
    selectedItems: [],
    editedItem: {},
    defaultItem: {
      checkbox: [],
      radio: {},

      //date: new Date(),
      status: false,
      //patient: this.patient.id
    },
    question_titles: [],
    questions: [],
  }),
  props: ["patient"],
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? this.$t("new_item") : $t("editing");
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
    toRow(item) {
      let ids = item.questions.split(",");
      let row = {};
      if (ids.length > 1)
        ids.map((id) => {
          let question = Object.assign(
            {},
            this.questions.find((q) => q.id == id)
          );
          let attribut = "v" + question.question_title;
          if (typeof row[attribut] == "undefined") {
            row[attribut] = question;
          } else {
            row[attribut].text += "; " + question.text;
            row[attribut].id += "," + question.id;
          }
        });
      else {
        let id = item.questions;
        let question = Object.assign(
          {},
          this.questions.find((q) => q.id == id)
        );
        let attribut = "v" + question.question_title;
        if (typeof row[attribut] == "undefined") {
          row[attribut] = question;
        } else {
          row[attribut].text += "; " + question.text;
          row[attribut].id += "," + question.id;
        }
      }
      row["id"] = item.id;
      row["status"] = item.status;
      row["date"] = item.date;
      return row;
    },
    async initialize() {
      try {
        this.headers.push({
          label: this.$t("status"),
          value: "status",
          field: "status",
        });
        this.headers.push({
          label: this.$t("date"),
          value: "date",
          field: "date",
        });
        let response = await this.$axios.get("/question_titles");
        let length = response.data.length;
        for (let i = 0; i < length; i++) {
          let item = response.data[length - i - 1];
          this.question_titles.push(item);
          this.headers.splice(0, 0, {
            label: item.name,
            field: (row) =>
              row["v" + item.id] ? row["v" + item.id]["text"] : "",
            style: "white-space: normal !important;",
          });
        }

        response = await this.$axios.get("/questions");
        response.data.map((x) => {
          this.questions.push(x);
        });
      } catch (e) {
        this.$q.notify({
          message: e,
        });
      }
      let patient_id = this.patient.id;
      this.$axios
        .get("/initial_questions/" + patient_id)
        .then((respone) => {
          respone.data.map((item) => {
            let row = this.toRow(item);
            this.items.push(this.toTemplate(row));
          });
        })
        .catch((e) => {
          this.$q.notify({
            message: e,
          });
        });
    },
    toTemplate(obj) {
      let resObj = Object.assign({}, obj);
      resObj.status = this.$helper.ToYesNO(obj.status);

      if (typeof obj.id != "undefined") resObj.id = obj.id;

      return resObj;
    },
    toObject(template) {
      let resObj = Object.assign({}, template);
      resObj.status = this.$helper.ToBoolFromYesNo(template.status);

      if (typeof template.id != "undefined") resObj.id = template.id;
      return resObj;
    },
    toItem(row) {
      let res = {
        id: row.id,
        status: row.status,
        date: row.date,
        checkbox: [],
        radio: {},
      };

      this.question_titles.map((item) => {
        let attribut = row["v" + item.id];
        if (typeof attribut != "undefined") {
          if (item.isMany) {
            if (typeof attribut.id == "number") res.checkbox.push(attribut.id);
            else
              attribut.id.split(",").map((id) => {
                res.checkbox.push(parseInt(id));
              });
          } else {
            res.radio["r" + item.id] = attribut.id;
          }
        }
      });
      return res;
    },
    editItem() {
      let item = this.selectedItems[0];
      this.editedIndex = this.items.indexOf(item);
      let row = this.toObject(item);
      this.editedItem = this.toItem(row);

      this.dialog = true;
    },
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
    async deleteItem() {
      this.$q
        .dialog({
          title: this.$t("confirm"),
          message: this.$t("would_like_delete"),
          cancel: true,
          persistent: true,
        })
        .onOk(async () => {
          let deletedItem = this.selectedItems[0];
          const index = this.items.indexOf(deletedItem);
          deletedItem = this.toItem(deletedItem);
          let initial_question = {
            id: deletedItem.id,
            patient: this.patient.id,
            questions: "",
            status: deletedItem.status,
            date: deletedItem.date,
          };
          // Convert the ids into text
          deletedItem.checkbox.map((item) => {
            initial_question.questions += item + ",";
          });
          Object.values(deletedItem.radio).map((item) => {
            initial_question.questions += item + ",";
          });

          // Clean the last mark (,)
          initial_question.questions = initial_question.questions.slice(0, -1);

          let response = await this.$helper.deleteInstance(
            initial_question,
            "/initial_question_request"
          );
          if (response == true) {
            this.items.splice(index, 1);
            this.selectedItems = []
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
        .onOk(() => {
          // console.log('>>>> second OK catcher')
        })
        .onCancel(() => {
          // console.log('>>>> Cancel')
        })
        .onDismiss(() => {
          // console.log('I am triggered on both OK and Cancel')
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
      let initial_question = {
        patient: this.patient.id,
        questions: "",
        status: this.editedItem.status,
        date: this.editedItem.date,
        id: this.editedItem.id,
      };

      // Convert the ids into text
      this.editedItem.checkbox.map((item) => {
        initial_question.questions += item + ",";
      });
      Object.values(this.editedItem.radio).map((item) => {
        initial_question.questions += item + ",";
      });

      // Clean the last mark (,)
      initial_question.questions = initial_question.questions.slice(0, -1);
      let response = await this.$helper.saveInstance(
        initial_question,
        "/initial_question_request"
      );
      if (response == true) {
        let row = this.toRow(initial_question);
        if (this.editedIndex > -1) {
          Object.assign(this.items[this.editedIndex], this.toTemplate(row));
        } else {
          this.items.push(this.toTemplate(row));
        }
        this.close();
      }

      if (response == true) {
        this.$q.notify({
          message: this.$t("saved"),
          color: "blue",
          icon: "success",
          actions: [{ label: this.$t("close"), color: "white" }],
        });
      } else {
        this.$q.notify({
          message: this.$t("unsaved"),
          color: "red",
          icon: "error",
          actions: [{ label: this.$t("close"), color: "white" }],
        });
      }
    },
    btnNewItem() {
      this.defaultItem = {
        checkbox: [],
        radio: {},

        date: this.$helper.GetCurrentDate(),
        status: false,
        patient: this.patient.id,
      };
      this.editedItem = Object.assign({}, this.defaultItem);
      this.dialog = true;
    },
  },
  components: {
    InitialQuestions,
  },
  mounted: function () {},
};
</script>