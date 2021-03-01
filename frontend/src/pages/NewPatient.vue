<template>
  <div class="q-pa-md">
    <q-stepper
      v-model="step"
      ref="stepper"
      color="primary"
      animated
      :vertical="$q.screen.lt.md"
      keep-alive
      header-nav
    >
      <q-step
        :name="1"
        :title="$t('init_inf')"
        icon="settings"
        :done="step > 1"
      >
        <patient-component :patient='patient' ref='refPatient'/>
      </q-step>

      <q-step
        :name="2"
        :title="$t('init_questions')"
        icon="live_help"
        :done="step > 2"
      >
        <initial-questions :selected="initial_question_selected"/>
      </q-step>

      <q-step
        :name="3"
        :title="$t('primary_diagnose')"
        icon="fas fa-diagnoses"
        :done="step > 3"
      >
        <primary-diagnose :primarydiagnose="primary_diagnose" ref="refPrimary"/>

      </q-step>

      <q-step
        :name="4"
        :title="$t('taking_medicine')"
        icon="fas fa-capsules"
        :done="step > 4"
      >
      <taking-medicine :takingmedicine='taking_medicine' ref='refTaking'/>
      </q-step>

      <q-step
        :name="5"
        :title="$t('complaint')"
        icon="fas fa-comment-medical"
        :done="step > 5"
      >
        <complaint :complaint="complaint" ref='refComplaint'/>
      </q-step>

      <q-step
        :name="6"
        :title="$t('blood_analysis')"
        icon="fas fa-burn"
        :done="step > 6"
      >
        <blood-analysis :bloodanalysis="blood_analysis" ref="refBlood" :check_acceptability="check_acceptability"/>
      </q-step>

      <q-step
        :name="7"
        :title="$t('other_analysis')"
        icon="fas fa-biohazard"
      >
        <other-component :other="others" ref="refOther"/>
      </q-step>

      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn @click="nextStep()" color="primary" :label="step === 7 ? $t('finish') : $t('continue')" />
          <q-btn v-if="step > 1" flat color="primary" @click="$refs.stepper.previous()" :label="$t('back')" class="q-ml-sm" />
          <q-btn v-show="step == 7" flat color="primary" @click="save()" :label="$t('save')" class="q-ml-sm" />
          <q-btn flat color="primary" v-show="false" @click="act()" label="Act" class="q-ml-sm" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </div>
</template>

<script>
import PatientComponent from '../components/editors/patient'
import InitialQuestions from '../components/editors/init-questions'
import PrimaryDiagnose from '../components/editors/primary-diagnose'
import TakingMedicine from '../components/editors/taking-medicine'
import Complaint from '../components/editors/complaint'
import BloodAnalysis from '../components/editors/blood-analysis'
import OtherComponent from '../components/editors/others'


export default {
  data () {
    return {
      step: 1,
      patient: {
        birthday: this.$helper.GetCurrentDate(),
        fromdate: this.$helper.GetCurrentDate(),
        gender: true
      },
      initial_question_selected: {
        checkbox: [],
        radio: {},
        date: this.$helper.GetCurrentDate(),
        status: false,
      },
      init_questions: {},
      primary_diagnose: {
        date: this.$helper.GetCurrentDate(),
        infiltration: false,
        decay: false,
        seeding: false,
        resorption: false,
        compaction: false,
        scarring: false,
        calcification: false,
        status: false,
        bk: false,
      },
      taking_medicine: {
        date: this.$helper.GetCurrentDate(),
        fromdate: this.$helper.GetCurrentDate(),
        streptomycin: false,
        rifampicin: false,
        isoniazid: false,
        pyrazinamide: false,
        ethambutol: false,
        status: false,
      },
      complaint: {
        diarrhea: false,
        normal_stool: false,
        constipation: false,
        flatulence: false,
        stomachache: false,
        from_stool_frequency: 0,
        to_stool_frequency: 0,
        status: false,
        date: this.$helper.GetCurrentDate(),
      },
      blood_analysis: {
        status: false,
        date: this.$helper.GetCurrentDate(),
        er: 0,
        leyk: 0,
        hb: 0,
        color: 0,
        pya: 0,
        sya: 0,
        eoz: 0,
        lf: 0,
        mon: 0,
        hb: 0,
        coe: 0,
        act: 0,
        alt: 0,
      },
      others: {
        status: false,
        date: this.$helper.GetCurrentDate(),
        from_weight_loss: 0,
        to_weight_loss: 0,
        tuberculosis_tolerance: false,
        related_disease: false,
        nausea: false,
        vomiting: false,
        headache: false,
        sweating: false,
        weakness: false,
        allergodermatosis: false,
        coproscopy: false,
      },
      ranges: [],
    }
  },
  methods: {
    initialize(){
      this.$axios.get('/getaccetableintervals')
      .then(response => {
        this.ranges = response.data
      })
    },
    async nextStep(){
      let hasError = await this.$refs.refPatient.hasError()
      .then(success => {
        return success
      })

      if (!hasError){
          this.showErrorNotify()
          return
      }
      if (typeof this.$refs.refPrimary != 'undefined'){
        hasError = await this.$refs.refPrimary.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          return
      }
      }

      if (typeof this.$refs.refTaking != 'undefined'){
        hasError = await this.$refs.refTaking.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          return
      }
      }

      if (typeof this.$refs.refComplaint != 'undefined'){
        hasError = await this.$refs.refComplaint.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          return
      }
      }

      if (typeof this.$refs.refBlood != 'undefined'){
        hasError = await this.$refs.refBlood.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          return
      }
      }

      if (typeof this.$refs.refOther != 'undefined'){
        hasError = await this.$refs.refOther.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          return
      }
      }

      this.$refs.stepper.next()
    },
    showErrorNotify(){
      this.$q.notify({
            message: this.$t('please_correct_errors'),
            color: 'red',
            icon: 'error',
            actions: [
              { label: this.$t('close'), color: 'white'}
            ]
          });
    },
    async save(){
      let hasError = await this.$refs.refPatient.hasError()
      .then(success => {
        return success
      })
      if (!hasError){
          this.step = 1
          this.showErrorNotify()
          return
      }

      if (typeof this.$refs.refPrimary != 'undefined'){
        hasError = await this.$refs.refPrimary.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          this.step = 3
          return
        }
      }

      if (typeof this.$refs.refTaking != 'undefined'){
        hasError = await this.$refs.refTaking.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          this.step = 4
          return
        }
      }

      if (typeof this.$refs.refComplaint != 'undefined'){
        hasError = await this.$refs.refComplaint.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          this.step = 5
          return
        }
      }

      if (typeof this.$refs.refBlood != 'undefined'){
        hasError = await this.$refs.refBlood.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          this.step = 6
          return
        }
      }

      if (typeof this.$refs.refOther != 'undefined'){
        hasError = await this.$refs.refOther.hasError()
        .then(success => {
          return success
        })

        if (!hasError){
          this.showErrorNotify()
          this.step = 7
          return
        }
      }

      // save the patient
      let response = await this.$helper.saveInstance(this.patient, '/patient_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      this.Ready_init_questions()
      // Save the initial questions
      response = await this.$helper.saveInstance(this.init_questions, '/initial_question_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      // Save the primary
      this.primary_diagnose.patient = this.patient.id
      response = await this.$helper.saveInstance(this.primary_diagnose, '/primary_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      // Save the taking
      this.taking_medicine.patient = this.patient.id
      response = await this.$helper.saveInstance(this.taking_medicine, '/taking_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      // Save the complaint
      this.complaint.patient = this.patient.id
      response = await this.$helper.saveInstance(this.complaint, '/complaint_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      // Save the complaint
      this.blood_analysis.patient = this.patient.id
      response = await this.$helper.saveInstance(this.blood_analysis, '/blood_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      // Save the complaint
      this.others.patient = this.patient.id
      response = await this.$helper.saveInstance(this.others, '/other_request')
      if (response != true){
        this.DealSavingRespone(response)
        return
      }

      this.$q.notify({
        message: this.$t('saved'),
        color: 'blue',
        icon: 'success',
        actions: [
          { label: this.$t('close'), color: 'white'}
        ]
        });
    },
    Ready_init_questions(){
      // Chech the primary diagnose id to be undefined to know ethier create instane or edit
      this.init_questions.patient = this.patient.id;
        // Convert the ids into text
      this.init_questions.questions = ""
      this.initial_question_selected.checkbox.map(item => {
        this.init_questions.questions += item + ","
      })
      Object.values(this.initial_question_selected.radio).map(item => {
        this.init_questions.questions += item + ","
      })
        // Clean the last mark (,)
      this.init_questions.questions = this.init_questions.questions.slice(0, -1)
        // For test Patient 70 id
        //this.initial_question.patient = 70
        //return 0;
    },
    DealSavingRespone(response){
      this.$q.notify({
          message: this.$t('unsaved'),
          color: 'red',
          icon: 'error',
          actions: [
          { label: this.$t('close'), color: 'white'}
        ]
      });
    },
    act(){
      console.log(this.$refs)
    },
    check_acceptability: function(name, instance){
      return this.$helper.check_acceptability(name, instance, this.ranges)
    },
  },
  mounted(){
    this.initialize()
  },
  components: {
    PatientComponent,
    InitialQuestions,
    PrimaryDiagnose,
    TakingMedicine,
    Complaint,
    BloodAnalysis,
    OtherComponent,
  }
}
</script>