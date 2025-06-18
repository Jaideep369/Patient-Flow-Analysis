# Import required libraries
import pandas as pd  # pandas is used for data manipulation and analysis using dataframes
import matplotlib.pyplot as plt  # matplotlib is used for creating static plots
import seaborn as sns  # seaborn is used for statistical data visualization
import numpy as np  # numpy is used for numerical operations like mean, sum, etc.
from matplotlib.ticker import MaxNLocator, FuncFormatter  # used to format tick labels on axes (e.g., integers, percentages)
import plotly.express as px  # plotly.express is used for quick interactive visualizations
import plotly.graph_objects as go  # plotly.graph_objects is used for creating detailed interactive plots

# Load dataset from CSV file
data = pd.read_csv('/content/hospital_datas45.csv')  # load the CSV file into a pandas dataframe

# Convert admission and discharge columns to datetime objects for date calculations
data['admission_date'] = pd.to_datetime(data['admission_date'])  # convert admission date column to datetime format
data['discharge_date'] = pd.to_datetime(data['discharge_date'])  # convert discharge date column to datetime format

# Calculate patient's length of stay in days
data['length_of_stay'] = (data['discharge_date'] - data['admission_date']).dt.days  # compute stay duration

# -----------------------------
# AVERAGE LENGTH OF STAY BY WARD
# -----------------------------
avg_stay = data.groupby('ward')['length_of_stay'].mean().reset_index()  # calculate average length of stay grouped by ward

# Line Chart – Avg Length of Stay
fig_stay = px.line(avg_stay, x='ward', y='length_of_stay', title='Average Length of Stay by Ward (Interactive)',
                   labels={'ward': 'Ward', 'length_of_stay': 'Avg Stay (Days)'}, markers=True, template='plotly_white')
fig_stay.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Avg Stay</b>: %{y:.1f} days', line=dict(color='darkgreen'))
fig_stay.update_layout(xaxis_title='Ward', yaxis_title='Average Stay (Days)', hovermode='x unified')
fig_stay.show()

# Bar Chart – Avg Length of Stay
fig_bar_stay = px.bar(avg_stay, x='ward', y='length_of_stay', title='Average Stay Metrics by Ward (Bar)',
                      labels={'ward': 'Ward', 'length_of_stay': 'Avg Stay (Days)'}, template='plotly_white',
                      color='length_of_stay', color_continuous_scale='Blues')
fig_bar_stay.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Avg Stay</b>: %{y:.1f} days')
fig_bar_stay.update_layout(xaxis_title='Ward', yaxis_title='Average Stay (Days)')
fig_bar_stay.show()

# -----------------------------
# BED OCCUPANCY RATE BY WARD
# -----------------------------
data['bed_days_used'] = data['length_of_stay']
bed_occupancy = data.groupby('ward')['bed_days_used'].sum().reset_index()
total_beds = data['ward'].value_counts().max()
avg_los = data['length_of_stay'].mean()
bed_occupancy['bed_occupancy_rate'] = bed_occupancy['bed_days_used'] / (total_beds * avg_los)

# Line Chart – Bed Occupancy Rate
fig_occ = px.line(bed_occupancy, x='ward', y='bed_occupancy_rate',
                  title='Bed Occupancy Rate by Ward (Interactive)', labels={'ward': 'Ward', 'bed_occupancy_rate': 'Occupancy Rate'},
                  markers=True, template='plotly_white')
fig_occ.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Occupancy Rate</b>: %{y:.1%}', line=dict(color='purple'))
fig_occ.update_layout(xaxis_title='Ward', yaxis_title='Occupancy Rate (%)', hovermode='x unified', yaxis_tickformat='.0%')
fig_occ.show()

# Bar Chart – Bed Occupancy Rate
fig_bar_occ = px.bar(bed_occupancy, x='ward', y='bed_occupancy_rate',
                     title='Bed Utilization Rate by Ward (Bar)', labels={'ward': 'Ward', 'bed_occupancy_rate': 'Occupancy Rate'},
                     template='plotly_white', color='bed_occupancy_rate', color_continuous_scale='Oranges')
fig_bar_occ.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Occupancy Rate</b>: %{y:.1%}')
fig_bar_occ.update_layout(xaxis_title='Ward', yaxis_title='Occupancy Rate (%)', yaxis_tickformat='.0%')
fig_bar_occ.show()

# -----------------------------
# DAILY BED OCCUPANCY TRACKING
# -----------------------------
records = []
for _, row in data.iterrows():
    stay_dates = pd.date_range(start=row['admission_date'], end=row['discharge_date'])
    for date in stay_dates:
        records.append({'date': date, 'ward': row['ward']})
daily_df = pd.DataFrame(records)
daily_occupancy = daily_df.groupby('date').size().reset_index(name='occupied_beds')

fig_daily = px.line(daily_occupancy, x='date', y='occupied_beds',
                    title='Daily Bed Occupancy Over Time (Interactive)',
                    labels={'date': 'Date', 'occupied_beds': 'Number of Occupied Beds'},
                    markers=True, template='plotly_white')
fig_daily.update_traces(hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Occupied Beds</b>: %{y}', line=dict(color='red'))
fig_daily.update_layout(xaxis_title='Date', yaxis_title='Occupied Beds', hovermode='x unified')
fig_daily.show()

# -----------------------------
# ADDITIONAL VISUALS
# -----------------------------
# 1. Readmission Rate Pie Chart (dummy example assuming readmission column exists)
# Expecting the 'readmission' column to contain binary or categorical values such as 'Yes', 'No', 'Readmitted', etc.
if 'readmission' in data.columns:
    readmit_counts = data['readmission'].value_counts().reset_index()
    readmit_counts.columns = ['status', 'count']
    fig_pie = px.pie(readmit_counts, names='status', values='count', title='Readmission Rate Distribution', template='plotly_white')
    fig_pie.show()

# 2. Admission/Discharge Trend
admit_discharge = data.groupby('admission_date').size().reset_index(name='Admissions')
discharge_trend = data.groupby('discharge_date').size().reset_index(name='Discharges')

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=admit_discharge['admission_date'], y=admit_discharge['Admissions'],
                               mode='lines+markers', name='Admissions', line=dict(color='green')))
fig_trend.add_trace(go.Scatter(x=discharge_trend['discharge_date'], y=discharge_trend['Discharges'],
                               mode='lines+markers', name='Discharges', line=dict(color='orange')))
fig_trend.update_layout(title='Admission & Discharge Trends', xaxis_title='Date', yaxis_title='Count',
                        template='plotly_white', hovermode='x unified')
fig_trend.show()

# 3. Day-wise Admission Rates
data['admit_day'] = data['admission_date'].dt.day_name()
admit_by_day = data['admit_day'].value_counts().reset_index()
admit_by_day.columns = ['Day', 'Admissions']
fig_daywise = px.bar(admit_by_day, x='Day', y='Admissions', title='Day-wise Admission Rates',
                     template='plotly_white', color='Admissions', color_continuous_scale='Viridis')
fig_daywise.update_traces(hovertemplate='<b>Day</b>: %{x}<br><b>Admissions</b>: %{y}')
fig_daywise.show()

# 4. Ward-Level Congestion – Patient Count
ward_congestion = data['ward'].value_counts().reset_index()
ward_congestion.columns = ['Ward', 'Patients']
fig_congestion = px.bar(ward_congestion, x='Ward', y='Patients', title='Ward-Level Congestion (Patient Volume)',
                        template='plotly_white', color='Patients', color_continuous_scale='Reds')
fig_congestion.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Patients</b>: %{y}')
fig_congestion.show()

# 5. Patient Volume Trend
volume_trend = data.groupby('admission_date').size().reset_index(name='Admissions')
fig_volume = px.line(volume_trend, x='admission_date', y='Admissions', title='Patient Volume Trend Over Time',
                     labels={'admission_date': 'Date'}, template='plotly_white', markers=True)
fig_volume.update_traces(hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Admissions</b>: %{y}', line=dict(color='blue'))
fig_volume.update_layout(xaxis_title='Date', yaxis_title='Number of Admissions', hovermode='x unified')
fig_volume.show()
