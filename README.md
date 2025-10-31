# Sicily Wind Analysis
This repository contains scripts and data for analyzing wind speeds over Sicily.
# 🌬️ Weather Exposure and Fragility Analysis

### 📘 Thesis Project – Energy Informatics & Power System Resilience

This repository contains the analytical workflow and scripts developed to study **the relationship between weather conditions (wind exposure)** and **failure fragility of power transmission infrastructure** across Sicily.

The project combines meteorological data, spatial tower locations, and historical failure records to model how environmental stressors impact the resilience of the transmission network.

---

## 🎯 Objectives

- Integrate multi-source datasets: **wind speed, direction, and tower attributes**
- Compute **exposure indices** based on spatial and temporal matching
- Develop **fragility models** for power line components
- Quantify **failure probabilities** under extreme weather conditions
- Support decision-making for **climate-resilient energy infrastructure**

---

## ⚙️ Methodology

1. **Data Collection**
   - Tower data from OpenStreetMap and Terna (voltage, height, material, circuits)
   - Wind data (U/V components) from MERIDA reanalysis datasets (2018–2022)
   - Historical failure data from Statnett/VAFFEL methodology

2. **Preprocessing**
   - Convert NetCDF weather data to GeoTIFF and Parquet formats
   - Spatially join tower coordinates with grid-based wind data (5×5 km)
   - Compute hourly wind exposure per tower

3. **Fragility Modelling**
   - Apply **Bayesian updating** based on historical failures
   - Estimate conditional probability of failure given weather intensity
   - Visualize exposure–failure relationships through regression and maps

---

## 📈 Key Results

- Developed a **data-driven fragility curve** linking wind intensity to failure probability  
- Mapped **vulnerability hotspots** across Sicilian transmission lines  
- Demonstrated integration between **meteorological analysis** and **power system reliability**

---

## 🧠 Tools & Technologies

- Python (Pandas, NumPy, Xarray, Geopandas, Matplotlib)
- QGIS / GeoPandas for spatial processing
- VAFFEL method for Bayesian failure rate updating
- PostgreSQL + PostGIS for spatial database management
- Parquet for large-scale time-series data storage



> “Understanding how weather exposure affects power system fragility is key to designing climate-resilient energy infrastructures.”  
This study bridges **data analytics**, **meteorology**, and **power system engineering** to support real-world decision-making in grid resilience.
