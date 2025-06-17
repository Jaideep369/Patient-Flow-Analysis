-- SQL Script: hospital_patient_flow.sql

--Step 1: Calculate the length of stay for each patient*

--The length of stay can be calculated by subtracting the admission date from the discharge date.
SELECT 
    Patient_ID,
    Patient_Name,
    ward,
    admission_date,
    discharge_date,
    DATEDIFF(day, admission_date, discharge_date) AS length_of_stay
FROM 
    hospital.dbo.patients;

--Step 2: Calculate the average length of stay 

-- we average the length of stay for all patients.
SELECT 
    AVG(DATEDIFF(day, admission_date, discharge_date)) AS average_length_of_stay
FROM 
   hospital.dbo.patients;

--Step 3: Calculate total bed days used

--The total bed days used can be calculated by summing up the length of stay for all patients.
SELECT 
    SUM(DATEDIFF(day, admission_date, discharge_date)) AS total_bed_days_used
FROM 
   hospital.dbo.patients;

--step 4: Bed Utilization Rate
--The bed utilization rate is typically calculated as (Total bed days used / Total available bed days) * 100. However, since we don't have the total available bed days from the provided data, we'll focus on the calculations we can perform with the given information.
--Query for Bed Utilization Analysis*
SELECT 
    ward,
    AVG(DATEDIFF(day, admission_date, discharge_date)) AS average_length_of_stay,
    SUM(DATEDIFF(day, admission_date, discharge_date)) AS total_bed_days_used
FROM 
     hospital.dbo.patients
GROUP BY 
    ward;

-- Step 5: Daily Admissions
SELECT admission_date, COUNT(*) AS admission_count
FROM hospital.dbo.patients
GROUP BY admission_date;

--step 6:daily discharges
SELECT 
    discharge_date as date,
    COUNT(*) AS discharges
FROM  hospital.dbo.patients
GROUP BY discharge_date
ORDER BY discharge_date;

-- Step 7: Readmission Rate
--formula readmission rate=(number of readmissions/number of discharges)x1.0
SELECT 
  (SELECT COUNT(*) FROM   hospital.dbo.patients WHERE readmission_flag = 1) * 1.0 /
  (SELECT COUNT(*) FROM   hospital.dbo.patients WHERE discharge_date IS NOT NULL) AS readmission_rate;


