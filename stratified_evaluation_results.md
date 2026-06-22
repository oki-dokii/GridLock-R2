# Stratified Evaluation Results

This report measures classification metrics (Precision, Recall, F1, Accuracy) for our models' Predicted Top-K hotspots against actual Top-K subgroups.

## Findings: Operational Blind Spots

- **Lowest Precision Subgroup (K=20):** `Adugodi` (police_station) with GLM-Ensemble | Global Precision: 0.0% (n=1286)
- **Lowest Recall Subgroup (K=20):** `Adugodi` (police_station) with GLM-Ensemble | Global Recall: 0.0% (n=1286)

---

## Overall Metrics

| Subgroup | Model | Global K | Precision | Global Recall | Within-Group Recall (Top 20%) | F1 Score | Accuracy (vs Base Rate) | n (test) |
|---|---|---|---|---|---|---|---|---|
| Overall | GLM-Ensemble | 20 | 88.3% | 88.3% | **88.3%** | 0.883 | 99.6% (BR: 98.3%) | 107943 |
| Overall | XGBoost | 20 | 65.0% | 65.0% | **65.0%** | 0.650 | 99.8% (BR: 99.7%) | 107943 |
| Overall | GLM-Ensemble | 50 | 80.7% | 80.7% | **80.7%** | 0.807 | 98.4% (BR: 95.9%) | 107943 |
| Overall | XGBoost | 50 | 68.0% | 68.0% | **68.0%** | 0.680 | 99.4% (BR: 99.1%) | 107943 |

## By Vehicle Type

| Subgroup | Model | Global K | Precision | Global Recall | Within-Group Recall (Top 20%) | F1 Score | Accuracy (vs Base Rate) | n (test) |
|---|---|---|---|---|---|---|---|---|
| BUS (BMTC/KSRTC) | GLM-Ensemble | 20 | 15.0% | 15.0% | **44.2%** | 0.150 | 97.2% (BR: 98.3%) | 588 |
| BUS (BMTC/KSRTC) | XGBoost | 20 | 1.7% | 1.7% | **32.4%** | 0.017 | 99.3% (BR: 99.7%) | 588 |
| BUS (BMTC/KSRTC) | GLM-Ensemble | 50 | 18.7% | 26.2% | **44.2%** | 0.218 | 94.5% (BR: 95.9%) | 588 |
| BUS (BMTC/KSRTC) | XGBoost | 50 | 2.7% | 2.8% | **32.4%** | 0.027 | 98.3% (BR: 99.1%) | 588 |
| CAR | GLM-Ensemble | 20 | 68.3% | 68.3% | **74.3%** | 0.683 | 99.0% (BR: 98.3%) | 34805 |
| CAR | XGBoost | 20 | 21.7% | 21.7% | **61.0%** | 0.217 | 99.5% (BR: 99.7%) | 34805 |
| CAR | GLM-Ensemble | 50 | 63.3% | 63.3% | **74.3%** | 0.633 | 97.0% (BR: 95.9%) | 34805 |
| CAR | XGBoost | 50 | 45.3% | 45.3% | **61.0%** | 0.453 | 99.1% (BR: 99.1%) | 34805 |
| FACTORY BUS | GLM-Ensemble | 20 | 1.7% | 2.2% | **4.8%** | 0.019 | 97.1% (BR: 98.3%) | 98 |
| FACTORY BUS | XGBoost | 20 | 0.0% | 0.0% | **22.1%** | 0.000 | 99.3% (BR: 99.7%) | 98 |
| FACTORY BUS | GLM-Ensemble | 50 | 4.7% | 14.2% | **4.8%** | 0.070 | 94.9% (BR: 95.9%) | 98 |
| FACTORY BUS | XGBoost | 50 | 2.0% | 4.7% | **22.1%** | 0.028 | 98.8% (BR: 99.1%) | 98 |
| GOODS AUTO | GLM-Ensemble | 20 | 51.7% | 51.7% | **43.3%** | 0.517 | 98.4% (BR: 98.3%) | 1262 |
| GOODS AUTO | XGBoost | 20 | 20.0% | 20.0% | **30.6%** | 0.200 | 99.5% (BR: 99.7%) | 1262 |
| GOODS AUTO | GLM-Ensemble | 50 | 40.7% | 40.7% | **43.3%** | 0.407 | 95.1% (BR: 95.9%) | 1262 |
| GOODS AUTO | XGBoost | 50 | 15.3% | 15.3% | **30.6%** | 0.153 | 98.6% (BR: 99.1%) | 1262 |
| HGV | GLM-Ensemble | 20 | 10.0% | 10.0% | **22.0%** | 0.100 | 97.0% (BR: 98.3%) | 531 |
| HGV | XGBoost | 20 | 5.0% | 5.0% | **20.9%** | 0.050 | 99.3% (BR: 99.7%) | 531 |
| HGV | GLM-Ensemble | 50 | 14.0% | 14.0% | **22.0%** | 0.140 | 92.9% (BR: 95.9%) | 531 |
| HGV | XGBoost | 50 | 2.7% | 2.7% | **20.9%** | 0.027 | 98.3% (BR: 99.1%) | 531 |
| JEEP | GLM-Ensemble | 20 | 41.7% | 41.7% | **39.4%** | 0.417 | 98.1% (BR: 98.3%) | 361 |
| JEEP | XGBoost | 20 | 11.7% | 11.7% | **30.4%** | 0.117 | 99.4% (BR: 99.7%) | 361 |
| JEEP | GLM-Ensemble | 50 | 37.3% | 37.3% | **39.4%** | 0.373 | 94.8% (BR: 95.9%) | 361 |
| JEEP | XGBoost | 50 | 18.0% | 18.0% | **30.4%** | 0.180 | 98.6% (BR: 99.1%) | 361 |
| LGV | GLM-Ensemble | 20 | 51.7% | 51.7% | **50.3%** | 0.517 | 98.4% (BR: 98.3%) | 3670 |
| LGV | XGBoost | 20 | 25.0% | 25.0% | **35.7%** | 0.250 | 99.5% (BR: 99.7%) | 3670 |
| LGV | GLM-Ensemble | 50 | 40.0% | 40.0% | **50.3%** | 0.400 | 95.0% (BR: 95.9%) | 3670 |
| LGV | XGBoost | 50 | 26.0% | 26.0% | **35.7%** | 0.260 | 98.7% (BR: 99.1%) | 3670 |
| LORRY/GOODS VEHICLE | GLM-Ensemble | 20 | 10.0% | 10.0% | **22.7%** | 0.100 | 97.0% (BR: 98.3%) | 523 |
| LORRY/GOODS VEHICLE | XGBoost | 20 | 0.0% | 0.0% | **14.1%** | 0.000 | 99.3% (BR: 99.7%) | 523 |
| LORRY/GOODS VEHICLE | GLM-Ensemble | 50 | 17.3% | 17.3% | **22.7%** | 0.173 | 93.2% (BR: 95.9%) | 523 |
| LORRY/GOODS VEHICLE | XGBoost | 50 | 2.0% | 2.0% | **14.1%** | 0.020 | 98.3% (BR: 99.1%) | 523 |
| MAXI-CAB | GLM-Ensemble | 20 | 35.0% | 35.0% | **47.6%** | 0.350 | 97.8% (BR: 98.3%) | 4644 |
| MAXI-CAB | XGBoost | 20 | 6.7% | 6.7% | **41.2%** | 0.067 | 99.4% (BR: 99.7%) | 4644 |
| MAXI-CAB | GLM-Ensemble | 50 | 37.3% | 37.3% | **47.6%** | 0.373 | 94.8% (BR: 95.9%) | 4644 |
| MAXI-CAB | XGBoost | 50 | 15.3% | 15.3% | **41.2%** | 0.153 | 98.5% (BR: 99.1%) | 4644 |
| MINI LORRY | GLM-Ensemble | 20 | 20.0% | 21.2% | **29.4%** | 0.205 | 97.4% (BR: 98.3%) | 75 |
| MINI LORRY | XGBoost | 20 | 3.3% | 3.3% | **18.9%** | 0.033 | 99.3% (BR: 99.7%) | 75 |
| MINI LORRY | GLM-Ensemble | 50 | 14.0% | 34.5% | **29.4%** | 0.198 | 95.3% (BR: 95.9%) | 75 |
| MINI LORRY | XGBoost | 50 | 2.7% | 5.6% | **18.9%** | 0.036 | 98.8% (BR: 99.1%) | 75 |
| MOPED | GLM-Ensemble | 20 | 46.7% | 46.7% | **39.4%** | 0.467 | 98.2% (BR: 98.3%) | 799 |
| MOPED | XGBoost | 20 | 26.7% | 26.7% | **32.6%** | 0.267 | 99.5% (BR: 99.7%) | 799 |
| MOPED | GLM-Ensemble | 50 | 34.7% | 34.7% | **39.4%** | 0.347 | 94.6% (BR: 95.9%) | 799 |
| MOPED | XGBoost | 50 | 25.3% | 25.3% | **32.6%** | 0.253 | 98.7% (BR: 99.1%) | 799 |
| MOTOR CYCLE | GLM-Ensemble | 20 | 73.3% | 73.3% | **64.9%** | 0.733 | 99.1% (BR: 98.3%) | 12940 |
| MOTOR CYCLE | XGBoost | 20 | 46.7% | 46.7% | **55.0%** | 0.467 | 99.6% (BR: 99.7%) | 12940 |
| MOTOR CYCLE | GLM-Ensemble | 50 | 68.0% | 68.0% | **64.9%** | 0.680 | 97.3% (BR: 95.9%) | 12940 |
| MOTOR CYCLE | XGBoost | 50 | 50.0% | 50.0% | **55.0%** | 0.500 | 99.1% (BR: 99.1%) | 12940 |
| OTHERS | GLM-Ensemble | 20 | 35.0% | 35.0% | **29.6%** | 0.350 | 97.9% (BR: 98.3%) | 340 |
| OTHERS | XGBoost | 20 | 6.7% | 6.7% | **26.4%** | 0.067 | 99.4% (BR: 99.7%) | 340 |
| OTHERS | GLM-Ensemble | 50 | 28.7% | 28.7% | **29.6%** | 0.287 | 94.1% (BR: 95.9%) | 340 |
| OTHERS | XGBoost | 50 | 10.0% | 10.0% | **26.4%** | 0.100 | 98.5% (BR: 99.1%) | 340 |
| PASSENGER AUTO | GLM-Ensemble | 20 | 63.3% | 63.3% | **66.2%** | 0.633 | 98.8% (BR: 98.3%) | 14470 |
| PASSENGER AUTO | XGBoost | 20 | 40.0% | 40.0% | **54.3%** | 0.400 | 99.6% (BR: 99.7%) | 14470 |
| PASSENGER AUTO | GLM-Ensemble | 50 | 62.7% | 62.7% | **66.2%** | 0.627 | 96.9% (BR: 95.9%) | 14470 |
| PASSENGER AUTO | XGBoost | 50 | 42.0% | 42.0% | **54.3%** | 0.420 | 99.0% (BR: 99.1%) | 14470 |
| PRIVATE BUS | GLM-Ensemble | 20 | 25.0% | 25.0% | **36.8%** | 0.250 | 97.5% (BR: 98.3%) | 731 |
| PRIVATE BUS | XGBoost | 20 | 11.7% | 11.7% | **34.7%** | 0.117 | 99.4% (BR: 99.7%) | 731 |
| PRIVATE BUS | GLM-Ensemble | 50 | 22.0% | 22.0% | **36.8%** | 0.220 | 93.5% (BR: 95.9%) | 731 |
| PRIVATE BUS | XGBoost | 50 | 11.3% | 11.3% | **34.7%** | 0.113 | 98.5% (BR: 99.1%) | 731 |
| SCHOOL VEHICLE | GLM-Ensemble | 20 | 3.3% | 3.3% | **19.3%** | 0.033 | 96.8% (BR: 98.3%) | 154 |
| SCHOOL VEHICLE | XGBoost | 20 | 1.7% | 1.7% | **12.1%** | 0.017 | 99.3% (BR: 99.7%) | 154 |
| SCHOOL VEHICLE | GLM-Ensemble | 50 | 4.0% | 6.2% | **19.3%** | 0.048 | 93.6% (BR: 95.9%) | 154 |
| SCHOOL VEHICLE | XGBoost | 50 | 0.7% | 1.2% | **12.1%** | 0.009 | 98.4% (BR: 99.1%) | 154 |
| SCOOTER | GLM-Ensemble | 20 | 78.3% | 78.3% | **66.4%** | 0.783 | 99.3% (BR: 98.3%) | 30518 |
| SCOOTER | XGBoost | 20 | 51.7% | 51.7% | **56.2%** | 0.517 | 99.7% (BR: 99.7%) | 30518 |
| SCOOTER | GLM-Ensemble | 50 | 72.7% | 72.7% | **66.4%** | 0.727 | 97.8% (BR: 95.9%) | 30518 |
| SCOOTER | XGBoost | 50 | 58.7% | 58.7% | **56.2%** | 0.587 | 99.3% (BR: 99.1%) | 30518 |
| TANKER | GLM-Ensemble | 20 | 3.3% | 3.3% | **7.9%** | 0.033 | 96.8% (BR: 98.3%) | 110 |
| TANKER | XGBoost | 20 | 0.0% | 0.0% | **23.5%** | 0.000 | 99.3% (BR: 99.7%) | 110 |
| TANKER | GLM-Ensemble | 50 | 12.0% | 20.2% | **7.9%** | 0.150 | 94.4% (BR: 95.9%) | 110 |
| TANKER | XGBoost | 50 | 2.0% | 2.9% | **23.5%** | 0.024 | 98.6% (BR: 99.1%) | 110 |
| TEMPO | GLM-Ensemble | 20 | 21.7% | 21.7% | **29.9%** | 0.217 | 97.4% (BR: 98.3%) | 551 |
| TEMPO | XGBoost | 20 | 8.3% | 8.3% | **25.2%** | 0.083 | 99.4% (BR: 99.7%) | 551 |
| TEMPO | GLM-Ensemble | 50 | 22.0% | 22.0% | **29.9%** | 0.220 | 93.6% (BR: 95.9%) | 551 |
| TEMPO | XGBoost | 50 | 9.3% | 9.3% | **25.2%** | 0.093 | 98.4% (BR: 99.1%) | 551 |
| TOURIST BUS | GLM-Ensemble | 20 | 16.7% | 16.7% | **25.2%** | 0.167 | 97.2% (BR: 98.3%) | 160 |
| TOURIST BUS | XGBoost | 20 | 0.0% | 0.0% | **20.6%** | 0.000 | 99.3% (BR: 99.7%) | 160 |
| TOURIST BUS | GLM-Ensemble | 50 | 19.3% | 30.8% | **25.2%** | 0.237 | 94.9% (BR: 95.9%) | 160 |
| TOURIST BUS | XGBoost | 50 | 6.7% | 8.3% | **20.6%** | 0.074 | 98.6% (BR: 99.1%) | 160 |
| TRACTOR | GLM-Ensemble | 20 | 3.3% | 8.3% | **23.4%** | 0.048 | 97.6% (BR: 98.3%) | 32 |
| TRACTOR | XGBoost | 20 | 1.7% | 2.4% | **24.7%** | 0.020 | 99.5% (BR: 99.7%) | 32 |
| TRACTOR | GLM-Ensemble | 50 | 6.0% | 32.7% | **23.4%** | 0.101 | 95.5% (BR: 95.9%) | 32 |
| TRACTOR | XGBoost | 50 | 2.7% | 14.0% | **24.7%** | 0.045 | 99.0% (BR: 99.1%) | 32 |
| VAN | GLM-Ensemble | 20 | 51.7% | 51.7% | **38.8%** | 0.517 | 98.4% (BR: 98.3%) | 581 |
| VAN | XGBoost | 20 | 20.0% | 20.0% | **29.8%** | 0.200 | 99.4% (BR: 99.7%) | 581 |
| VAN | GLM-Ensemble | 50 | 35.3% | 35.3% | **38.8%** | 0.353 | 94.7% (BR: 95.9%) | 581 |
| VAN | XGBoost | 50 | 14.0% | 14.0% | **29.8%** | 0.140 | 98.5% (BR: 99.1%) | 581 |

## By Police Station

| Subgroup | Model | Global K | Precision | Global Recall | Within-Group Recall (Top 20%) | F1 Score | Accuracy (vs Base Rate) | n (test) |
|---|---|---|---|---|---|---|---|---|
| Adugodi | GLM-Ensemble | 20 | 0.0% | 0.0% | **38.9%** | 0.000 | 96.7% (BR: 98.3%) | 1286 |
| Adugodi | XGBoost | 20 | 0.0% | 0.0% | **54.9%** | 0.000 | 99.3% (BR: 99.7%) | 1286 |
| Adugodi | GLM-Ensemble | 50 | 2.0% | 4.0% | **38.9%** | 0.027 | 93.9% (BR: 95.9%) | 1286 |
| Adugodi | XGBoost | 50 | 0.0% | 0.0% | **54.9%** | 0.000 | 98.3% (BR: 99.1%) | 1286 |
| Ashok Nagar | GLM-Ensemble | 20 | 0.0% | 0.0% | **50.0%** | 0.000 | 96.8% (BR: 98.3%) | 1003 |
| Ashok Nagar | XGBoost | 20 | 0.0% | 0.0% | **55.9%** | 0.000 | 99.3% (BR: 99.7%) | 1003 |
| Ashok Nagar | GLM-Ensemble | 50 | 2.7% | 6.7% | **50.0%** | 0.038 | 94.5% (BR: 95.9%) | 1003 |
| Ashok Nagar | XGBoost | 50 | 0.0% | 0.0% | **55.9%** | 0.000 | 98.3% (BR: 99.1%) | 1003 |
| Banashankari | GLM-Ensemble | 20 | 0.0% | 0.0% | **71.9%** | 0.000 | 96.9% (BR: 98.3%) | 273 |
| Banashankari | XGBoost | 20 | 0.0% | 0.0% | **41.7%** | 0.000 | 99.3% (BR: 99.7%) | 273 |
| Banashankari | GLM-Ensemble | 50 | 0.0% | 0.0% | **71.9%** | 0.000 | 94.3% (BR: 95.9%) | 273 |
| Banashankari | XGBoost | 50 | 0.0% | 0.0% | **41.7%** | 0.000 | 98.6% (BR: 99.1%) | 273 |
| Banaswadi | GLM-Ensemble | 20 | 0.0% | 0.0% | **59.4%** | 0.000 | 96.7% (BR: 98.3%) | 1629 |
| Banaswadi | XGBoost | 20 | 0.0% | 0.0% | **57.7%** | 0.000 | 99.3% (BR: 99.7%) | 1629 |
| Banaswadi | GLM-Ensemble | 50 | 4.7% | 5.9% | **59.4%** | 0.052 | 92.9% (BR: 95.9%) | 1629 |
| Banaswadi | XGBoost | 50 | 1.3% | 1.3% | **57.7%** | 0.013 | 98.3% (BR: 99.1%) | 1629 |
| Basavanagudi | GLM-Ensemble | 20 | 0.0% | 0.0% | **80.0%** | 0.000 | 96.8% (BR: 98.3%) | 1525 |
| Basavanagudi | XGBoost | 20 | 0.0% | 0.0% | **66.7%** | 0.000 | 99.3% (BR: 99.7%) | 1525 |
| Basavanagudi | GLM-Ensemble | 50 | 2.0% | 5.4% | **80.0%** | 0.029 | 94.5% (BR: 95.9%) | 1525 |
| Basavanagudi | XGBoost | 50 | 1.3% | 1.3% | **66.7%** | 0.013 | 98.3% (BR: 99.1%) | 1525 |
| Bellandur | GLM-Ensemble | 20 | 0.0% | 0.0% | **68.5%** | 0.000 | 96.7% (BR: 98.3%) | 2211 |
| Bellandur | XGBoost | 20 | 0.0% | 0.0% | **59.4%** | 0.000 | 99.3% (BR: 99.7%) | 2211 |
| Bellandur | GLM-Ensemble | 50 | 0.0% | 0.0% | **68.5%** | 0.000 | 93.4% (BR: 95.9%) | 2211 |
| Bellandur | XGBoost | 50 | 0.0% | 0.0% | **59.4%** | 0.000 | 98.3% (BR: 99.1%) | 2211 |
| Byatarayanapura | GLM-Ensemble | 20 | 0.0% | 0.0% | **81.1%** | 0.000 | 96.7% (BR: 98.3%) | 1513 |
| Byatarayanapura | XGBoost | 20 | 0.0% | 0.0% | **66.5%** | 0.000 | 99.3% (BR: 99.7%) | 1513 |
| Byatarayanapura | GLM-Ensemble | 50 | 0.0% | 0.0% | **81.1%** | 0.000 | 94.0% (BR: 95.9%) | 1513 |
| Byatarayanapura | XGBoost | 50 | 0.0% | 0.0% | **66.5%** | 0.000 | 98.3% (BR: 99.1%) | 1513 |
| Chamarajpet | GLM-Ensemble | 20 | 10.0% | 15.8% | **73.3%** | 0.122 | 97.6% (BR: 98.3%) | 1550 |
| Chamarajpet | XGBoost | 20 | 0.0% | 0.0% | **58.6%** | 0.000 | 99.3% (BR: 99.7%) | 1550 |
| Chamarajpet | GLM-Ensemble | 50 | 6.0% | 23.7% | **73.3%** | 0.096 | 95.3% (BR: 95.9%) | 1550 |
| Chamarajpet | XGBoost | 50 | 2.7% | 3.2% | **58.6%** | 0.029 | 98.4% (BR: 99.1%) | 1550 |
| Chikkabanavara | GLM-Ensemble | 20 | 0.0% | 0.0% | **60.0%** | 0.000 | 97.2% (BR: 98.3%) | 313 |
| Chikkabanavara | XGBoost | 20 | 0.0% | 0.0% | **55.2%** | 0.000 | 99.3% (BR: 99.7%) | 313 |
| Chikkabanavara | GLM-Ensemble | 50 | 0.0% | 0.0% | **60.0%** | 0.000 | 94.8% (BR: 95.9%) | 313 |
| Chikkabanavara | XGBoost | 50 | 0.0% | 0.0% | **55.2%** | 0.000 | 98.6% (BR: 99.1%) | 313 |
| Chikkajala | GLM-Ensemble | 20 | 5.0% | 7.3% | **73.3%** | 0.059 | 97.4% (BR: 98.3%) | 2307 |
| Chikkajala | XGBoost | 20 | 3.3% | 3.3% | **79.4%** | 0.033 | 99.3% (BR: 99.7%) | 2307 |
| Chikkajala | GLM-Ensemble | 50 | 3.3% | 12.6% | **73.3%** | 0.052 | 95.0% (BR: 95.9%) | 2307 |
| Chikkajala | XGBoost | 50 | 2.7% | 2.9% | **79.4%** | 0.028 | 98.4% (BR: 99.1%) | 2307 |
| City Market | GLM-Ensemble | 20 | 25.0% | 40.6% | **60.0%** | 0.309 | 98.2% (BR: 98.3%) | 6704 |
| City Market | XGBoost | 20 | 15.0% | 15.0% | **73.2%** | 0.150 | 99.4% (BR: 99.7%) | 6704 |
| City Market | GLM-Ensemble | 50 | 14.7% | 59.4% | **60.0%** | 0.235 | 96.1% (BR: 95.9%) | 6704 |
| City Market | XGBoost | 50 | 11.3% | 11.3% | **73.2%** | 0.113 | 98.5% (BR: 99.1%) | 6704 |
| Cubbon Park | GLM-Ensemble | 20 | 1.7% | 1.9% | **20.0%** | 0.018 | 97.0% (BR: 98.3%) | 1001 |
| Cubbon Park | XGBoost | 20 | 0.0% | 0.0% | **47.4%** | 0.000 | 99.3% (BR: 99.7%) | 1001 |
| Cubbon Park | GLM-Ensemble | 50 | 6.0% | 18.2% | **20.0%** | 0.090 | 95.0% (BR: 95.9%) | 1001 |
| Cubbon Park | XGBoost | 50 | 0.0% | 0.0% | **47.4%** | 0.000 | 98.3% (BR: 99.1%) | 1001 |
| Devanahalli Airport | GLM-Ensemble | 20 | 1.7% | 1.7% | **68.9%** | 0.017 | 96.9% (BR: 98.3%) | 393 |
| Devanahalli Airport | XGBoost | 20 | 0.0% | 0.0% | **60.6%** | 0.000 | 99.3% (BR: 99.7%) | 393 |
| Devanahalli Airport | GLM-Ensemble | 50 | 0.7% | 1.6% | **68.9%** | 0.009 | 94.4% (BR: 95.9%) | 393 |
| Devanahalli Airport | XGBoost | 50 | 0.0% | 0.0% | **60.6%** | 0.000 | 98.4% (BR: 99.1%) | 393 |
| Electronic City | GLM-Ensemble | 20 | 0.0% | 0.0% | **59.5%** | 0.000 | 96.7% (BR: 98.3%) | 1588 |
| Electronic City | XGBoost | 20 | 0.0% | 0.0% | **54.1%** | 0.000 | 99.3% (BR: 99.7%) | 1588 |
| Electronic City | GLM-Ensemble | 50 | 0.7% | 0.8% | **59.5%** | 0.007 | 92.7% (BR: 95.9%) | 1588 |
| Electronic City | XGBoost | 50 | 0.7% | 0.7% | **54.1%** | 0.007 | 98.3% (BR: 99.1%) | 1588 |
| HAL Old Airport | GLM-Ensemble | 20 | 5.0% | 5.0% | **76.7%** | 0.050 | 96.9% (BR: 98.3%) | 8370 |
| HAL Old Airport | XGBoost | 20 | 8.3% | 8.3% | **77.7%** | 0.083 | 99.4% (BR: 99.7%) | 8370 |
| HAL Old Airport | GLM-Ensemble | 50 | 6.7% | 8.2% | **76.7%** | 0.074 | 93.0% (BR: 95.9%) | 8370 |
| HAL Old Airport | XGBoost | 50 | 6.0% | 6.0% | **77.7%** | 0.060 | 98.4% (BR: 99.1%) | 8370 |
| HSR Layout | GLM-Ensemble | 20 | 0.0% | 0.0% | **66.7%** | 0.000 | 96.7% (BR: 98.3%) | 1445 |
| HSR Layout | XGBoost | 20 | 0.0% | 0.0% | **59.2%** | 0.000 | 99.3% (BR: 99.7%) | 1445 |
| HSR Layout | GLM-Ensemble | 50 | 2.0% | 3.5% | **66.7%** | 0.025 | 93.6% (BR: 95.9%) | 1445 |
| HSR Layout | XGBoost | 50 | 0.0% | 0.0% | **59.2%** | 0.000 | 98.3% (BR: 99.1%) | 1445 |
| Halasur | GLM-Ensemble | 20 | 0.0% | 0.0% | **73.3%** | 0.000 | 97.2% (BR: 98.3%) | 1490 |
| Halasur | XGBoost | 20 | 0.0% | 0.0% | **64.8%** | 0.000 | 99.3% (BR: 99.7%) | 1490 |
| Halasur | GLM-Ensemble | 50 | 2.7% | 10.0% | **73.3%** | 0.042 | 94.9% (BR: 95.9%) | 1490 |
| Halasur | XGBoost | 50 | 0.0% | 0.0% | **64.8%** | 0.000 | 98.3% (BR: 99.1%) | 1490 |
| Halasuru Gate | GLM-Ensemble | 20 | 15.0% | 23.1% | **80.0%** | 0.182 | 97.8% (BR: 98.3%) | 2420 |
| Halasuru Gate | XGBoost | 20 | 0.0% | 0.0% | **58.3%** | 0.000 | 99.3% (BR: 99.7%) | 2420 |
| Halasuru Gate | GLM-Ensemble | 50 | 6.7% | 25.6% | **80.0%** | 0.106 | 95.3% (BR: 95.9%) | 2420 |
| Halasuru Gate | XGBoost | 50 | 3.3% | 3.3% | **58.3%** | 0.033 | 98.3% (BR: 99.1%) | 2420 |
| Hebbala | GLM-Ensemble | 20 | 5.0% | 12.3% | **80.0%** | 0.068 | 97.7% (BR: 98.3%) | 1215 |
| Hebbala | XGBoost | 20 | 5.0% | 5.2% | **62.1%** | 0.051 | 99.4% (BR: 99.7%) | 1215 |
| Hebbala | GLM-Ensemble | 50 | 2.0% | 12.3% | **80.0%** | 0.034 | 95.2% (BR: 95.9%) | 1215 |
| Hebbala | XGBoost | 50 | 2.7% | 5.3% | **62.1%** | 0.035 | 98.8% (BR: 99.1%) | 1215 |
| Hennuru | GLM-Ensemble | 20 | 0.0% | 0.0% | **35.1%** | 0.000 | 97.0% (BR: 98.3%) | 142 |
| Hennuru | XGBoost | 20 | 0.0% | 0.0% | **20.9%** | 0.000 | 99.3% (BR: 99.7%) | 142 |
| Hennuru | GLM-Ensemble | 50 | 0.0% | 0.0% | **35.1%** | 0.000 | 94.4% (BR: 95.9%) | 142 |
| Hennuru | XGBoost | 50 | 0.0% | 0.0% | **20.9%** | 0.000 | 98.7% (BR: 99.1%) | 142 |
| High ground | GLM-Ensemble | 20 | 11.7% | 15.2% | **60.0%** | 0.131 | 97.5% (BR: 98.3%) | 1261 |
| High ground | XGBoost | 20 | 0.0% | 0.0% | **67.0%** | 0.000 | 99.3% (BR: 99.7%) | 1261 |
| High ground | GLM-Ensemble | 50 | 7.3% | 24.3% | **60.0%** | 0.112 | 95.2% (BR: 95.9%) | 1261 |
| High ground | XGBoost | 50 | 2.0% | 2.0% | **67.0%** | 0.020 | 98.3% (BR: 99.1%) | 1261 |
| Hulimavu | GLM-Ensemble | 20 | 0.0% | 0.0% | **78.0%** | 0.000 | 96.7% (BR: 98.3%) | 964 |
| Hulimavu | XGBoost | 20 | 0.0% | 0.0% | **69.9%** | 0.000 | 99.3% (BR: 99.7%) | 964 |
| Hulimavu | GLM-Ensemble | 50 | 0.0% | 0.0% | **78.0%** | 0.000 | 93.7% (BR: 95.9%) | 964 |
| Hulimavu | XGBoost | 50 | 0.0% | 0.0% | **69.9%** | 0.000 | 98.3% (BR: 99.1%) | 964 |
| J.P. Nagar | GLM-Ensemble | 20 | 0.0% | 0.0% | **34.9%** | 0.000 | 96.7% (BR: 98.3%) | 605 |
| J.P. Nagar | XGBoost | 20 | 0.0% | 0.0% | **43.4%** | 0.000 | 99.3% (BR: 99.7%) | 605 |
| J.P. Nagar | GLM-Ensemble | 50 | 0.0% | 0.0% | **34.9%** | 0.000 | 93.8% (BR: 95.9%) | 605 |
| J.P. Nagar | XGBoost | 50 | 0.0% | 0.0% | **43.4%** | 0.000 | 98.3% (BR: 99.1%) | 605 |
| Jalahalli | GLM-Ensemble | 20 | 0.0% | 0.0% | **66.7%** | 0.000 | 96.8% (BR: 98.3%) | 461 |
| Jalahalli | XGBoost | 20 | 0.0% | 0.0% | **62.5%** | 0.000 | 99.3% (BR: 99.7%) | 461 |
| Jalahalli | GLM-Ensemble | 50 | 0.0% | 0.0% | **66.7%** | 0.000 | 94.3% (BR: 95.9%) | 461 |
| Jalahalli | XGBoost | 50 | 0.0% | 0.0% | **62.5%** | 0.000 | 98.4% (BR: 99.1%) | 461 |
| Jayanagara | GLM-Ensemble | 20 | 0.0% | 0.0% | **93.3%** | 0.000 | 96.7% (BR: 98.3%) | 1250 |
| Jayanagara | XGBoost | 20 | 0.0% | 0.0% | **70.6%** | 0.000 | 99.3% (BR: 99.7%) | 1250 |
| Jayanagara | GLM-Ensemble | 50 | 1.3% | 3.5% | **93.3%** | 0.019 | 94.4% (BR: 95.9%) | 1250 |
| Jayanagara | XGBoost | 50 | 0.0% | 0.0% | **70.6%** | 0.000 | 98.3% (BR: 99.1%) | 1250 |
| Jeevanbheemanagar | GLM-Ensemble | 20 | 0.0% | 0.0% | **95.2%** | 0.000 | 96.7% (BR: 98.3%) | 2598 |
| Jeevanbheemanagar | XGBoost | 20 | 1.7% | 1.7% | **65.4%** | 0.017 | 99.3% (BR: 99.7%) | 2598 |
| Jeevanbheemanagar | GLM-Ensemble | 50 | 2.0% | 3.3% | **95.2%** | 0.025 | 93.6% (BR: 95.9%) | 2598 |
| Jeevanbheemanagar | XGBoost | 50 | 1.3% | 1.3% | **65.4%** | 0.013 | 98.3% (BR: 99.1%) | 2598 |
| Jnanabharathi | GLM-Ensemble | 20 | 0.0% | 0.0% | **61.9%** | 0.000 | 96.8% (BR: 98.3%) | 458 |
| Jnanabharathi | XGBoost | 20 | 0.0% | 0.0% | **42.2%** | 0.000 | 99.3% (BR: 99.7%) | 458 |
| Jnanabharathi | GLM-Ensemble | 50 | 0.0% | 0.0% | **61.9%** | 0.000 | 94.2% (BR: 95.9%) | 458 |
| Jnanabharathi | XGBoost | 50 | 0.0% | 0.0% | **42.2%** | 0.000 | 98.4% (BR: 99.1%) | 458 |
| K.G. Halli | GLM-Ensemble | 20 | 0.0% | 0.0% | **53.3%** | 0.000 | 97.0% (BR: 98.3%) | 321 |
| K.G. Halli | XGBoost | 20 | 0.0% | 0.0% | **46.3%** | 0.000 | 99.3% (BR: 99.7%) | 321 |
| K.G. Halli | GLM-Ensemble | 50 | 0.0% | 0.0% | **53.3%** | 0.000 | 94.5% (BR: 95.9%) | 321 |
| K.G. Halli | XGBoost | 50 | 0.0% | 0.0% | **46.3%** | 0.000 | 98.5% (BR: 99.1%) | 321 |
| K.R. Pura | GLM-Ensemble | 20 | 5.0% | 5.0% | **58.9%** | 0.050 | 96.9% (BR: 98.3%) | 2527 |
| K.R. Pura | XGBoost | 20 | 3.3% | 3.3% | **61.8%** | 0.033 | 99.3% (BR: 99.7%) | 2527 |
| K.R. Pura | GLM-Ensemble | 50 | 6.0% | 10.6% | **58.9%** | 0.076 | 94.0% (BR: 95.9%) | 2527 |
| K.R. Pura | XGBoost | 50 | 3.3% | 3.3% | **61.8%** | 0.033 | 98.3% (BR: 99.1%) | 2527 |
| K.S. Layout | GLM-Ensemble | 20 | 0.0% | 0.0% | **75.6%** | 0.000 | 96.8% (BR: 98.3%) | 359 |
| K.S. Layout | XGBoost | 20 | 0.0% | 0.0% | **49.3%** | 0.000 | 99.3% (BR: 99.7%) | 359 |
| K.S. Layout | GLM-Ensemble | 50 | 0.0% | 0.0% | **75.6%** | 0.000 | 94.1% (BR: 95.9%) | 359 |
| K.S. Layout | XGBoost | 50 | 0.0% | 0.0% | **49.3%** | 0.000 | 98.4% (BR: 99.1%) | 359 |
| Kamakshipalya | GLM-Ensemble | 20 | 0.0% | 0.0% | **68.3%** | 0.000 | 96.8% (BR: 98.3%) | 542 |
| Kamakshipalya | XGBoost | 20 | 0.0% | 0.0% | **63.3%** | 0.000 | 99.3% (BR: 99.7%) | 542 |
| Kamakshipalya | GLM-Ensemble | 50 | 0.0% | 0.0% | **68.3%** | 0.000 | 94.4% (BR: 95.9%) | 542 |
| Kamakshipalya | XGBoost | 50 | 0.0% | 0.0% | **63.3%** | 0.000 | 98.4% (BR: 99.1%) | 542 |
| Kengeri | GLM-Ensemble | 20 | 0.0% | 0.0% | **63.3%** | 0.000 | 97.0% (BR: 98.3%) | 187 |
| Kengeri | XGBoost | 20 | 0.0% | 0.0% | **45.8%** | 0.000 | 99.3% (BR: 99.7%) | 187 |
| Kengeri | GLM-Ensemble | 50 | 0.0% | 0.0% | **63.3%** | 0.000 | 94.5% (BR: 95.9%) | 187 |
| Kengeri | XGBoost | 50 | 0.0% | 0.0% | **45.8%** | 0.000 | 98.7% (BR: 99.1%) | 187 |
| Kodigehalli | GLM-Ensemble | 20 | 8.3% | 8.3% | **65.6%** | 0.083 | 97.0% (BR: 98.3%) | 3625 |
| Kodigehalli | XGBoost | 20 | 10.0% | 10.0% | **68.1%** | 0.100 | 99.4% (BR: 99.7%) | 3625 |
| Kodigehalli | GLM-Ensemble | 50 | 4.0% | 4.8% | **65.6%** | 0.044 | 92.8% (BR: 95.9%) | 3625 |
| Kodigehalli | XGBoost | 50 | 4.7% | 4.7% | **68.1%** | 0.047 | 98.4% (BR: 99.1%) | 3625 |
| Madiwala | GLM-Ensemble | 20 | 0.0% | 0.0% | **36.7%** | 0.000 | 96.7% (BR: 98.3%) | 697 |
| Madiwala | XGBoost | 20 | 0.0% | 0.0% | **41.6%** | 0.000 | 99.3% (BR: 99.7%) | 697 |
| Madiwala | GLM-Ensemble | 50 | 1.3% | 3.1% | **36.7%** | 0.019 | 94.2% (BR: 95.9%) | 697 |
| Madiwala | XGBoost | 50 | 0.0% | 0.0% | **41.6%** | 0.000 | 98.3% (BR: 99.1%) | 697 |
| Magadi Road | GLM-Ensemble | 20 | 1.7% | 1.7% | **57.8%** | 0.017 | 96.7% (BR: 98.3%) | 3078 |
| Magadi Road | XGBoost | 20 | 0.0% | 0.0% | **64.9%** | 0.000 | 99.3% (BR: 99.7%) | 3078 |
| Magadi Road | GLM-Ensemble | 50 | 6.7% | 12.5% | **57.8%** | 0.087 | 94.2% (BR: 95.9%) | 3078 |
| Magadi Road | XGBoost | 50 | 1.3% | 1.3% | **64.9%** | 0.013 | 98.3% (BR: 99.1%) | 3078 |
| Mahadevapura | GLM-Ensemble | 20 | 0.0% | 0.0% | **64.0%** | 0.000 | 96.7% (BR: 98.3%) | 2584 |
| Mahadevapura | XGBoost | 20 | 0.0% | 0.0% | **54.6%** | 0.000 | 99.3% (BR: 99.7%) | 2584 |
| Mahadevapura | GLM-Ensemble | 50 | 5.3% | 6.3% | **64.0%** | 0.058 | 92.8% (BR: 95.9%) | 2584 |
| Mahadevapura | XGBoost | 50 | 1.3% | 1.3% | **54.6%** | 0.013 | 98.3% (BR: 99.1%) | 2584 |
| Malleshwaram | GLM-Ensemble | 20 | 13.3% | 13.9% | **80.0%** | 0.136 | 97.2% (BR: 98.3%) | 7964 |
| Malleshwaram | XGBoost | 20 | 6.7% | 6.7% | **77.4%** | 0.067 | 99.4% (BR: 99.7%) | 7964 |
| Malleshwaram | GLM-Ensemble | 50 | 15.3% | 39.3% | **80.0%** | 0.220 | 95.5% (BR: 95.9%) | 7964 |
| Malleshwaram | XGBoost | 50 | 8.7% | 8.7% | **77.4%** | 0.087 | 98.4% (BR: 99.1%) | 7964 |
| Mico Layout | GLM-Ensemble | 20 | 0.0% | 0.0% | **47.8%** | 0.000 | 96.7% (BR: 98.3%) | 792 |
| Mico Layout | XGBoost | 20 | 0.0% | 0.0% | **56.9%** | 0.000 | 99.3% (BR: 99.7%) | 792 |
| Mico Layout | GLM-Ensemble | 50 | 0.0% | 0.0% | **47.8%** | 0.000 | 94.2% (BR: 95.9%) | 792 |
| Mico Layout | XGBoost | 50 | 0.0% | 0.0% | **56.9%** | 0.000 | 98.3% (BR: 99.1%) | 792 |
| No Police Station | GLM-Ensemble | 20 | 1.7% | 1.9% | **26.7%** | 0.018 | 97.2% (BR: 98.3%) | 136 |
| No Police Station | XGBoost | 20 | 0.0% | 0.0% | **40.8%** | 0.000 | 99.3% (BR: 99.7%) | 136 |
| No Police Station | GLM-Ensemble | 50 | 1.3% | 3.7% | **26.7%** | 0.020 | 94.7% (BR: 95.9%) | 136 |
| No Police Station | XGBoost | 50 | 1.3% | 2.8% | **40.8%** | 0.018 | 98.7% (BR: 99.1%) | 136 |
| Peenya | GLM-Ensemble | 20 | 0.0% | 0.0% | **53.3%** | 0.000 | 97.1% (BR: 98.3%) | 352 |
| Peenya | XGBoost | 20 | 0.0% | 0.0% | **44.9%** | 0.000 | 99.3% (BR: 99.7%) | 352 |
| Peenya | GLM-Ensemble | 50 | 0.0% | 0.0% | **53.3%** | 0.000 | 94.6% (BR: 95.9%) | 352 |
| Peenya | XGBoost | 50 | 0.0% | 0.0% | **44.9%** | 0.000 | 98.5% (BR: 99.1%) | 352 |
| Pulikeshinagar(F.Town) | GLM-Ensemble | 20 | 0.0% | 0.0% | **66.7%** | 0.000 | 96.9% (BR: 98.3%) | 1465 |
| Pulikeshinagar(F.Town) | XGBoost | 20 | 0.0% | 0.0% | **59.0%** | 0.000 | 99.3% (BR: 99.7%) | 1465 |
| Pulikeshinagar(F.Town) | GLM-Ensemble | 50 | 2.7% | 7.2% | **66.7%** | 0.039 | 94.6% (BR: 95.9%) | 1465 |
| Pulikeshinagar(F.Town) | XGBoost | 50 | 0.0% | 0.0% | **59.0%** | 0.000 | 98.3% (BR: 99.1%) | 1465 |
| R.T. Nagar | GLM-Ensemble | 20 | 0.0% | 0.0% | **46.7%** | 0.000 | 96.9% (BR: 98.3%) | 488 |
| R.T. Nagar | XGBoost | 20 | 0.0% | 0.0% | **43.3%** | 0.000 | 99.3% (BR: 99.7%) | 488 |
| R.T. Nagar | GLM-Ensemble | 50 | 0.0% | 0.0% | **46.7%** | 0.000 | 94.3% (BR: 95.9%) | 488 |
| R.T. Nagar | XGBoost | 50 | 0.0% | 0.0% | **43.3%** | 0.000 | 98.5% (BR: 99.1%) | 488 |
| Rajajinagar | GLM-Ensemble | 20 | 5.0% | 5.0% | **66.7%** | 0.050 | 96.9% (BR: 98.3%) | 3285 |
| Rajajinagar | XGBoost | 20 | 3.3% | 3.3% | **58.6%** | 0.033 | 99.3% (BR: 99.7%) | 3285 |
| Rajajinagar | GLM-Ensemble | 50 | 7.3% | 11.3% | **66.7%** | 0.089 | 93.8% (BR: 95.9%) | 3285 |
| Rajajinagar | XGBoost | 50 | 4.0% | 4.0% | **58.6%** | 0.040 | 98.3% (BR: 99.1%) | 3285 |
| Sadashivanagar | GLM-Ensemble | 20 | 1.7% | 1.7% | **38.7%** | 0.017 | 97.0% (BR: 98.3%) | 587 |
| Sadashivanagar | XGBoost | 20 | 0.0% | 0.0% | **59.0%** | 0.000 | 99.3% (BR: 99.7%) | 587 |
| Sadashivanagar | GLM-Ensemble | 50 | 2.0% | 3.7% | **38.7%** | 0.026 | 94.5% (BR: 95.9%) | 587 |
| Sadashivanagar | XGBoost | 50 | 0.0% | 0.0% | **59.0%** | 0.000 | 98.5% (BR: 99.1%) | 587 |
| Sheshadripuram | GLM-Ensemble | 20 | 5.0% | 5.8% | **46.7%** | 0.054 | 97.1% (BR: 98.3%) | 1250 |
| Sheshadripuram | XGBoost | 20 | 0.0% | 0.0% | **57.9%** | 0.000 | 99.3% (BR: 99.7%) | 1250 |
| Sheshadripuram | GLM-Ensemble | 50 | 4.0% | 11.5% | **46.7%** | 0.059 | 94.8% (BR: 95.9%) | 1250 |
| Sheshadripuram | XGBoost | 50 | 0.0% | 0.0% | **57.9%** | 0.000 | 98.3% (BR: 99.1%) | 1250 |
| Shivajinagar | GLM-Ensemble | 20 | 15.0% | 26.5% | **93.3%** | 0.192 | 97.9% (BR: 98.3%) | 9506 |
| Shivajinagar | XGBoost | 20 | 13.3% | 13.3% | **92.5%** | 0.133 | 99.4% (BR: 99.7%) | 9506 |
| Shivajinagar | GLM-Ensemble | 50 | 10.0% | 43.9% | **93.3%** | 0.163 | 95.7% (BR: 95.9%) | 9506 |
| Shivajinagar | XGBoost | 50 | 12.7% | 12.7% | **92.5%** | 0.127 | 98.5% (BR: 99.1%) | 9506 |
| Thalagattapura | GLM-Ensemble | 20 | 0.0% | 0.0% | **61.9%** | 0.000 | 96.7% (BR: 98.3%) | 338 |
| Thalagattapura | XGBoost | 20 | 0.0% | 0.0% | **39.0%** | 0.000 | 99.3% (BR: 99.7%) | 338 |
| Thalagattapura | GLM-Ensemble | 50 | 0.0% | 0.0% | **61.9%** | 0.000 | 94.1% (BR: 95.9%) | 338 |
| Thalagattapura | XGBoost | 50 | 0.0% | 0.0% | **39.0%** | 0.000 | 98.3% (BR: 99.1%) | 338 |
| Upparpet | GLM-Ensemble | 20 | 21.7% | 50.0% | **80.0%** | 0.302 | 98.3% (BR: 98.3%) | 12446 |
| Upparpet | XGBoost | 20 | 36.7% | 36.7% | **88.3%** | 0.367 | 99.6% (BR: 99.7%) | 12446 |
| Upparpet | GLM-Ensemble | 50 | 10.7% | 61.7% | **80.0%** | 0.182 | 96.0% (BR: 95.9%) | 12446 |
| Upparpet | XGBoost | 50 | 33.3% | 33.3% | **88.3%** | 0.333 | 98.9% (BR: 99.1%) | 12446 |
| V.V.Puram (C.Pet) | GLM-Ensemble | 20 | 5.0% | 10.1% | **53.3%** | 0.067 | 97.7% (BR: 98.3%) | 777 |
| V.V.Puram (C.Pet) | XGBoost | 20 | 5.0% | 5.0% | **43.6%** | 0.050 | 99.3% (BR: 99.7%) | 777 |
| V.V.Puram (C.Pet) | GLM-Ensemble | 50 | 4.0% | 20.1% | **53.3%** | 0.067 | 95.4% (BR: 95.9%) | 777 |
| V.V.Puram (C.Pet) | XGBoost | 50 | 2.0% | 2.5% | **43.6%** | 0.022 | 98.5% (BR: 99.1%) | 777 |
| Vijayanagara | GLM-Ensemble | 20 | 11.7% | 11.7% | **66.7%** | 0.117 | 97.1% (BR: 98.3%) | 4523 |
| Vijayanagara | XGBoost | 20 | 1.7% | 1.7% | **67.5%** | 0.017 | 99.3% (BR: 99.7%) | 4523 |
| Vijayanagara | GLM-Ensemble | 50 | 10.0% | 17.3% | **66.7%** | 0.127 | 94.3% (BR: 95.9%) | 4523 |
| Vijayanagara | XGBoost | 50 | 5.3% | 5.3% | **67.5%** | 0.053 | 98.4% (BR: 99.1%) | 4523 |
| Whitefield | GLM-Ensemble | 20 | 0.0% | 0.0% | **56.7%** | 0.000 | 96.7% (BR: 98.3%) | 1280 |
| Whitefield | XGBoost | 20 | 0.0% | 0.0% | **49.8%** | 0.000 | 99.3% (BR: 99.7%) | 1280 |
| Whitefield | GLM-Ensemble | 50 | 1.3% | 1.8% | **56.7%** | 0.015 | 92.8% (BR: 95.9%) | 1280 |
| Whitefield | XGBoost | 50 | 1.3% | 1.3% | **49.8%** | 0.013 | 98.3% (BR: 99.1%) | 1280 |
| Wilson Garden | GLM-Ensemble | 20 | 0.0% | 0.0% | **66.7%** | 0.000 | 96.8% (BR: 98.3%) | 1260 |
| Wilson Garden | XGBoost | 20 | 0.0% | 0.0% | **53.7%** | 0.000 | 99.3% (BR: 99.7%) | 1260 |
| Wilson Garden | GLM-Ensemble | 50 | 0.0% | 0.0% | **66.7%** | 0.000 | 94.2% (BR: 95.9%) | 1260 |
| Wilson Garden | XGBoost | 50 | 0.0% | 0.0% | **53.7%** | 0.000 | 98.3% (BR: 99.1%) | 1260 |
| Yelahanka | GLM-Ensemble | 20 | 0.0% | 0.0% | **51.8%** | 0.000 | 96.7% (BR: 98.3%) | 624 |
| Yelahanka | XGBoost | 20 | 0.0% | 0.0% | **44.9%** | 0.000 | 99.3% (BR: 99.7%) | 624 |
| Yelahanka | GLM-Ensemble | 50 | 0.0% | 0.0% | **51.8%** | 0.000 | 93.8% (BR: 95.9%) | 624 |
| Yelahanka | XGBoost | 50 | 0.0% | 0.0% | **44.9%** | 0.000 | 98.4% (BR: 99.1%) | 624 |
| Yeshwanthpura | GLM-Ensemble | 20 | 0.0% | 0.0% | **50.0%** | 0.000 | 96.7% (BR: 98.3%) | 975 |
| Yeshwanthpura | XGBoost | 20 | 0.0% | 0.0% | **52.4%** | 0.000 | 99.3% (BR: 99.7%) | 975 |
| Yeshwanthpura | GLM-Ensemble | 50 | 0.7% | 1.3% | **50.0%** | 0.009 | 94.0% (BR: 95.9%) | 975 |
| Yeshwanthpura | XGBoost | 50 | 0.0% | 0.0% | **52.4%** | 0.000 | 98.3% (BR: 99.1%) | 975 |