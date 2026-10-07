# Summary of Related Articles

Five articles are summarised. For each, the "Read" line states how much of the
article was actually read, so claims can be traced to a source.

---

## Article 1: Alfouly et al. (2025)

**A. Alfouly, M. A. Ismeil, I. Hamdan, "A novel inverter control strategy for maximum hosting capacity photovoltaic systems in distribution networks using power factor," PLOS ONE, vol. 20, e0310301, 2025. doi:10.1371/journal.pone.0310301**

Read: article text, key sections.

### Problem
The study compares **Power Factor (PF)** control with **Volt-VAr** control for a grid-connected low-voltage (LV) PV system under normal operating conditions and fault conditions, including short-circuit events.

### Methodology
Transient simulations in **MATLAB/Simulink** on a simple low-voltage network with a **100 kVA** PV system and a **10 kVA** aggregated load located 5 km from the feeder end.

### Results
PF control gives more stable performance than Volt-VAr control, particularly during faults (single-phase-to-ground, two-phase-to-ground, three-phase-to-ground). Reported power factor: 0.96 with PF control versus 0.74 with Volt-VAr control.

### Limitations
* Despite its title, the study does **not report hosting capacity in kW or MW**; it expresses improvement through power factor and percentage figures.
* The test system is **highly simplified** (one feeder, one PV unit, one load), which limits generalisation to multi-bus distribution networks.
* Thermal loading of network equipment does not appear in the evaluation (as far as the sections read show).
* The conclusion that PF control outperforms Volt-VAr appears inconsistent with commonly applied standards such as IEEE 1547, and no sufficient physical explanation is given.
* The authors acknowledge the need to study more diverse load conditions.

### Relevance to this project
Representative of studies that evaluate control strategies without thermal constraints and without kW-level hosting capacity.

---

## Article 2: Chathurangi et al. (2021)

**D. Chathurangi, U. Jayatunga, S. Perera, A. P. Agalgaonkar, T. Siyambalapitiya, "Comparative evaluation of solar PV hosting capacity enhancement using Volt-VAr and Volt-Watt control strategies," Renewable Energy, vol. 177, pp. 1063-1075, 2021. doi:10.1016/j.renene.2021.06.037**

Read: abstract only (full text behind a ScienceDirect paywall).

### Problem
Which control strategy, **Volt-VAr or Volt-Watt**, is more effective for increasing the hosting capacity of solar PV systems.

### Methodology
Both strategies are compared on feeders with **different conductor and cable types**. Detailed methodology could not be examined.

### Results
* Volt-VAr is more effective for feeders with **bare overhead conductors**.
* Volt-Watt is more effective for feeders with **underground cables**.

### Limitations
* Based on the abstract only; methodology, simulation conditions and quantitative results need verification in the full paper.
* The interaction between reactive power support and transformer thermal limits is not examined (as far as the abstract shows).

### Relevance to this project
The closest prior comparison of Volt-VAr and Volt-Watt. This project adds thermal limits and the distinction between nameplate and delivered capacity.

---

## Article 3: Ame-Oko and Lavrova (2024)

**A. Ame-Oko, O. Lavrova, "Mitigation of limitation imposed on hosting capacity in low voltage networks by their distribution transformer loading and degradation considerations," IET Energy Systems Integration, 2024. doi:10.1049/esi2.12143**

Read: abstract only.

### Problem
The thermal condition of the distribution transformer limits PV hosting capacity in LV networks.

### Methodology
Examines how transformer loading and degradation affect hosting capacity, then proposes a **battery energy storage system (BESS) dispatch strategy** to mitigate the limit. Three scenarios: no transformer restriction, with restriction, and with the BESS strategy.

### Results
* Without restriction, transformer lifetime is consumed to about 6% of expected lifetime.
* Restricting HC (a 32% curtailment) brings lifetime to 149% of expected.
* With the BESS strategy, lifetime is 127% of expected and HC is 62% above the curtailed value and 10% above the original HC.

### Limitations
* Mitigation is by storage, not by inverter control.
* Network details were not checked (abstract only).

### Relevance to this project
Independent evidence that the transformer is a binding hosting-capacity constraint, and an example of a measure that lifts the thermal ceiling.

---

## Article 4: Qamar et al. (2023)

**N. Qamar, A. Arshad, K. Mahmoud, M. Lehtonen, "Hosting capacity in distribution grids: A review of definitions, performance indices, determination methodologies, and enhancement techniques," Energy Science & Engineering, 2023. doi:10.1002/ese3.1389**

Read: the part of the review on DSO limits (Table 1) and the abstract; not read in full.

### Problem
Review of how hosting capacity is defined, measured, determined and enhanced.

### Relevant content
Table 1 lists DSO rules limiting distributed generation to a fraction of the MV/LV transformer rating: Portugal below 25%, Spain below 50%, Italy below 65%, South Africa below 50%, and Belgium below the full transformer rating.

### Limitations (for this project)
A review, not a feeder-level comparison of Volt-VAr and Volt-Watt.

### Relevance to this project
Confirms the practical relevance of the transformer constraint.

---

## Article 5: Dissanayake et al. (2022)

**R. Dissanayake, A. Wijethunge, J. Wijayakulasooriya, J. Ekanayake, "Optimizing PV-Hosting Capacity with the Integrated Employment of Dynamic Line Rating and Voltage Regulation," Energies, vol. 15, no. 22, 8537, 2022. doi:10.3390/en15228537**

Read: abstract and the case-study description.

### Problem
Maximise PV hosting capacity of an LV network by combining dynamic line rating, voltage regulation and PV re-phasing.

### Methodology
Optimisation framework (MATLAB `fmincon`) with dynamic line rating from IEEE 738 thermal equations, coordinated on-load tap changer and reactive power compensation, and PV re-phasing. Case study: one real LV network in Sri Lanka, **25 nodes, 40 households**, with fixed PV locations.

### Results
* Base case (static line rating and tap changer): 204.4 kW.
* Dynamic line rating with tap changer: 288.0 kW (+40.9%).
* Plus coordinated tap changer and reactive compensation: 313.8 kW.
* Plus re-phasing: 314.3 kW (+53.5% overall).

### Limitations
* A single network, located in an equatorial country; the authors recommend simulation with summer data in a non-equatorial country.
* Does not compare Volt-VAr and Volt-Watt.

### Relevance to this project
Combines voltage control with a thermal measure on a real network, but on a single topology.
