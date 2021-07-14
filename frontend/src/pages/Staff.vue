<template>
  <div class="q-pa-md">
    <q-table
      :title="$t('staffs').format_letter()"
      :data="items"
      :columns="$store.state.common.StaffList_Colunms"
      row-key="id"
      :filter="filter"
      :no-data-label="$t('nothingtoshow').format_letter()"
      :rows-per-page-label="$t('rows_per_page_label') + ':'"
      :selected-rows-label="$helper.getSelectedString"
      :pagination-label="$helper.get_pagination_label"
      :selected.sync="selectedItems"
      selection="single"
    >
      <template v-slot:top-right="props">
        <div class="row">
          <q-btn-group style="margin-right: 30px; margin-top: 5px" flat>
            <q-btn icon="add" to='/staffs/0'>
              <q-tooltip>{{ $t("new_item").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="edit"
              @click="editItem"
              :disable="selectedItems.length != 1"
            >
              <q-tooltip>{{ $t("edit").format_letter() }}</q-tooltip>
            </q-btn>
            <q-btn
              icon="delete"
              @click="deleteItem"
              :disable="selectedItems.length != 1"
            >
              <q-tooltip>{{ $t("delete").format_letter() }}</q-tooltip>
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
  name: "StaffList",
  data() {
    return {
      filter: "",
      items: [],
      permissions: {
        view: false,
        add: false,
        change: false,
        delete: false
      },
      user_role: this.$store.state.auth.user_role,
      positions: [],
      selectedItems: []
    };
  },

  computed: {
    IsSelectedItem() {
      return this.selectedItems.length;
    }
  },

  methods: {
    async initialize() {
      await await this.$axios.get("/positions").then(response => {
        this.positions = response.data;
      });
      this.updateDate();
    },

    async updateDate() {
      await this.$axios.get("/staffs/0").then(response => {
        this.items = response.data;
        for (let i = 0; i < this.items.length; i++) {
          for (let j = 0; j < this.positions.length; j++) {
            if (this.items[i].position == this.positions[j].id) {
              this.items[i].position_name = this.positions[j].title;
              break;
            }
          }
        }
      });
    },
    editItem(){
      this.$router.push('staffs/' + this.selectedItems[0].id)
    },
    deleteItem(){
      
    },
  },
  beforeMount() {
    this.initialize();
  },
  components: {}
};
</script>

<style scop></style>
