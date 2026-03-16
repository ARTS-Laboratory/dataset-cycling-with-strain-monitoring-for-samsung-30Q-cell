# 📘 Cell_Combined_Cycle_Plot Script
This script loads charge and discharge .lvm files for each battery cell, aligns their timestamps, merges them into a single continuous dataset, removes invalid strain spikes, detects strain‑based cycling events, and generates a strain‑vs‑time plot with peak markers.

## 🔍 What the Script Does
For each cell, the script:
```text
- Loads the charge and discharge files
- Drops rows with missing current or voltage
- Converts time from seconds to hours
- Converts strain to microstrain
- Computes milliamp‑hours using the trapezoidal rule
- Detects the timestamp jump between charge and discharge
- Shifts the discharge timestamps so both datasets align
- Merges charge and discharge into a single .lvm file
- Removes strain outliers (for cell3 only)
- Detects strain peaks to estimate the number of cycles
- Plots strain vs. time and highlights the detected peaks

This produces a clean, continuous dataset and a visual representation of strain cycling behavior.
```
## ▶️ How to Use the Script
### 1. Place your data files
Each cell must have:
```text
Charge file:    *_ChargeCycle1.lvm
Discharge file: *_DischargeCycle1.lvm

The script automatically loads them based on the cells dictionary.
```
### 2. Run the script
The script will:
```text
- Load and clean the charge and discharge data
- Align the discharge timestamps to follow the charge data
- Merge both into a single continuous .lvm file
- Detect strain peaks
- Count the number of cycles
- Generate a strain plot with peak markers
```
### 3. View the merged output
For each cell, the script writes:
```text
cell1.lvm
cell2.lvm
cell3.lvm

These contain the combined charge+discharge dataset sorted by time.
```
### 4. Inspect the cycle count
The script prints:
```text
Number of cycles: X

This is based on the number of positive strain peaks detected.
```
### 5. View the generated plot
Each plot shows:
```text
- Strain vs. time
- Red markers at detected peaks
- A title indicating the cell
- Dual y‑axes (strain and max strain)

This helps visualize mechanical cycling behavior.
```
## 🧭 Processing Diagram
```text
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
   │ Clean data (drop NaNs, convert units)│
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Detect timestamp jump between files  │
   │ Shift discharge timestamps           │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Merge charge + discharge into one file│
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Remove strain outliers (cell3 only)  │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Detect strain peaks and count cycles │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Plot strain vs. time with peaks      │
   └──────────────────────────────────────┘
```

## 🔢 Explanation of Key Computations
```text
Timestamp Alignment
The script finds the first large jump in the charge file’s time column.
This jump marks the end of charge and the start of discharge.
The discharge timestamps are shifted forward by this amount so both datasets form a continuous timeline.
Milliamp‑Hour Calculation
The script uses the trapezoidal rule:
mAh = cumulative sum of (average current * time difference * 1000)

This produces a smooth estimate of charge throughput.
Strain Peak Detection
The script identifies peaks in the strain signal using:
- Minimum distance between peaks
- Minimum prominence
- Positive strain only
The number of detected peaks corresponds to the number of mechanical cycles.
```
## 📄 Example Output
Number of cycles: 147

A plot is displayed showing strain vs. time with red peak markers.
![Cell 1 Plot](./images/Cell1.png)


# 🔋 Capacity_Extractor
A lightweight, cycle‑aware capacity analysis tool for battery test data.
This script processes charge/discharge .lvm files, detects cycle boundaries, computes per‑cycle capacities, and exports clean summary files for each cell.

## 📘 Overview
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
All results are written to a dedicated Capacity/ folder.

## ⚙️ How the Script Works
### 1. Load charge and discharge data
```text
For each cell, the script loads:
Charge file:    *_ChargeCycle*.lvm
Discharge file: *_DischargeCycle*.lvm
```

You define these in the cells dictionary.

### 2. Detect cycles automatically
Cycles are identified by:
- Timestamp resets
- Large time gaps (configurable threshold)
Each cycle is processed independently.

### 3. Compute charge capacity
- Cycle 1 uses the cell’s QSTART offset:
```text
Qc1 = QSTART + ∫ I_charge dt
```
- Cycles 2 and higher start from 0.1 offset:
```text
Qc(n>=2) = Q + ∫ I_charge dt
```
### 4. Compute discharge Capacity
Discharge always begins from the charge capacity of the same cycle:
```text
Qd(n) = Qc(n) - ∫ |I_discharge| dt
```
### 5. Export results
For each cell, the script writes:
```text
Capacity/cellX_capacity_summary.lvm
```

## ▶️ How to Use the Script
### 1. Add your data files
Place your .lvm charge/discharge files in the same directory as the script.
Update the cells dictionary:
```text
cells = {
    "cell1": ["_1__ChargeCycle1.lvm","_1__DischargeCycle1.lvm"],
    "cell2": ["_2__ChargeCycle1.lvm","_2__DischargeCycle1.lvm"],
    "cell3": ["_3__ChargeCycle1.lvm","_3__DischargeCycle1.lvm"]
}
```


### 2. Set QSTART for each cell
QSTART is applied only to cycle 1:
```text
QSTARTS = {
    "cell1": 1.50,
    "cell2": 1.40,
    "cell3": 1.60
}
```


### 3. Run the script
It will:
- Detect cycles
- Compute charge/discharge capacities
- Save summary files in Capacity/
- No user interaction required.

### 4. View the output
Example:
```text
Cycle	ChargeCapacity_Ah	RemainingCapacity_after_Discharge_Ah
1	    4.32		        0.22
2	    2.79		        0.25
3	    2.75		        0.28
```


## 🧭 Processing Flow
```text
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
   │ Compute charge capacity per cycle    │
   │ (QSTART added only to cycle 1)       │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Compute discharge capacity per cycle │
   │ (starts from charge capacity)        │
   └──────────┬───────────────────────────┘
              │
              ▼
   ┌──────────────────────────────────────┐
   │ Save summary file in SOC/ folder     │
   └──────────────────────────────────────┘
```


## 📂 Output Directory Structure
```text
project/
├── Capacity_Extractor.py
├── _1__ChargeCycle1.lvm
├── _1__DischargeCycle1.lvm
├── _2__ChargeCycle1.lvm
├── _2__DischargeCycle1.lvm
│
└── Capacity/
    ├── cell1_capacity_summary.lvm
    ├── cell2_capacity_summary.lvm
    └── cell3_capacity_summary.lvm
```



