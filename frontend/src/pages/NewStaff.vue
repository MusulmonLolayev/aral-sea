<template>
  <div>
    <q-form ref="userForm">
      <h6 style="margin:15px">{{ $t("personal_inf").format_letter() }}</h6>
      <q-separator inset />
      <div class="row" style="margin: 10px">
        <div class="col-4" style="margin: 5px">
          <q-input
            v-model="staff.last_name"
            dense
            :label="$t('last_name').format_letter()"
            outlined
            :rules="[value => (value && value.length > 3) || $t('min_char_3')]"
          />
        </div>
        <div class="col-4" style="margin: 5px">
          <q-input
            v-model="staff.first_name"
            dense
            :label="$t('first_name').format_letter()"
            outlined
            :rules="[value => (value && value.length > 3) || $t('min_char_3')]"
          />
        </div>
        <div class="col-4" style="margin: 5px">
          <q-input
            v-model="staff.middle_name"
            dense
            :label="$t('middle_name').format_letter()"
            outlined
          />
        </div>

        <div class="col-4" style="margin: 5px;">
          <q-select
            :label="$t('position').format_letter()"
            :options="positions"
            option-value="id"
            option-label="title"
            emit-value
            map-options
            v-model="staff.position"
            dense
          />
        </div>

        <div class="col-4" style="margin: 5px;">
          <q-select
            :label="$t('district').format_letter()"
            :options="districts"
            option-value="id"
            option-label="name"
            emit-value
            map-options
            v-model="staff.districts"
            dense
            multiple
          >
            <template
              v-slot:option="{
                itemProps,
                itemEvents,
                opt,
                selected,
                toggleOption
              }"
            >
              <q-item v-bind="itemProps" v-on="itemEvents">
                <q-item-section>
                  <q-item-label v-html="opt.name"></q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-toggle :value="selected" @input="toggleOption(opt)" />
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </div>

        <div class="col-8" style="margin: 5px;">
          <q-input
            v-model="staff.order"
            dense
            :label="$t('order_text').format_letter()"
            outlined
          />
        </div>
      </div>
      <h6 style="margin:15px">{{ $t("user_inf").format_letter() }}</h6>
      <q-separator inset />
      <div class="row" style="margin: 10px">
        <div class="col-4" style="margin: 5px">
          <q-input
            v-model="user.username"
            dense
            :label="$t('user_or_email').format_letter()"
            outlined
          />
        </div>
        <div class="col-4" style="margin: 5px">
          <q-input
            v-model="user.password"
            type="password"
            dense
            :label="$t('password').format_letter()"
            outlined
            :rules="rules.password"
          />
        </div>
        <div class="col-4" style="margin: 5px">
          <q-input
            v-model="password"
            type="password"
            dense
            :label="$t('conf_password').format_letter()"
            outlined
            :rules="rules.conf_password"
          />
        </div>
      </div>
    </q-form>
    <!--<h6 style="margin:15px">{{ $t("permissions").format_letter() }}</h6>
    <q-separator inset />
    <div class="row" style="margin: 10px">
      <div class="col-3">
        <div class="col-3" style="margin: 5px; margin-left: 20px">
          <q-select
            :label="$t('groups').format_letter()"
            :options="groups"
            option-value="id"
            option-label="name"
            emit-value
            map-options
            v-model="selectedGroup"
            dense
            multiple
          >
            <template
              v-slot:option="{
                itemProps,
                itemEvents,
                opt,
                selected,
                toggleOption
              }"
            >
              <q-item v-bind="itemProps" v-on="itemEvents">
                <q-item-section>
                  <q-item-label v-html="opt.name"></q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-toggle :value="selected" @input="toggleOption(opt)" />
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </div>
      </div>
    </div> -->
    <div class="row" style="float:right; margin: 10px">
      <q-btn
        style="margin-right: 10px"
        :label="$t('cancel')"
        @click="$router.go(-1)"
      ></q-btn>
      -<q-btn
        style="margin-right: 10px"
        :label="$t('save_and_back')"
        @click="onSaveAndBack"
      ></q-btn>
      <q-btn
        style="margin-right: 10px"
        :label="$t('save')"
        @click="onSave"
      ></q-btn>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      staff: {
        id: null,
        last_name: null,
        first_name: null,
        middle_name: null,
        position: null,
        districts: []
      },
      user: {
        id: null,
        username: null,
        password: null
      },
      password: null,
      rules: {
        password: [
          value =>
            (value && value.length > 6) || this.$t("min_char_6").format_letter()
        ],
        conf_password: [
          value =>
            value == this.user.password ||
            this.$t("passwordsnotmatched").format_letter()
        ]
      },
      // 0 => user, 1 => staff, 2 => permissions
      positions: [],
      districts: []
    };
  },

  computed: {},

  methods: {
    async initialize() {
      await this.$axios.get("/positions").then(response => {
        this.positions = response.data;
      });
      await this.$axios.get("/districts_by_region/2").then(response => {
        this.districts = response.data;
      });
      if (this.$route.params.id != 0) {
        this.$axios.get("/staffs/" + this.$route.params.id).then(response => {
          this.user = response.data["user"];
          this.staff = response.data["staff"];
        });
      }
    },
    onSaveAndBack() {
      this.$refs.userForm.validate().then(success => {
        if (success) {
          if (this.staff.id == null || this.user.id == null) {
            this.$axios
              .post("/users", {
                user: this.user,
                staff: this.staff
              })
              .then(response => {
                this.user.id = response.data.user;
                this.staff.id = response.data.staff;

                this.$router.go(-1);
              })
              .catch(error => {
                this.onError(error)
              });
          } else {
            this.$axios
              .put("/users", {
                user: this.user,
                staff: this.staff
              })
              .then(response => {
                this.user.id = response.data.user;
                this.staff.id = response.data.staff;
                this.$router.go(-1);
              })
              .catch(error => {
                console.log(error.response.status);
                this.onError(error)
              });
          }
        } else {
          this.$q.notify({
            message: this.$t("fill_all_fields").format_letter(),
            color: "red",
            icon: "error",
            actions: [
              { label: this.$t("close").format_letter(), color: "white" }
            ]
          });
        }
      });
    },
    onSave() {
      this.$refs.userForm.validate().then(success => {
        if (success) {
          if (this.staff.id == null || this.user.id == null) {
            this.$axios
              .post("/users", {
                user: this.user,
                staff: this.staff
              })
              .then(response => {
                this.user.id = response.data.user;
                this.staff.id = response.data.staff;
              })
              .catch(error => {
                this.onError(error)
              });
          } else {
            this.$axios
              .put("/users", {
                user: this.user,
                staff: this.staff
              })
              .then(response => {
                this.user.id = response.data.user;
                this.staff.id = response.data.staff;
              })
              .catch(error => {
                this.onError(error)
              });
          }
        } else {
          this.$q.notify({
            message: this.$t("fill_all_fields").format_letter(),
            color: "red",
            icon: "error",
            actions: [
              { label: this.$t("close").format_letter(), color: "white" }
            ]
          });
        }
      });
    },
    onError(error) {
      if (error.response.status == 406) {
        this.$q.dialog({
          title: this.$t("user_not_created").format_letter(),
          message: this.$t("error_reason").format_letter() + ":\n" + this.$t("user_exists").format_letter().format(this.user.username),
        });
      }
    }
  },
  mounted() {
    this.initialize();
  }
};
</script>
