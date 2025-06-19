# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MaxNLocator, FuncFormatter
import plotly.express as px
import plotly.graph_objects as go

# Load dataset from CSV file
data = pd.read_csv('/content/hospital_datas45.csv', on_bad_lines='skip')

# Convert date columns to datetime
data['admission_date'] = pd.to_datetime(data['admission_date'])
data['discharge_date'] = pd.to_datetime(data['discharge_date'])

# Calculate Length of Stay
data['length_of_stay'] = (data['discharge_date'] - data['admission_date']).dt.days

# -----------------------------
# AVERAGE LENGTH OF STAY BY WARD
# -----------------------------
avg_stay = data.groupby('ward')['length_of_stay'].mean().reset_index()

# Line Chart – Avg Length of Stay
fig_stay = px.line(avg_stay, x='ward', y='length_of_stay', title='Average Length of Stay by Ward (Interactive)',
                   labels={'ward': 'Ward', 'length_of_stay': 'Avg Stay (Days)'}, markers=True, template='plotly_white')
fig_stay.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Avg Stay</b>: %{y:.1f} days',
                       line=dict(color='darkgreen'),
                       mode='lines+markers+text',
                       text=avg_stay['length_of_stay'].round(1),
                       textposition='top center')
fig_stay.update_layout(xaxis_title='Ward', yaxis_title='Average Stay (Days)', hovermode='x unified')
fig_stay.show()

# Bar Chart – Avg Length of Stay
fig_bar_stay = px.bar(avg_stay, x='ward', y='length_of_stay', title='Average Stay Metrics by Ward (Bar)',
                      labels={'ward': 'Ward', 'length_of_stay': 'Avg Stay (Days)'}, template='plotly_white',
                      color='length_of_stay', color_continuous_scale='Blues')
fig_bar_stay.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Avg Stay</b>: %{y:.1f} days',
                           text=avg_stay['length_of_stay'].round(1),
                           textposition='outside')
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
                  title='Bed Occupancy Rate by Ward (Interactive)',
                  labels={'ward': 'Ward', 'bed_occupancy_rate': 'Occupancy Rate'},
                  markers=True, template='plotly_white')
fig_occ.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Occupancy Rate</b>: %{y:.1%}',
                      line=dict(color='purple'),
                      mode='lines+markers+text',
                      text=(bed_occupancy['bed_occupancy_rate'] * 100).round(1).astype(str) + '%',
                      textposition='top center')
fig_occ.update_layout(xaxis_title='Ward', yaxis_title='Occupancy Rate (%)', hovermode='x unified',
                      yaxis_tickformat='.0%')
fig_occ.show()

# Bar Chart – Bed Occupancy Rate
fig_bar_occ = px.bar(bed_occupancy, x='ward', y='bed_occupancy_rate',
                     title='Bed Utilization Rate by Ward (Bar)',
                     labels={'ward': 'Ward', 'bed_occupancy_rate': 'Occupancy Rate'},
                     template='plotly_white', color='bed_occupancy_rate',
                     color_continuous_scale='Oranges')
fig_bar_occ.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Occupancy Rate</b>: %{y:.1%}',
                          text=(bed_occupancy['bed_occupancy_rate'] * 100).round(1).astype(str) + '%',
                          textposition='outside')
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
fig_daily.update_traces(hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Occupied Beds</b>: %{y}',
                        line=dict(color='red'),
                        mode='lines+markers+text',
                        text=daily_occupancy['occupied_beds'],
                        textposition='top center')
fig_daily.update_layout(xaxis_title='Date', yaxis_title='Occupied Beds', hovermode='x unified')
fig_daily.show()

# -----------------------------
# ADDITIONAL CHARTS
# -----------------------------

# 1. Admission/Discharge Trend
admit_discharge = data.groupby('admission_date').size().reset_index(name='Admissions')
discharge_trend = data.groupby('discharge_date').size().reset_index(name='Discharges')

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=admit_discharge['admission_date'], y=admit_discharge['Admissions'],
                               mode='lines+markers+text', name='Admissions', line=dict(color='green'),
                               text=admit_discharge['Admissions'], textposition='top center'))
fig_trend.add_trace(go.Scatter(x=discharge_trend['discharge_date'], y=discharge_trend['Discharges'],
                               mode='lines+markers+text', name='Discharges', line=dict(color='orange'),
                               text=discharge_trend['Discharges'], textposition='top center'))
fig_trend.update_layout(title='Admission & Discharge Trends', xaxis_title='Date', yaxis_title='Count',
                        template='plotly_white', hovermode='x unified')
fig_trend.show()

# 2. Day-wise Admission Rates
data['admit_day'] = data['admission_date'].dt.day_name()
admit_by_day = data['admit_day'].value_counts().reset_index()
admit_by_day.columns = ['Day', 'Admissions']
fig_daywise = px.bar(admit_by_day, x='Day', y='Admissions', title='Day-wise Admission Rates',
                     template='plotly_white', color='Admissions', color_continuous_scale='Viridis')
fig_daywise.update_traces(hovertemplate='<b>Day</b>: %{x}<br><b>Admissions</b>: %{y}',
                          text=admit_by_day['Admissions'], textposition='outside')
fig_daywise.show()

# 3. Ward-Level Congestion – Patient Count
ward_congestion = data['ward'].value_counts().reset_index()
ward_congestion.columns = ['Ward', 'Patients']
fig_congestion = px.bar(ward_congestion, x='Ward', y='Patients', title='Ward-Level Congestion (Patient Volume)',
                        template='plotly_white', color='Patients', color_continuous_scale='Reds')
fig_congestion.update_traces(hovertemplate='<b>Ward</b>: %{x}<br><b>Patients</b>: %{y}',
                             text=ward_congestion['Patients'], textposition='outside')
fig_congestion.show()

# 4. Patient Volume Trend
volume_trend = data.groupby('admission_date').size().reset_index(name='Admissions')
fig_volume = px.line(volume_trend, x='admission_date', y='Admissions', title='Patient Volume Trend Over Time',
                     labels={'admission_date': 'Date'}, template='plotly_white', markers=True)
fig_volume.update_traces(hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Admissions</b>: %{y}',
                         line=dict(color='blue'),
                         mode='lines+markers+text',
                         text=volume_trend['Admissions'], textposition='top center')
fig_volume.update_layout(xaxis_title='Date', yaxis_title='Number of Admissions', hovermode='x unified')
fig_volume.show()
# -----------------------------
# READMISSION RATE BY WARD
# -----------------------------
# Sort and identify readmissions
data = data.sort_values(by=['Patient ID', 'admission_date'])
data['next_admission'] = data.groupby('Patient ID')['admission_date'].shift(-1)
data['current_discharge'] = data['discharge_date']
data['days_until_readmit'] = (data['next_admission'] - data['current_discharge']).dt.days
data['is_readmitted'] = data['days_until_readmit'].apply(lambda x: 1 if 0 < x <= 30 else 0)

# Calculate readmission rate
readmit_stats = data.groupby('ward').agg(
    total_discharges=('Patient ID', 'count'),
    readmissions=('is_readmitted', 'sum')
).reset_index()
readmit_stats['readmission_rate'] = readmit_stats['readmissions'] / readmit_stats['total_discharges']

# Format as percentage for custom display (optional, for bar labels if needed)
readmit_stats['readmission_label'] = (readmit_stats['readmission_rate'] * 100).round(1).astype(str) + '%'

# Interactive Bar Chart – Readmission Rate by Ward (with % on Y-axis)
fig_readmit = px.bar(readmit_stats, x='ward', y='readmission_rate',
                     title='Readmission Rate by Ward (within 30 Days)',
                     labels={'ward': 'Ward', 'readmission_rate': 'Readmission Rate'},
                     template='plotly_white',
                     color='readmission_rate', color_continuous_scale='Purples')

# Update tooltip and y-axis format
fig_readmit.update_traces(
    hovertemplate='<b>Ward</b>: %{x}<br><b>Readmission Rate</b>: %{y:.1%}'
)

# Show bar values (optional — for manager visibility)
fig_readmit.update_traces(
    text=readmit_stats['readmission_label'],
    textposition='outside'
)

# Set y-axis to show 0%, 10%, 20%, etc.
fig_readmit.update_layout(
    xaxis_title='Ward',
    yaxis_title='Readmission Rate (%)',
    yaxis_tickformat='.0%',
    hovermode='x unified',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

fig_readmit.show()
