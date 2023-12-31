import pandas as pd
import numpy as np
import os
import seaborn as sn
import matplotlib.pyplot as plt

# Exercise
excel_file_path = "./bhp.csv"
df = pd.read_csv(excel_file_path)

lower_quantile = 0.01
higher_quantile = 0.99
std_deviation = 3

# Display the 01th and 99th percentiles of the 'price_per_sqft' column
print("01th and 99th percentiles of 'price_per_sqft' column:")
print(df.price_per_sqft.quantile([lower_quantile, higher_quantile]))
print("\n")

# Display descriptive statistics of the 'price' column
print("Descriptive statistics of 'price' column:")
print(df.describe())
print("\n")

# Apply log with base 10 to the 'price' column
df["price_per_sqft"] = df["price_per_sqft"].apply(np.log10)

# Calculate the 01th and 99th percentiles
per_01 = df.price_per_sqft.quantile(lower_quantile)
per_99 = df.price_per_sqft.quantile(higher_quantile)
per_01 -= 1.5 * (per_99 - per_01)
per_99 += 1.5 * (per_99 - per_01)

# Filter out outliers based on the percentiles
df_no_outlier = df[(df.price_per_sqft > per_01) & (df.price_per_sqft < per_99)]

df_no_outlier["zscore"] = (
    df_no_outlier["price_per_sqft"] - df_no_outlier["price_per_sqft"].mean()
) / df_no_outlier["price_per_sqft"].std()

# removing outlier using zscore
df_no_outlier = df_no_outlier[
    (df_no_outlier["zscore"] > -std_deviation)
    & (df_no_outlier["zscore"] < std_deviation)
]

# Display lengths of the original and filtered DataFrames
print(
    f"Original DataFrame length: {len(df)}, Filtered DataFrame length: {len(df_no_outlier)}"
)
print("\n")

# Display standard deviations of the 'price_per_sqft' column in both DataFrames
print(
    f"Standard deviation of 'price_per_sqft' column in the original DataFrame: {df['price_per_sqft'].std()}"
)
print(
    f"Standard deviation of 'price_per_sqft' column in the filtered DataFrame: {df_no_outlier['price_per_sqft'].std()}"
)
print("\n")

# Display descriptive statistics of the 'price_per_sqft' column in the filtered DataFrame
print("Descriptive statistics of 'price_per_sqft' column in the filtered DataFrame:")
print(df_no_outlier.price_per_sqft.describe())
print("\n")

# Specify the path where you want to save the CSV file
csv_file_path = "./output_file.csv"

# Check if the file already exists and delete it
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)
    print(f"Existing file '{csv_file_path}' deleted.")
    print("\n")

# Write the DataFrame without outliers to a CSV file
df_no_outlier.to_csv(csv_file_path, index=False)

# normal distribution
# if you apply log function to a datset it becomes log normally distributed
sn.histplot(data=df_no_outlier["price_per_sqft"], kde=True, log_scale=True)
plt.show()
