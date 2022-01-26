<template>
  <div style="margin: 15px">
    <q-table
      :title="$t('farms').format_letter()"
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
            <q-btn
              icon="add"
              dense
              v-if="IsPermission('add_farm')"
              @click="onCreateItem"
            >
              <q-tooltip>{{ $t("new_item").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="edit"
              :disable="!IsSelectedItem"
              dense
              v-if="IsPermission('change_farm')"
              @click="onEdit"
            >
              <q-tooltip>{{ $t("go_detail").format_letter() }}</q-tooltip>
            </q-btn>

            <q-btn
              icon="delete"
              :disable="!IsSelectedItem"
              @click="deleteItem"
              v-if="IsPermission('delete_farm')"
            >
              <q-tooltip>{{ $t("delete").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn icon="update" @click="onUpdate">
              <q-tooltip>{{ $t("update_data").format_letter() }}</q-tooltip>
            </q-btn>
            <div style="width: 200px">
              <q-select
                :label="$t('select_district').format_letter()"
                :options="districts"
                option-value="id"
                option-label="name"
                emit-value
                map-options
                v-model="selected_district"
                style="margin-right: 30px"
                @input="onDistrictChanged"
              />
            </div>
          </q-btn-group>
        </div>
      </template>
    </q-table>
    <q-dialog v-model="dialog">
      <q-card style="width: 400px">
        <q-card-section>
          <span class="headline">{{
            this.$t("new_item").format_letter()
          }}</span>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-pt-none">
          <farm :farm="farm" ref="refFarm" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            color="blue darken-1"
            dense
            @click="onCancel"
            :label="$t('cancel').format_letter()"
          />
          <q-btn
            color="blue darken-1"
            dense
            @click="OnSave"
            :label="$t('save').format_letter()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import Farm from "../components/editors/farm.vue";

export default {
  name: "FarmList",
  data: function() {
    return {
      dialog: false,
      headers: [],
      items: [],
      selectedItems: [],
      filter: "",
      districts: [],
      farm: this.$helper.farm(),
      selected_district: {}
    };
  },
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
        { label: this.$t("farm_name").format_letter(), field: row => row.name }
      ];

      await this.$axios.get("district_request").then(response => {
        this.districts = response.data;
        this.selected_district = this.districts[0].id;
        this.Update();
      });
    },

    async deleteItem() {
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
          let response = await this.$helper.deleteInstance(item, "farm_request1");
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
    onUpdate() {
      this.Update();
    },

    Update() {
      this.items = [];
      this.$axios
        .get("district_farms/" + this.selected_district)
        .then(respone => {
          this.items = respone.data;
        });
    },

    onDistrictChanged() {
      this.Update();
    },

    OnSave() {
      this.$refs["refFarm"].hasError().then(result => {
        if (result) {
          if (this.farm.id == 0) {
            this.$axios.post("farm_request1", this.farm).then(response => {
              this.$q.notify({
                message: this.$t("created").format_letter(),
                color: "blue",
                icon: "success",
                actions: [
                  { label: this.$t("close").format_letter(), color: "white" }
                ]
              });
              this.farm.id = response.data;
              this.items.push(this.farm);
              this.dialog = false;
            });
          }
          else{
            let farm = this.farm
            this.$axios.put("farm_request1", farm)
            .then(response => {
              this.$q.notify({
                message: this.$t("updated").format_letter(),
                color: "blue",
                icon: "success",
                actions: [
                  { label: this.$t("close").format_letter(), color: "white" }
                ]
              });
              let index = this.items.indexOf(this.selectedItems[0])
              Object.assign(this.items[index], this.farm)
              this.dialog = false;
            });
          }
        }
      });
    },

    onCreateItem() {
      this.farm = this.$helper.farm();
      this.dialog = true;
    },

    onEdit() {
      let item = this.selectedItems[0];
      this.farm = Object.assign({}, item);
      this.dialog = true;
    },
    onCancel() {
      this.dialog = false;
    }
  },
  components: {
    Farm
  },
  mounted: function() {}
};
</script>

<style></style>
