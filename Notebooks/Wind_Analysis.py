#Importing Libraries and default settings
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
script_dir = os.path.dirname(os.path.abspath(__file__))
images_folder = os.path.join(script_dir, "images")
os.makedirs(images_folder, exist_ok=True)

#Reading the file
network_path = r"C:\Users\z0050910\Wind Data Analysis\Data\Dataset.csv"
local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw", "Dataset.csv")
if os.path.exists(network_path):
    path = network_path
    print("Using network path")
else:
    path = local_path
    print("Using local path")
print(os.path.exists(path))
df = pd.read_csv(path)

#Pre Analysis
print(df.head())
print(df.columns)
print(df.info())
print(df.describe())
print(df.duplicated().sum())

#Handling Data types
df['Date/Time'] = pd.to_datetime(df['Date/Time'], dayfirst=True)
print(df.info())

#Date and Time Segregation
df["Month"]= df["Date/Time"].dt.month
df["Hour"]= df["Date/Time"].dt.hour
df["Day"]= df["Date/Time"].dt.day
print(df.head())

#Calculating Negative Wind Speed and Negative power, if any
negative_wind = df[df['Wind Speed (m/s)'] < 0]
print("Negative Wind Speed:", len(negative_wind))
negative_power = df[df['LV ActivePower (kW)'] < 0]
print("Negative Active Power:", len(negative_power))
print("\nNegative Power Summary:")
print(negative_power['LV ActivePower (kW)'].describe())
print("\nWind Speed during negative power events:")
print(negative_power['Wind Speed (m/s)'].describe())

#Efficiency Calculator
df['Efficiency'] = (
    df['LV ActivePower (kW)'] /
    df['Theoretical_Power_Curve (KWh)']
)
print("Efficiency:")
print(df["Efficiency"].describe())
df["Efficiency"] = df["Efficiency"].replace([np.inf, -np.inf], np.nan)
print("Efficiency:")
print(df["Efficiency"].describe())

#Power Loss
df["Power Loss"]= (
    df['Theoretical_Power_Curve (KWh)']-
       df['LV ActivePower (kW)']
)
print("Power Loss:")
print(df["Power Loss"].describe())
sns.histplot(df["Power Loss"], bins=50)
plt.title("Power Loss")
plt.ylabel("Frequency")
plt.savefig(os.path.join(images_folder, "P1.png"), bbox_inches="tight")  
plt.close()
sns.scatterplot(x=df["Wind Speed (m/s)"], y=df["Power Loss"])
plt.title("Impact of Wind Speed on Power Loss")
plt.savefig(os.path.join(images_folder, "P2.png"), bbox_inches="tight")  
plt.close()

#Windspeed Distribution
plt.figure()
sns.histplot(
    df["Wind Speed (m/s)"],
    bins=30,
    kde=True,
    color="skyblue"
)
plt.title("Wind Speed Distribution")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Frequency")
plt.savefig(os.path.join(images_folder, "P3.png"), bbox_inches="tight")  
plt.close()

#Active Power Distribution
plt.figure()
sns.histplot(
    df["LV ActivePower (kW)"],
    bins=30,
    kde=True,
    color="green"
)
plt.title("Active Power Distribution")
plt.xlabel("Active Power (kW)")
plt.ylabel("Frequency")
plt.savefig(os.path.join(images_folder, "P4.png"), bbox_inches="tight")  
plt.close()

#Wind Speed vs. Active Power 
plt.figure()
sns.scatterplot(
    x = df["Wind Speed (m/s)"],
    y = df['LV ActivePower (kW)'],
    alpha = 0.5
)
plt.title("Wind Speed vs. Active Power")
plt.savefig(os.path.join(images_folder, "P5.png"), bbox_inches="tight")  
plt.close()

#Wind Speed vs. Theoretical Power
plt.figure()
sns.scatterplot(
    data=df,
    x="Wind Speed (m/s)",
    y="Theoretical_Power_Curve (KWh)",
    alpha=0.5,
    color="red"
)
plt.title("Wind Speed vs Theoretical Power")
plt.savefig(os.path.join(images_folder, "P6.png"), bbox_inches="tight")  
plt.close()

#Actual vs. Theoretical Power
plt.figure()
sns.scatterplot(
    data= df,
    x= "Theoretical_Power_Curve (KWh)",
    y = "LV ActivePower (kW)"
)
plt.title("Actual Vs. Theoretical Power")
plt.savefig(os.path.join(images_folder, "P7.png"), bbox_inches="tight")  
plt.close()

#Monthly Power Generation Data
monthly_power = df.groupby("Month")["LV ActivePower (kW)"].sum()
monthly_power.plot(
    kind="bar",
    color="orange"
)
plt.title("Monthly Power Generation")
plt.xlabel("Month")
plt.ylabel("Power Generated (kW)")
plt.savefig(os.path.join(images_folder, "P8.png"), bbox_inches="tight")  
plt.close()

#Hourly Average Power Generation
hourly_power = df.groupby("Hour")["LV ActivePower (kW)"].mean()
hourly_power.plot(
    kind = "bar",
    color= "green"
)
plt.title("Hourly Average Power Generation")
plt.xlabel("Hour")
plt.ylabel("Average Power Generated (kW)")
plt.savefig(os.path.join(images_folder, "P9.png"), bbox_inches="tight")  
plt.close()

#Wind Direction vs. Active Power
plt.figure()
sns.scatterplot(
    data=df,
    x="Wind Direction (°)",
    y="LV ActivePower (kW)",
    alpha=0.5,
    color="brown"
)
plt.title("Wind Direction vs Active Power")
plt.savefig(os.path.join(images_folder, "P10.png"), bbox_inches="tight")
plt.close()

#Heatmap for Correlation
correlation = df[
    [
        "LV ActivePower (kW)",
        "Wind Speed (m/s)",
        "Theoretical_Power_Curve (KWh)",
        "Wind Direction (°)"
    ]
].corr()
sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)
plt.title("Correlation Matrix")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(images_folder, "P11.png"), bbox_inches="tight")  
plt.close()

#Top 10 Power Losses
top_losses = df.sort_values(
    by="Power Loss",
    ascending=False
)
print(top_losses.head(10))

#Processing the Data
folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(folder, exist_ok=True)
file_path = os.path.join(folder, "Processed_Data.csv")
df.to_csv(file_path, index=False)
print("Saved at:", file_path)