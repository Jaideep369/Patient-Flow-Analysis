import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# Load patient data
data = pd.read_csv('/content/hospital_datas.csv')

# Calculate length of stay
data['admission_date'] = pd.to_datetime(data['admission_date'])
data['discharge_date'] = pd.to_datetime(data['discharge_date'])
data['length_of_stay'] = (data['discharge_date'] - data['admission_date']).dt.days
print(data['length_of_stay'])

# Calculate average length of stay
avg_length_of_stay = data['length_of_stay'].mean()
print(f'Average length of stay: {avg_length_of_stay} days')

# Calculate average length of stay by ward
avg_length_of_stay = data.groupby('ward')['length_of_stay'].mean().reset_index()
print(avg_length_of_stay)

# Plot average length of stay by ward
plt.figure(figsize=(10,6))
sns.barplot(x='ward', y='length_of_stay', data=avg_length_of_stay)
plt.title('Average Length of Stay by Ward')
plt.xlabel('Ward')
plt.ylabel('Average Length of Stay')
plt.show()



# Calculate bed occupancy by ward
data['bed_days_used'] = data['length_of_stay']
bed_occupancy = data.groupby('ward')['bed_days_used'].sum().reset_index()
total_beds = data['ward'].value_counts().max() # assuming total beds = max ward capacity
bed_occupancy['bed_occupancy_rate'] = bed_occupancy['bed_days_used'] / (total_beds * data['length_of_stay'].mean())
print(bed_occupancy['bed_occupancy_rate'])

# Plot bed occupancy rate by ward in barplot format
plt.figure(figsize=(10,6))
sns.barplot(x='ward', y='bed_occupancy_rate', data=bed_occupancy)
plt.title('Bed Occupancy Rate by Ward')
plt.xlabel('Ward')
plt.ylabel('Bed Occupancy Rate')
plt.show()

# Plot bed occupancy rate by ward in lineplot format
plt.figure(figsize=(10,6))
fig, ax = plt.subplots(2, 1,)
sns.lineplot(x='ward', y='bed_occupancy_rate', data=bed_occupancy, ax=ax[1])
ax[1].set_title('Bed Occupancy Rate by Ward')
ax[1].set_xlabel('Ward')
ax[1].set_ylabel('Bed Occupancy Rate')
plt.tight_layout()
plt.show()


# Plot bed occupancy and average stay metrics
fig, ax = plt.subplots(2, 1, figsize=(10, 10))
sns.barplot(x='ward', y='length_of_stay', data=avg_length_of_stay, ax=ax[0])
ax[0].set_title('Average Length of Stay by Ward')
ax[0].set_xlabel('Ward')
ax[0].set_ylabel('Average Length of Stay')



