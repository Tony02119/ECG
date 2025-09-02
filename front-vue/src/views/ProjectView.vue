<script setup>
</script>

<template>
  <section class="bg-red-800 min-h-screen">
    <div class="container m-auto max-w-3xl py-24">
      <div class="bg-white px-4 md:px-8 py-8 mb-4 shadow-md rounded-md border">
        <!-- Titre du projet -->
        <h2 class="text-3xl text-center font-semibold mb-8">ECG Analysis Project</h2>

        <!-- Description générale du projet -->
        <div class="mb-6">
          <p class="text-gray-700 mb-4">
            This project demonstrates the use of AI models for ECG analysis from different patients. Our goal is to analyze ECG data to detect dangerous arrhythmias that could indicate a cardiovascular risk.
          </p>
        </div>

        <!-- Section ajoutée : Comprendre l'ECG et la détection des arythmies -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold mb-2">Understanding the Electrocardiogram (ECG) and the Detection of Cardiac Arrhythmias</h3>
          <p class="text-gray-700 mb-4">
            The electrocardiogram (ECG) is a fundamental medical tool that records the heart's electrical activity and enables its rhythms to be analyzed. The ECG helps diagnose a variety of conditions, including arrhythmias, which are irregularities in the frequency or regularity of the heartbeat.
          </p>
          <p class="text-gray-700 mb-4">
            Our AI project is designed to detect different forms of arrhythmia based on ECG analysis. We use AI trained on medical databases, such as Physionet, and classify arrhythmias into 6 main classes, which are further subdivided into 14 subclasses.
          </p>

          <h4 class="text-lg font-semibold mb-2">How to read an ECG</h4>
          <p class="text-gray-700 mb-4">
            An ECG trace is generally made up of several waves:
          </p>
          <ul class="list-disc list-inside mb-4">
            <li><strong>P wave:</strong> Represents depolarization of the atria (contraction of the atria).</li>
            <li><strong>QRS complex:</strong> Corresponds to ventricular depolarization (ventricular contraction).</li>
            <li><strong>T wave:</strong> Represents ventricular repolarization (ventricular relaxation).</li>
          </ul>
          <p class="text-gray-700 mb-4">
            Analysis of the intervals between these waves and the shape of each complex helps diagnose various cardiac pathologies.
          </p>

          <!-- Insertion de l'image ici -->
          <div class="mb-6 text-center">
            <img src="../assets/img/ecg_description.png" alt="ECG Description" class="w-auto h-auto rounded-md shadow-lg mx-auto" />
            <i>ECG of a heart in normal sinus rhythm</i>
          </div>

          <!-- Vidéo YouTube intégrée -->
          <div class="mb-4">
            <h3 class="text-xl font-semibold mb-2">Understanding ECG and How to Analyze It</h3>
            <p class="text-gray-700 mb-4">
              The following video explains how ECGs work and how to analyze them effectively.
            </p>
            <!-- Intégration de la vidéo YouTube -->
            <div class="video-container">
              <iframe
                  class="w-full h-64 md:h-80"
                  src="https://www.youtube.com/embed/FP0QuLfV9_0"
                  title="YouTube video player"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen
              ></iframe>
            </div>
          </div>

          <h4 class="text-lg font-semibold mb-2">Recognizing arrhythmias from ECGs</h4>
          <p class="text-gray-700 mb-4">
            <strong>1. AFIB (Atrial Fibrillation)</strong><br>
            Atrial Fibrillation (AFIB) is characterized by rapid and irregular electrical activity in the atria, leading to irregular heartbeats. On the ECG, this is seen as the absence of distinct P waves and an irregularly irregular R-R interval. The atria quiver rather than contracting effectively, which can lead to blood clot formation and increase the risk of stroke.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>2. B (Bradycardia)</strong><br>
            Bradycardia (B) refers to a slower-than-normal heart rate, typically defined as fewer than 60 beats per minute in adults. On the ECG, the intervals between the QRS complexes are prolonged, but the waveforms (P wave, QRS complex, and T wave) are usually normal.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>3. BBB (Bundle Branch Block)</strong><br>
            A Bundle Branch Block (BBB) occurs when there's a delay or blockage along the electrical pathway that makes the heart beat. It can affect either the right or left bundle branch. On an ECG, BBB is identified by a widened QRS complex, greater than 120 ms, and often specific patterns in the QRS morphology depending on which branch is blocked.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>4. BI (Bifascicular Block)</strong><br>
            Bifascicular Block (BI) is the combination of right bundle branch block (RBBB) and a block in one of the fascicles of the left bundle branch. On the ECG, this condition presents as a prolonged QRS complex with RBBB features and left-axis deviation.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>5. HGEA (High-Grade Ectopic Atrial Activity)</strong><br>
            High-Grade Ectopic Atrial Activity (HGEA) involves abnormal electrical impulses originating outside the sinoatrial node, leading to irregular atrial contractions. The ECG shows premature atrial complexes (PACs), with the ectopic P waves often differing in morphology from sinus P waves.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>6. N (Normal ECG)</strong><br>
            A Normal ECG (N) shows regular heart rhythm, typically with a heart rate between 60-100 beats per minute. The P waves, QRS complexes, and T waves are all distinct and properly timed, reflecting normal electrical activity within the heart.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>7. NOD (Nodal Rhythm)</strong><br>
            Nodal Rhythm (NOD), also known as junctional rhythm, occurs when the electrical impulse originates from the atrioventricular (AV) node rather than the sinoatrial (SA) node. The ECG often shows an absence of P waves or inverted P waves, with regular and narrow QRS complexes.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>8. Ne (Nodal Escape Rhythm)</strong><br>
            Nodal Escape Rhythm (Ne) is a type of junctional rhythm that occurs when the SA node fails to fire, and the AV node takes over as the pacemaker. The ECG typically shows slow, regular heartbeats with narrow QRS complexes, and P waves may be absent or follow the QRS complex.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>9. SBR (Sinus Bradycardia)</strong><br>
            Sinus Bradycardia (SBR) is a slower-than-normal heart rate that originates from the sinoatrial (SA) node. The ECG shows a regular rhythm with a rate less than 60 beats per minute, but the P waves, QRS complexes, and T waves are otherwise normal.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>10. SVTA (Supraventricular Tachycardia)</strong><br>
            Supraventricular Tachycardia (SVTA) is an abnormally fast heart rate that originates above the ventricles. The ECG shows a rapid heart rate with narrow QRS complexes, often without distinct P waves. SVTA can lead to symptoms like palpitations, dizziness, and chest pain.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>11. VER (Ventricular Escape Rhythm)</strong><br>
            Ventricular Escape Rhythm (VER) occurs when the ventricles take over as the pacemaker of the heart, often due to failure of higher pacemakers like the SA or AV node. The ECG shows a slow heart rate with wide and abnormal QRS complexes, as the electrical impulse spreads slowly through the ventricles.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>12. VF (Ventricular Fibrillation)</strong><br>
            Ventricular Fibrillation (VF) is a life-threatening condition where the ventricles quiver rather than contract properly, preventing effective blood flow. On the ECG, VF appears as rapid, chaotic electrical activity with no discernible P waves, QRS complexes, or T waves. Immediate medical intervention, such as defibrillation, is required.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>13. VFL (Ventricular Flutter)</strong><br>
            Ventricular Flutter (VFL) is characterized by a very fast ventricular rhythm, usually over 250 beats per minute. On the ECG, the QRS complexes are wide and have a sine wave pattern, with no distinct separation between them. Like VF, VFL is a medical emergency.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>14. VTHR (Ventricular Tachycardia High Risk)</strong><br>
            Ventricular Tachycardia High Risk (VTHR) refers to a specific type of ventricular tachycardia associated with a high risk of progressing to ventricular fibrillation or cardiac arrest. The ECG shows a very fast heart rate originating in the ventricles, with wide QRS complexes and no visible P waves.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>15. VTLR (Ventricular Tachycardia Low Risk)</strong><br>
            Ventricular Tachycardia Low Risk (VTLR) refers to ventricular tachycardia that is less likely to deteriorate into more serious arrhythmias. The ECG shows wide QRS complexes with regular rhythm, but the rate may be slower than in high-risk cases of VT.
          </p>

          <p class="text-gray-700 mb-4">
            <strong>16. VTTdP (Ventricular Tachycardia with Torsades de Pointes)</strong><br>
            Ventricular Tachycardia with Torsades de Pointes (VTTdP) is a specific form of ventricular tachycardia with a characteristic twisting of the QRS complexes around the baseline. The ECG shows a pattern of undulating QRS amplitude, which is potentially life-threatening and requires prompt treatment.
          </p>

          <h4 class="text-lg font-semibold mb-2">The importance of detecting cardiac arrhythmias</h4>
          <p class="text-gray-700 mb-4">
            Early detection of arrhythmias is crucial to avoid serious complications such as stroke or cardiac arrest. By analyzing an ECG, our artificial intelligence-based system can identify and classify these arrhythmias with high accuracy.
          </p>

          <h4 class="text-lg font-semibold mb-2">Conclusion</h4>
          <p class="text-gray-700 mb-4">
            Thanks to medical databases such as Physionet and our AI, we have developed a solution capable of detecting and classifying many forms of arrhythmia. This technology has the potential to revolutionize the early diagnosis of heart disease and save lives through rapid intervention.
          </p>
        </div>

        <!-- Remerciements -->
        <div class="text-center">
          <p class="text-gray-700 font-semibold">
            Thank you for exploring our ECG analysis project. We hope this tool aids you in improving cardiac health assessments.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
h2 {
  color: #333;
}

p, ul {
  line-height: 1.6;
}

label {
  display: block;
  margin-bottom: 8px;
}

.container {
  max-width: 72rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  text-align: justify;
}
</style>