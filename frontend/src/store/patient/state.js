function GetCurrentDate() {
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, "0");
  var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
  var yyyy = today.getFullYear();

  today = yyyy + "-" + mm + "-" + dd;
  return today;
}
export default function() {
  return {
    primary_diagnose: {
      date: GetCurrentDate(),
      status: false,
      clinicalform: null,
      right_lung_top: null,
      right_lung_bottom: null,
      left_lung_top: null,
      left_lung_bottom: null,
      infiltration: null,
      decay: null,
      seeding: null,
      resorption: null,
      bk: null
    },
    taking_medicine: {
      date: GetCurrentDate(),
      fromdate: GetCurrentDate(),
      streptomycin: null,
      rifampicin: null,
      isoniazid: null,
      pyrazinamide: null,
      ethambutol: null,

      status: false
    },
    complaint: {
      diarrhea: null,
      normal_stool: null,
      constipation: null,
      flatulence: null,
      stomachache: null,
      stool_frequency: null,
      character: null,
      tuberculosis_tolerance: null,
      related_disease: null,
      nausea: null,
      vomiting: null,
      headache: null,
      sweating: null,
      weakness: null,
      allergodermatosis: null,
      weight_loss: null,

      status: false,
      date: GetCurrentDate()
    },
    blood_analysis: {
      status: false,
      date: GetCurrentDate(),
      er: null,
      leyk: null,
      hb: null,
      color: null,
      pya: null,
      sya: null,
      eoz: null,
      lf: null,
      mon: null,
      hb: null,
      coe: null,
      act: null,
      alt: null
    }
  };
}
