from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os

app = Flask(__name__)

# Load and preprocess data
co2_data_path = "CO2 Python Data/cleaned_co2_data.csv"
temp_data_path = "CO2 Python Data/merged_data.csv"

# Read the CSV files
co2_data = pd.read_csv(co2_data_path)
temp_data = pd.read_csv(temp_data_path)

# Calculate correlation
correlation, p_value = pearsonr(temp_data['Mean_CO2'], temp_data['Average_Temperature'])

# Path to save the scatter plot
img_path = "static/co2temp.png"

# Create the scatter plot if it doesn't exist
if not os.path.exists(img_path):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=temp_data, x='Mean_CO2', y='Average_Temperature', color="blue", edgecolor="w", s=100)
    plt.title(f"CO₂ Emissions vs Temperature Change (Correlation: {correlation:.2f})")
    plt.xlabel("Mean CO₂ Levels (ppm)")
    plt.ylabel("Average Temperature (°C)")
    plt.grid()
    plt.savefig(img_path)

# Route for the welcome page
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Route for the purpose page
@app.route("/purpose")
def purpose():
    return render_template("purpose.html", title="Research Purpose")

# Route for the data visualizations page
@app.route("/visualizations")
def visualizations():
    avg_co2 = co2_data['Mean_CO2'].mean()
    avg_temp = temp_data['Average_Temperature'].mean()
    return render_template(
        "visualizations.html",
        title="Data Visualizations",
        correlation=correlation,
        p_value=p_value,
        avg_co2=avg_co2,
        avg_temp=avg_temp,
        img_path=img_path
    )

if __name__ == "__main__":
    app.run(debug=True)
