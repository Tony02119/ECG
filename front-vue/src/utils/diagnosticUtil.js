// Information on each class
const diseasesInfo = {
    "Disclaimer": "The information provided here is for educational purposes only and should not be considered as medical advice. Please consult a healthcare professional for accurate diagnosis and treatment.",
    "Sinus Rhythm": "Normal sinus rhythm is a regular heart rhythm initiated by the sinus node, considered a healthy rhythm.",
    "Supraventricular": "Supraventricular arrhythmias are irregular heartbeats originating from the atria or the atrioventricular node.",
    "Potentially Dangerous": " A potentially dangerous condition can indicate an irregular heartbeat that may lead to severe complications.",
    "Threatening VT": "Threatening ventricular tachycardia involves a rapid heart rhythm originating from the ventricles, which can be life-threatening.",
    "Special Form TdP": "Torsades de Pointes is a specific form of polymorphic ventricular tachycardia that can lead to ventricular fibrillation.",
    "Dangerous VFL/VF": "Ventricular flutter (VFL) or ventricular fibrillation (VF) are highly dangerous conditions where the heart quivers instead of pumping blood effectively.",
    "AFIB": " Atrial fibrillation is an arrhythmia where the atria beat irregularly, often quickly, disrupting the heart's normal rhythm.",
    "B": "Bradycardia is an abnormally slow heart rate that may require monitoring or treatment.",
    "BBB": "A bundle branch block is a delay or blockage in the electrical signals within the ventricles, affecting the heart's rhythm.",
    "BI": "Bigeminy is an arrhythmia where a normal heartbeat is followed by a premature beat, creating an irregular pattern.",
    "HGEA": "High-grade ectopic activity refers to frequent abnormal heartbeats originating from areas outside the sinus node.",
    "N": "Normal sinus rhythm represents a healthy heart function with a regular electrical impulse.",
    "NOD": "Nodal rhythm occurs when the atrioventricular node takes over heart rhythm regulation, which can be normal or abnormal.",
    "Ne": "Normal sinus rhythm with ectopic activity is characterized by extra abnormal beats in an otherwise regular rhythm.",
    "SBR": "Sinus bradycardia is a slow but regular sinus rhythm, often seen in athletes or during rest.",
    "SVTA": "Supraventricular tachycardia is a rapid heart rhythm originating from the atria or atrioventricular node.",
    "VER": "Ventricular escape rhythm occurs when the ventricles take over pacing in the absence of sinus or atrioventricular node control.",
    "VF": "Ventricular fibrillation is a medical emergency where the heart's electrical activity is chaotic, preventing effective blood pumping.",
    "VFL": "Ventricular flutter is a rapid, chaotic rhythm in the ventricles, often a precursor to ventricular fibrillation.",
    "VTHR": "Ventricular tachycardia with a high rate refers to a fast rhythm in the ventricles that requires urgent medical intervention.",
    "VTLR": "Ventricular tachycardia with a low rate presents a fast but more moderate rhythm that still needs monitoring.",
    "VTTdP": "Ventricular tachycardia with Torsades de Pointes is a dangerous form of tachycardia requiring immediate treatment."
};

// Function to get the color based on the risk percentage with 8 levels
const getRiskColor = (dangerLevel) => {
    if (dangerLevel >= 90) {
        return '#7F1D1D'; // Dark red for extremely high risk
    } else if (dangerLevel >= 80) {
        return '#B91C1C'; // Red for very high risk
    } else if (dangerLevel >= 70) {
        return '#DC2626'; // Lighter red for high risk
    } else if (dangerLevel >= 60) {
        return '#F87171'; // Light red for moderate-high risk
    } else if (dangerLevel >= 50) {
        return '#FBBF24'; // Yellow for moderate risk
    } else if (dangerLevel >= 40) {
        return '#FDE68A'; // Light yellow for moderate-low risk
    } else if (dangerLevel >= 30) {
        return '#34D399'; // Light green for low risk
    } else {
        return '#10B981'; // Dark green for very low risk
    }
}

// Function to get the message based on the risk percentage
const getRiskMessage = (dangerLevel) => {
    if (dangerLevel >= 90) {
        return 'Seek immediate medical attention or go to the hospital.';
    } else if (dangerLevel >= 80) {
        return 'Urgent consultation with a healthcare provider is recommended.';
    } else if (dangerLevel >= 70) {
        return 'Please consult your doctor as soon as possible.';
    } else if (dangerLevel >= 60) {
        return 'It is advised to schedule a visit with your healthcare provider soon.';
    } else if (dangerLevel >= 50) {
        return 'Consider a routine health check-up with your doctor.';
    } else if (dangerLevel >= 40) {
        return 'Take care of your health and inform your doctor at your next visit if you feel any discomfort.';
    } else if (dangerLevel >= 30) {
        return 'Everything seems fine, but regular health check-ups are always beneficial.';
    } else {
        return 'No immediate concern, but regular monitoring is a good practice.';
    }
}

// Function to get the description of a disease
const getDiseaseDescription = (name) => {
    switch (name) {
        case 'AFIB':
            return 'Atrial Fibrillation (AFIB) is an irregular and often rapid heart rate that occurs when the two upper chambers of the heart experience chaotic electrical signals. It can lead to blood clots, stroke, heart failure, and other heart-related complications.';
        case 'B':
            return 'Normal Sinus Rhythm (B) represents a regular heartbeat that starts at the sinoatrial node, typically ranging from 60 to 100 beats per minute in a healthy adult.';
        case 'BBB':
            return 'Bundle Branch Block (BBB) is a condition in which there’s a delay or blockage along the pathway that electrical impulses travel to make the heart beat. This may indicate an underlying cardiac issue.';
        case 'BI':
            return 'Myocardial Infarction (BI), commonly known as a heart attack, occurs when blood flow decreases or stops to a part of the heart, causing damage to the heart muscle.';
        case 'HGEA':
            return 'Generalized Atrial Enlargement (HGEA) indicates an abnormal enlargement of the atria, often seen in patients with chronic heart conditions such as hypertension or atrial fibrillation.';
        case 'N':
            return 'Normal Rhythm (N) refers to the expected, regular rhythm of the heart, with no noticeable abnormalities in the electrical activity as measured by an ECG.';
        case 'NOD':
            return 'Nodal Rhythm (NOD), also known as junctional rhythm, is a type of arrhythmia where the electrical activity originates from the atrioventricular node instead of the sinoatrial node.';
        case 'Ne':
            return 'Neonatal (Ne) describes the rhythm of a newborn’s heart. It is typically faster than that of an adult, often ranging from 120 to 160 beats per minute.';
        case 'SBR':
            return 'Severe Bradycardia (SBR) is a condition where the heart rate is significantly below the normal range, often under 40 beats per minute, which can cause dizziness, fatigue, or fainting.';
        case 'SVTA':
            return 'Supraventricular Tachycardia (SVTA) is an abnormally fast heartbeat that originates above the heart’s ventricles. It can cause dizziness, palpitations, and in some cases, chest pain.';
        case 'VER':
            return 'Ventricular Ectopic Rhythm (VER) refers to abnormal heartbeats that originate in the ventricles, the lower chambers of the heart. This condition can be harmless or indicate a more serious heart problem.';
        case 'VF':
            return 'Ventricular Fibrillation (VF) is a life-threatening condition where the heart quivers instead of pumping due to disorganized electrical activity in the ventricles. It requires immediate medical intervention.';
        case 'VFL':
            return 'Ventricular Flutter (VFL) is a fast and irregular heart rhythm originating from the ventricles, often leading to decreased cardiac output and potentially progressing to ventricular fibrillation.';
        case 'VTHR':
            return 'Ventricular Tachycardia Rapid (VTHR) is a fast but regular heart rhythm that originates in the ventricles. It can lead to reduced cardiac output and may require medical intervention if sustained.';
        case 'VTLR':
            return 'Ventricular Tachycardia Slow (VTLR) is a slower form of ventricular tachycardia, which can still affect heart function and cause symptoms like fatigue or shortness of breath.';
        case 'VTTdP':
            return 'Torsades de Pointes (VTTdP) is a rare and specific type of polymorphic ventricular tachycardia that can lead to sudden cardiac death if not treated promptly.';
        default:
            return 'No medical description available.';
    }
}

export { diseasesInfo, getRiskColor, getRiskMessage, getDiseaseDescription };