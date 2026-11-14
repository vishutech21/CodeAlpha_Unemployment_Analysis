
import pandas as pd

# Load dataset
file_path = "data/Unemployment in India.csv"

df = pd.read_csv(file_path, sep="\t")

# Clean column names
df.columns = df.columns.str.strip()

# Check columns
print("Column Names:")
print(df.columns.tolist())

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())


# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Remove extra spaces
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Convert date column
df["Date"] = pd.to_datetime(
    df["Date"].str.strip(),
    format="%d-%m-%Y",
    errors="coerce"
)

# Convert numerical columns
numeric_cols = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates()

print("\nCleaned Dataset Shape:")
print(df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())


# Find rows containing missing values
print("\nRows with Missing Values:")
print(df[df.isnull().any(axis=1)])

# Remove completely empty rows
df.dropna(how="all", inplace=True)

# Remove rows with remaining missing values
df.dropna(inplace=True)

print("\nMissing Values After Fix:")
print(df.isnull().sum())

print("\nFinal Dataset Shape:")
print(df.shape)


import matplotlib.pyplot as plt

# Monthly unemployment trend
monthly_data = df.groupby("Date")[
    "Estimated Unemployment Rate (%)"
].mean().reset_index()

monthly_data = monthly_data.sort_values("Date")

# Create graph
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_data["Date"],
    monthly_data["Estimated Unemployment Rate (%)"],
    marker="o"
)

plt.title("Monthly Unemployment Rate in India")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("monthly_unemployment_trend.png")
plt.show()



# COVID-19 impact analysis
df["Period"] = df["Date"].apply(
    lambda x: "Before COVID-19"
    if x < pd.Timestamp("2020-03-01")
    else "During COVID-19"
)

covid_data = df.groupby("Period")[
    "Estimated Unemployment Rate (%)"
].mean()

print("\nCOVID-19 Impact:")
print(covid_data)

# Plot COVID impact
plt.figure(figsize=(8, 5))

covid_data.plot(kind="bar")

plt.title("Unemployment Rate: Before vs During COVID-19")
plt.xlabel("Period")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("covid19_impact.png")
plt.show()
