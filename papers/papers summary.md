# Summary of Related Articles

## Article 1: Alfouly et al. (2025)

**A Novel Inverter Control Strategy for Maximum Hosting Capacity PV Systems Using Power Factor**

### Problem

The study compares **Power Factor (PF)** control with **Volt-VAr** control for a grid-connected low-voltage (LV) PV system under both normal operating conditions and fault conditions, including short-circuit events.

### Methodology

The authors use **transient simulations in MATLAB/Simulink** based on a simple test system consisting of:

* One feeder
* One PV source rated at **100 kVA**
* One load rated at **10 kVA**

### Results

The study reports that **PF control provides more stable performance than Volt-VAr control**, particularly during fault conditions, including:

* Single-phase-to-ground faults
* Two-phase-to-ground faults
* Three-phase-to-ground faults

### Limitations

* Despite its title, the study **does not calculate hosting capacity quantitatively in kW**. Instead, it primarily evaluates qualitative voltage and power behavior.
* The test system is **highly simplified**, consisting of a single feeder and a single PV unit, which limits the generalizability of the findings to realistic multi-bus distribution networks.
* The reported conclusion that **PF control outperforms Volt-VAr control** appears inconsistent with commonly applied industry standards such as **IEEE 1547**, and the study does not provide sufficient physical explanation for this observation.
* The authors themselves acknowledge the need to investigate **more diverse load conditions** in future work.

---

## Article 2: Chathurangi et al. (2021)

**Comparative Evaluation of Solar PV Hosting Capacity Enhancement Using Volt-VAr and Volt-Watt Control Strategies**

### Problem

The study investigates which control strategy, **Volt-VAr or Volt-Watt**, is more effective for increasing the hosting capacity of solar PV systems.

### Methodology

The study compares the two control strategies on distribution feeders with **different conductor/cable types**. Based on the available abstract, the comparison considers differences between feeder configurations, although the detailed methodology could not be examined because the full text was not available.

### Results

The reported findings indicate that:

* **Volt-VAr control** is more effective for feeders using **bare overhead conductors**.
* **Volt-Watt control** is more effective for feeders using **underground cables**.

### Limitations

* The assessment is based **only on the available abstract**, as the full text was not accessible.
* Therefore, the detailed methodology, simulation conditions, network characteristics, and **quantitative results** require verification through the full paper, which is currently behind a **ScienceDirect paywall**.
