<template>
  <q-form ref="form">
    <div>
      <div class="row">
        <!--<div class="input_div" v-for="(item, index) in labels" :key="index">
          <q-input
            :label="$t(item)"
            v-model="bloodanalysis[item]"
            type="number"
            :rules="[() => required(item)]"
            :ref="item"
            style="margin-right: 5px"
          >
            <template v-slot:after>
              <q-btn dense flat icon="scatter_plot" @click="onScatterCharShow(item)"/>
            </template>
          </q-input>
        </div> -->


        <div class="input_div">
          <q-input
            v-model="bloodanalysis.er"
            type="number"
            :rules="[() => required('er')]"
            ref="er"
            :label="$t('er')"
            style="margin-right: 5px"
            :suffix="'*10^12' + $t('_liter')"
            step="0.1"
            min='0'
            max="10"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.leyk"
            type="number"
            :rules="[() => required('leyk')]"
            ref="leyk"
            :label="$t('leyk')"
            style="margin-right: 5px"
            :suffix="'*10^6' + $t('_liter')"
            min='0'
            max="100000"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.hb"
            type="number"
            :rules="[() => required('hb')]"
            ref="hb"
            :label="$t('hb')"
            style="margin-right: 5px"
            :suffix="$t('gram_liter')"
            min='0'
            max="1000"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.color"
            type="number"
            :rules="[() => required('color')]"
            ref="color"
            :label="$t('color')"
            style="margin-right: 5px"
            step="0.1"
            min='0'
            max="2"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.pya"
            type="number"
            :rules="[() => required('pya')]"
            ref="pya"
            :label="$t('pya')"
            style="margin-right: 5px"
            suffix="%"
            min='0'
            max="100"
          />
        </div>
        <div class="input_div">
          <q-input
            v-model="bloodanalysis.sya"
            type="number"
            :rules="[() => required('sya')]"
            ref="sya"
            :label="$t('sya')"
            style="margin-right: 5px"
            suffix="%"
            min='0'
            max="100"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.eoz"
            type="number"
            :rules="[() => required('eoz')]"
            ref="eoz"
            :label="$t('eoz')"
            style="margin-right: 5px"
            suffix="%"
            min='0'
            max="100"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.lf"
            type="number"
            :rules="[() => required('lf')]"
            ref="lf"
            :label="$t('lf')"
            style="margin-right: 5px"
            suffix="%"
            min='0'
            max="100"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.mon"
            type="number"
            :rules="[() => required('mon')]"
            ref="mon"
            :label="$t('mon')"
            style="margin-right: 5px"
            suffix="%"
            min='0'
            max="100"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.act"
            type="number"
            :rules="[() => required('act')]"
            ref="act"
            :label="$t('act')"
            style="margin-right: 5px"
            :suffix="$t('_liter')"
            min='0'
            max="10"
          />
        </div>

        <div class="input_div">
          <q-input
            v-model="bloodanalysis.alt"
            type="number"
            :rules="[() => required('alt')]"
            ref="alt"
            :label="$t('alt')"
            style="margin-right: 5px"
            :suffix="$t('_liter')"
            min='0'
            max="10"
          />
        </div>

        <div class="input_div">
          <q-checkbox
            style="margin-top: 15px"
            v-model="bloodanalysis.status"
            :label="$t('status')"
          />
        </div>
        <div class="input_div">
          <q-input
            :label="$t('date')"
            v-model="bloodanalysis.date"
            type="date"
          />
        </div>
      </div>
      <div v-show="isError">
        <span class="red--text"
          >{{ $t("_logical_errors") }}: {{ logicalErrors.length }}</span
        >
        <q-markup-table height="100" dense>
          <tbody>
            <tr v-for="(item, index) in logicalErrors" :key="index">
              <td>{{ item.error }}</td>
            </tr>
          </tbody>
        </q-markup-table>
      </div>
    </div>
  </q-form>
</template>

<script>
export default {
  name: "BloodAnalysis",
  props: ["bloodanalysis", "check_acceptability"],
  data: function() {
    return {
      logicalErrors: [],
      labels: [
        "er",
        "leyk",
        "hb",
        "color",
        "pya",
        "sya",
        "eoz",
        "lf",
        "mon",
        "act",
        "alt"
      ]
    };
  },
  computed: {
    isError: function() {
      return this.logicalErrors.length;
    }
  },
  methods: {
    initialize() {},
    required(name) {
      let value = this.bloodanalysis[name];
      if (value === 0 || value === null || value === "") return true;
      //if (!value) return this.$t("required");

      this.logicalErrors = this.logicalErrors.filter(
        item => item["feature_name1"] != name && item["feature_name2"] != name
      );

      if (typeof this.check_acceptability != "undefined") {
        let res = this.check_acceptability(name, this.bloodanalysis);
        if (typeof res == "boolean") return res;
        Object.keys(res).forEach(item => {
          let t = -1;
          for (let i = 0; i < this.logicalErrors.length; i++) {
            let e = this.logicalErrors[i];
            if (
              (e["feature_name1"] == name &&
                e["feature_name2"] == res[item]["feature_name2"]) ||
              (e["feature_name2"] == name &&
                e["feature_name1"] == res[item]["feature_name2"])
            ) {
              t = i;
              break;
            }
          }
          if (t > -1) {
            this.logicalErrors[t].error = res[item].error;
          } else {
            this.logicalErrors.push(res[item]);
          }
        });
        return res.length + " " + this.$t("logical_errors") + ".";
      }
      return true;
    },
    hasError() {
      let error = false;
      this.labels.forEach(item => {
        let res = this.required(item);
        if (typeof res == "string") {
          error = true;
          if (this.$refs[item].hasError) this.$refs[item].validate(true);
        }
      });
      return error;
    },
    hasError() {
      return this.$refs["form"].validate();
    },
    onScatterCharShow(feature){
    }
  },
  beforeMount() {
    this.initialize();
  }
};
</script>

<style lang="scss" scoped>
div.input_div {
  margin-left: 5px;
  margin-right: 5px;
  width: 200px;
}
</style>
