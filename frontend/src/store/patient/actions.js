export function setCurrentPatient (context, {patient}) {
    context.commit('setCurrentPatient', {patient: patient})
}

export function setCurrentPrimary (context, {primary_diagnose}) {
    context.commit('setCurrentPrimary', {primary_diagnose: primary_diagnose})
}

export function setCurrentTaking (context, {taking_medicine}) {
    context.commit('setCurrentTaking', {taking_medicine: taking_medicine})
}

export function setCurrentComplaint (context, {complaint}) {
    context.commit('setCurrentComplaint', {complaint: complaint})
}

export function setCurrentBlood (context, {blood_analysis}) {
    context.commit('setCurrentBlood', {blood_analysis: blood_analysis})
}
