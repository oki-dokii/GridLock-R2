# Data Analysis Report: Parking Violations in Bengaluru

This report analyzes a dataset of **298,450 parking violations** recorded in Bengaluru, Karnataka, spanning from **November 9, 2023, to April 8, 2024** (approximately 5 months). 

The goal of this analysis is to identify key spatial, temporal, and operational patterns of illegal parking to help address the challenge of **Parking-Induced Congestion** and enable targeted, AI-driven enforcement.

---

```mermaid
mindmap
  root(("Bengaluru Parking<br>Violations"))
    "Spatial Hotspots"
      "Upparpet (Transit Hub)"
      "Shivajinagar (Commercial Hub)"
      "Outer Ring Road (IT Corridor)"
      "Hebbal (Highway Entry)"
    "Temporal Patterns"
      "Peak Hours (IST): 10 AM - 12 PM"
      "Weekly Peaks: Sundays & Saturdays"
      "Night Logging: 3 AM - 6 AM"
    "Violation Types"
      "Wrong Parking (55.3%)"
      "No Parking (46.6%)"
      "Main Road Parking (8.0%)"
      "Footpath Parking (1.3%)"
    "Vehicle Segments"
      "Two-Wheelers (45.5%)"
      "Cars (29.8%)"
      "Autos (12.7%)"
    "Validation Audit"
      "Approved (67%)"
      "Rejected (29%)"
      "Officer Discrepancy (1.8% to 86.8% rejection)"
```

---

## 1. Key Findings & Overview

- **100% Parking-Related**: Every record in the dataset contains at least one parking violation (e.g., "Wrong Parking", "No Parking", "Parking on Footpath").
- **High Rejection Rate**: Out of the ~172,000 cases that have been validated by authorities, **29% (49,754 cases) were rejected**. 
- **Two-Wheelers Rule**: Scooters and Motorcycles represent the largest group of offending vehicles, combining for **45.5%** of all logged violations.
- **Morning Rush Peak**: Violations peak sharply between **10:00 AM and 12:00 PM IST**, aligning with morning commute hours and the opening of commercial districts.
- **Weekend Spikes**: Sunday (50,162) and Saturday (44,523) see the highest number of violations, likely due to shopping, dining, and leisure traffic in commercial areas.

---

## 2. Violation Type Distribution

The dataset records multiple violations per vehicle event. The table below lists the most common violation types and their occurrence rates:

| Violation Type | Count | % of Total Dataset |
| :--- | :--- | :--- |
| **Wrong Parking** | 164,977 | 55.28% |
| **No Parking** | 139,050 | 46.59% |
| **Parking in a Main Road** | 23,943 | 8.02% |
| **Defective Number Plate** | 7,848 | 2.63% |
| **Parking on Footpath** | 3,757 | 1.26% |
| **Parking near Bus Stop/School/Hospital** | 2,403 | 0.81% |
| **Double Parking** | 2,037 | 0.68% |
| **Parking near Road Crossing** | 1,687 | 0.57% |
| **Refuse to Go for Hire** (Autos) | 887 | 0.30% |
| **Parking near Traffic Light or Zebra Crossing** | 525 | 0.18% |

> [!NOTE]
> Violations like "Defective Number Plate" and "Refuse to Go for Hire" co-occur with parking violations, as the enforcement mechanism records multiple issues during a single parking stop.

---

## 3. Offending Vehicle Categories

Analyzing the vehicle types involved reveals where enforcement should focus:

- **Two-Wheelers (Scooters + Motorcycles)**: **135,667 cases (45.5%)**
- **Cars**: **88,870 cases (29.8%)**
- **Passenger Autos**: **37,813 cases (12.7%)**
- **Commercial Vehicles (Maxi-Cabs, LGVs, Private Buses)**: **21,260 cases (7.1%)**

```
Two-Wheelers:   [====================] 45.5%
Cars:           [=============] 29.8%
Autos:          [======] 12.7%
Commercial/LGV: [===] 7.1%
```

---

## 4. Temporal Patterns (Indian Standard Time - IST)

The timestamps in the dataset were parsed and converted to **IST (UTC+5:30)** to reflect actual local behavior.

### Hour of the Day (IST)
The peak period for violations is mid-morning, with a significant secondary drop in the afternoon before rising again in the evening.

- **Peak Commute**: **10:00 AM - 12:00 PM** (32k+ per hour)
- **Morning Start**: **8:00 AM - 10:00 AM** (25k-27k per hour)
- **Early Morning Spike**: A notable volume of violations is logged between **3:00 AM and 6:00 AM IST** (~21k-23k per hour). This may be due to batch uploads from handheld devices, overnight parking checks, or shift-change data syncs.

### Day of the Week
Violations are heavily concentrated around weekends:
1. **Sunday**: 50,162
2. **Saturday**: 44,523
3. **Thursday**: 43,547
4. **Tuesday**: 42,697
5. **Wednesday**: 41,977
6. **Friday**: 40,864
7. **Monday**: 34,680 (Lowest)

---

## 5. Spatial Hotspots (Illegal Parking Zones)

Grouping by police station jurisdiction and coordinates (rounded to ~110m precision) reveals major bottleneck corridors in Bengaluru.

### Top 5 Police Stations
These five police stations represent **41.4%** of the entire dataset's violations:
1. **Upparpet** (34,468 cases) — Hub of transit (Majestic Bus Station, City Railway Station).
2. **Shivajinagar** (28,044 cases) — Highly congested commercial district and major bus terminus.
3. **Malleshwaram** (22,200 cases) — Traditional market streets (Sampige Road).
4. **HAL Old Airport** (20,819 cases) — Dense IT/office corridor and inner ring road.
5. **City Market** (17,646 cases) — Chaotic wholesale market area with heavy commercial vehicle loading.

### Top 5 Geographic Hotspots (Street Level)
1. **New Horizon College Road, Kadubeesanahalli (Outer Ring Road)**: ~6,200 violations (Embassy Tech Village & NHCE area). A massive tech park corridor known for severe bottlenecks.
2. **Kamaraj Road & Dickenson Road, Shivaji Nagar**: ~5,400 violations. Heavy commercial shopping district near Commercial Street.
3. **Bellary Road, Hebbal**: ~2,600 violations. A major arterial entry point to Bengaluru from the airport, prone to bottlenecking.
4. **MBT Road, Devasandra Junction, KR Puram**: ~3,000 violations. A crucial junction connecting East Bengaluru with the IT corridors.
5. **3rd Cross Road, Chickpete**: ~2,300 violations. Extremely narrow and congested wholesale market alleys.

---

## 6. Validation Audit & Data Quality Issues

An audit of the `validation_status` column reveals significant operational and data quality concerns:

- **Missing Validation**: **42.0% (125,254 cases)** have no validation status, indicating a large backlog of unreviewed cases.
- **High Rejection Rate**: **28.9%** of reviewed cases are marked as **rejected**. This represents wasted patrol resources and device errors.
- **Officer Discrepancy**: Rejection rates vary dramatically by the reporting officer (`created_by_id`).
  - Some officers have nearly perfect approval rates (e.g., `FKUSR01073` has **98.1% approved**).
  - Others have extremely high rejection rates (e.g., `FKUSR02046` has **86.8% rejected** out of 122 cases, and `FKUSR01903` has **82.7% rejected**).

> [!WARNING]
> The wide discrepancy in officer-level approval rates suggests that some hand-held devices are poorly calibrated, or certain officers are incorrectly logging standard parkings as violations, leading to heavy manual processing overhead.

---

## 7. Connecting to Traffic Congestion (Next Steps)

While the dataset lists parking violations, it does not include traffic speeds or travel times. To solve the problem statement (*"quantify their impact on traffic flow to enable targeted enforcement"*), we can:
1. **Correlate with Traffic Speed Data**: Overlay these parking hotspots with open-source traffic congestion datasets (like Google Maps API or TomTom Traffic Index) to measure speed drops during peak violation hours.
2. **Impact Index**: Create a "Congestion Impact Score" for each hotspot, defined by:
   $$\text{Impact Score} = \text{Violation Frequency} \times \text{Road Capacity Class} \times \text{Peak Hour Commute factor}$$
3. **AI Patrol Optimization**: Train an optimization model to route enforcement officers to high-impact hotspots *just before* peak violation hours (e.g., 9:30 AM), rather than reacting post-congestion.
