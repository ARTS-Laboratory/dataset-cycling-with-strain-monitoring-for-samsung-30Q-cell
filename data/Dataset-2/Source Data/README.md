🔋 Capacity_Extractor
A lightweight, cycle‑aware capacity analysis tool for battery test data.
This script processes charge/discharge .lvm files, detects cycle boundaries, computes per‑cycle capacities, and exports clean summary files for each cell.

📘 Overview
The Capacity_Extractor script computes per‑cycle charge and discharge capacities for multiple battery cells. It is designed for datasets where:
- Each cell has separate charge and discharge files
- Cycles are embedded within each file
- Time resets or large time gaps indicate new cycles
- The initial SOC is unknown, so each cell receives its own QSTART offset
The script ensures:
- QSTART applies only to cycle 1 (per cell)
- Every other cycle starts from zero
- Discharge capacity continues from the charge capacity of the same cycle
- No cross‑cycle carry‑over
- Capacity fade emerges naturally as integrals shrink with age
All results are written to a dedicated SOC/ folder.

⚙️ How the Script Works
1. Load charge and discharge data
For each cell, the script loads:
Charge file:    *_ChargeCycle*.lvm
Discharge file: *_DischargeCycle*.lvm


You define these in the cells dictionary.

2. Detect cycles automatically
Cycles are identified by:
- Timestamp resets
- Large time gaps (configurable threshold)
Each cycle is processed independently.

3. Compute charge capacity
For each cycle:
- Integrate current over time
- If it’s cycle 1, add the cell’s QSTART
- Otherwise, start from zero
Mathematically:
Q_{c1}=Q_{\mathrm{START}}+\int I_{\mathrm{charge}}dt
Q_{c,n\geq 2}=\int I_{\mathrm{charge}}dt

4. Compute discharge capacity
Discharge always continues from the charge capacity of the same cycle:
Q_{d,n}=Q_{c,n}-\int |I_{\mathrm{discharge}}|dt
This produces a physically meaningful “remaining capacity” after discharge.

5. Export results
For each cell, the script writes:
SOC/cellX_capacity_summary.lvm


Each file contains:
|  |  | 
|  |  | 
|  |  | 
|  |  | 



▶️ How to Use the Script
1. Add your data files
Place your .lvm charge/discharge files in the same directory as the script.
Update the cells dictionary:
cells = {
    "cell1": ["_1__ChargeCycle1.lvm","_1__DischargeCycle1.lvm"],
    "cell2": ["_2__ChargeCycle1.lvm","_2__DischargeCycle1.lvm"],
    "cell3": ["_3__ChargeCycle1.lvm","_3__DischargeCycle1.lvm"]
}



2. Set QSTART for each cell
QSTART is applied only to cycle 1:
QSTARTS = {
    "cell1": 1.50,
    "cell2": 1.40,
    "cell3": 1.60
}



3. Run the script
It will:
- Detect cycles
- Compute charge/discharge capacities
- Save summary files in SOC/
No user interaction required.

4. View the output
Example:
Cycle	ChargeCapacity_Ah	RemainingCapacity_after_Discharge_Ah
1	    4.32		        0.22
2	    2.79		        0.25
3	    2.75		        0.28



🧭 Processing Flow
          ┌──────────────────────────┐
          │     Start the script     │
          └──────────┬──────────────┘
                     │
                     ▼
      ┌────────────────────────────────┐
      │ Load charge & discharge files  │
      └──────────┬─────────────────────┘
                 │
                 ▼
   ┌──────────────────────────────────────┐
   │ Detect cycles from timestamp jumps   │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Compute charge capacity per cycle     │
   │ (QSTART added only to cycle 1)        │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Compute discharge capacity per cycle  │
   │ (starts from charge capacity)         │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Save summary file in SOC/ folder     │
   └──────────────────────────────────────┘



📂 Output Directory Structure
project/
│
├── Capacity_Extractor.py
├── _1__ChargeCycle1.lvm
├── _1__DischargeCycle1.lvm
├── _2__ChargeCycle1.lvm
├── _2__DischargeCycle1.lvm
│
└── SOC/
    ├── cell1_capacity_summary.lvm
    ├── cell2_capacity_summary.lvm
    └── cell3_capacity_summary.lvm




