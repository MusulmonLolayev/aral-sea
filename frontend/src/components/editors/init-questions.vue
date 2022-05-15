<template>
  <div>
    <ol>
      <li v-for="(item, index) in question_titles" :key="'Q' + index">
        <h6 v-if="!$q.screen.lt.md">{{item.title}}</h6>
        <h6 style="font-size:12px" v-else>{{item.title}}</h6>
        <ul v-if="item.isMany">
          <li style="list-style-type: none;">
            <div class="row" style="margin:0px">
              <div class="col-md-5"
                v-for="(option_item, option_index) in get_questions(item.id)"
                :key="index + '_' + option_index"
                md="3"
                cols="10"
                style="margin:0px"
              >
                <q-checkbox
                  :label="option_item.text"
                  v-model="selected.checkbox"
                  :val="option_item.id"
                />
              </div>
            </div>
          </li>
        </ul>
        <ul v-else>
            <li style="list-style-type: none;">
              <div class="row" style="margin:0px">
                <div class="col-md-5"
                  v-for="(option_item, option_index) in get_questions(item.id)"
                  :key="index + '_' + option_index"
                  md="3"
                  cols="10"
                  style="margin:0px"
                >
                  <q-radio v-model="selected.radio['r' + item.id]" :label="option_item.text" :val="option_item.id" />
                </div>
              </div>
            </li>
        </ul>
      </li>
    </ol>
    <div class="row">
      <div class="col" cols="10" md="3">
        <q-checkbox v-model="selected.status" label="Status" />
      </div>
      <div class="col" cols="10" md="3">
        <q-input
        :label="$t('date')"
        v-model="selected.date"
        type='date'
      />
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "InitialQuestions",
  props: ["selected"],
  data: function() {
    return {
      question_titles: [],
      questions: [],
    };
  },
  created() {
    this.initialize();
  },
  methods: {
    async initialize() {
      if (typeof this.selected.id == "undefined") {
        this.selected.date = this.$helper.GetCurrentDate();
      }
      try {
        let response = await this.$axios.get("/question_titles");
        for (let i = 0; i < response.data.length; i++) {
          let item = response.data[i];
          this.question_titles.push(item);
        }

        response = await this.$axios.get("/questions");
        response.data.map(x => {
          this.questions.push(x);
        });
      } catch (e) {
        //this.$store.state.message.showMessage("Error", e, "error");
      }
    },
    get_questions(title_id) {
      let res = [];
      this.questions.map(item => {
        if (item.question_title == title_id) res.push(item);
      });
      return res;
    },
  },
};
</script>

<style scoped>
</style>