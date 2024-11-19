import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Step 1: Load Data
# Adjust file paths to include the folder name
co2_data = pd.read_csv('CO2 Python Data/cleaned_co2_data.csv')  # Path adjusted for folder
temperature_data = pd.read_csv('CO2 Python Data/cleaned_gistemp_data.csv')  # Path adjusted for folder

# Check the columns
print("CO2 Data Columns:", co2_data.columns)
print("Temperature Data Columns:", temperature_data.columns)

# Step 2: Clean Data
# Convert Year to datetime in CO2 data
co2_data['Year'] = pd.to_datetime(co2_data['Year'], format='%Y')

# Select monthly columns and calculate the annual average temperature, ignoring missing values
monthly_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
temperature_data['Average_Temperature'] = temperature_data[monthly_columns].mean(axis=1)

# Display results for Average Temperature to verify calculation
print(temperature_data[['Year', 'Average_Temperature']])

# Save the temperature data with the Average_Temperature column to a new CSV file
temperature_data.to_csv('CO2 Python Data/temperature_with_annual_avg.csv', index=False)

# Convert Year to datetime in temperature data
temperature_data['Year'] = pd.to_datetime(temperature_data['Year'], format='%Y')

# Step 3: Merge Data
merged_data = pd.merge(co2_data, temperature_data[['Year', 'Average_Temperature']], on='Year')

# Save merged data to CSV in the same folder
merged_data.to_csv('CO2 Python Data/merged_data.csv', index=False)

# Check merged data columns
print("Merged Data Columns:", merged_data.columns)

# Step 4: Analyze Correlation
correlation, p_value = pearsonr(merged_data['Mean_CO2'], merged_data['Average_Temperature'])
print(f'Correlation: {correlation}, P-Value: {p_value}')

# Step 5: Visualization
plt.figure(figsize=(12, 6))

# Scatter plot
sns.scatterplot(data=merged_data, x='Mean_CO2', y='Average_Temperature')
plt.title('CO2 Emissions vs Global Average Temperature')
plt.xlabel('CO2 Emissions (Mean_CO2)')
plt.ylabel('Global Average Temperature (°C)')
plt.grid()
plt.show()

# Line graph for trends
plt.figure(figsize=(12, 6))
plt.plot(merged_data['Year'], merged_data['Mean_CO2'], label='CO2 Emissions', color='blue')
plt.plot(merged_data['Year'], merged_data['Average_Temperature'], label='Global Average Temperature', color='red')
plt.title('Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()
plt.grid()
plt.show()
