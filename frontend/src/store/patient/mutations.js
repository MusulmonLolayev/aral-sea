export function setCurrentPatient (state, {patient}) {
    state.patient = patient
}

export function setCurrentPrimary (state, {primary_diagnose}) {
    state.primary_diagnose = primary_diagnose
}

export function setCurrentTaking (state, {taking_medicine}) {
    state.taking_medicine = taking_medicine
}

export function setCurrentComplaint (state, {complaint}) {
    state.complaint = complaint
}

export function setCurrentBlood (state, {blood_analysis}) {
    state.blood_analysis = blood_analysis
}