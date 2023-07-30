import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chardet
from datetime import datetime
from babel.dates import format_date

# Load the data
rawdata = open("../data/save.csv", "rb").read()
result = chardet.detect(rawdata)
encoding = result["encoding"]


# Load the CSV file with the correct delimiter and skipping the first row
# Also drop the last 'Unnamed' column
bank_data = pd.read_csv(
    "../data/save.csv", encoding=encoding, delimiter=";", skiprows=1
)
bank_data = bank_data.drop(columns=["Unnamed: 4"])

# Rename the columns
bank_data.columns = ["Date", "Libellé", "Montant", "Devise"]


# Supprimer la première ligne si elle n'est pas nécessaire
# bank_data = bank_data.iloc[1:]


# Convertir 'Date' en format datetime
bank_data["Date"] = pd.to_datetime(bank_data["Date"], format="%d/%m/%Y")

# Convertir 'Montant' en format numérique et convertir les erreurs en NaN
bank_data["Montant"] = pd.to_numeric(
    bank_data["Montant"].str.replace(",", "."), errors="coerce"
)

# Supprimer les lignes avec NaN dans 'Montant'
bank_data = bank_data.dropna(subset=["Montant"])

# Trier par date
bank_data = bank_data.sort_values("Date")


# Calculate balance
bank_data["Balance"] = bank_data["Montant"].cumsum()

# Calculate credits and debits
bank_data["Credits"] = bank_data["Montant"].clip(lower=0)
bank_data["Debits"] = bank_data["Montant"].clip(upper=0)

# Group data by month
monthly_data = bank_data.resample("M", on="Date").sum()

# Get the last balance of each month
end_of_month_balance = bank_data.resample("M", on="Date")["Balance"].last()

# Replace the 'Balance' column in monthly_data with end_of_month_balance
monthly_data["Balance"] = end_of_month_balance

# Calculate net income for each month
monthly_data["Net"] = monthly_data["Credits"] + monthly_data["Debits"]

# Make debits positive for visualization
monthly_data["Debits"] = monthly_data["Debits"].abs()

# Find the minimum and maximum values to set the same scale for both Montant and Balance
min_val = min(monthly_data[["Credits", "Debits", "Net", "Balance"]].min())
max_val = max(monthly_data[["Credits", "Debits", "Net", "Balance"]].max())

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 8))

# Define bar width
bar_width = 0.25

# Set position of bar on X axis
r1 = np.arange(len(monthly_data))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Make the bar plot
ax1.bar(
    r1,
    monthly_data["Credits"],
    color="green",
    width=bar_width,
    edgecolor="grey",
    label="Credits",
)
ax1.bar(
    r2,
    monthly_data["Debits"],
    color="red",
    width=bar_width,
    edgecolor="grey",
    label="Debits",
)
ax1.bar(
    r3,
    monthly_data["Net"],
    color="purple",
    width=bar_width,
    edgecolor="grey",
    label="Net",
)

# parse the date
date = datetime.strptime("2023-07", "%Y-%m")

# format the date
formatted_date = format_date(date, "MMMM yyyy", locale="fr")

# Add xticks on the middle of the group bars
ax1.set_xlabel("Mois", fontweight="bold")
ax1.set_ylabel("Montant", fontweight="bold")
ax1.set_xticks([r + bar_width for r in range(len(monthly_data))])
ax1.set_xticklabels([date.strftime(formatted_date) for date in monthly_data.index])

# Set the same scale for Montant
ax1.set_ylim(min_val, max_val)

# Make the line plot for balance
ax1.plot(r2, monthly_data["Balance"], color="blue", label="Balance")

# Create legend & Show graphic
ax1.legend(loc="upper left")
plt.title("Crédits, Débits, Net et Balance par mois")
plt.grid(True)
plt.show()
