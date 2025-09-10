# Predicting Parking Lot Wait Time

This project is a simple program designed to **predict waiting times for selected parking lots in Taipei City**.  
It retrieves real-time parking availability data from the **Taipei City Government Open Data API**.  
Since actual vehicle entry/exit times are not available, the project uses **historical records of cumulative real-time available spaces** to build datasets, and then applies **confidence intervals** to estimate the distribution of waiting times.

---

##  Features
- Fetches parking lot availability data via the Taipei Open Data API
- Builds historical datasets for analysis
- Estimates waiting time ranges using **confidence interval statistics**

---

## ⚙ Language
- Python

---

##  Main Tools & Libraries
- [APScheduler](https://apscheduler.readthedocs.io/) — Task scheduling (periodic data collection)  
- [SciPy](https://scipy.org/) — Statistical analysis & confidence intervals  
- [PyMySQL](https://pymysql.readthedocs.io/) — MySQL database connection  

---
