import pandas as pd
import numpy as np

print("Pandas version:", pd.__version__)

df = pd.read_csv("car_fuel_efficiency_2026.csv")

print(df.head())
print(df.shape)
print(df.columns)

print("Fuel types:", df["fuel_type"].nunique())
print(df["fuel_type"].unique())

print("Missing values:")
print(df.isna().sum())

asia = df[df["origin"] == "Asia"]

print("Max fuel efficiency in Asia:", asia["fuel_efficiency_mpg"].max())

median_before = df["horsepower"].median()
mode = df["horsepower"].mode()[0]

print("Median before:", median_before)
print("Mode:", mode)

df["horsepower"] = df["horsepower"].fillna(mode)

median_after = df["horsepower"].median()

print("Median after:", median_after)
print("Changed:", median_before != median_after)

print(asia[["vehicle_weight", "model_year"]].head(7))

X = asia[["vehicle_weight", "model_year"]].head(7).values

print("X:")
print(X)

XT = X.T

print("X.T:")
print(XT)

XTX = XT @ X

print("X.T @ X:")
print(XTX)

XTX_inv = np.linalg.inv(XTX)

print("Inverse:")
print(XTX_inv)

y = np.array([1100, 1300, 800, 900, 1000, 1100, 1200])

print("y:")
print(y)

w = XTX_inv @ XT @ y

print("w:")
print(w)

print("Sum of w:", w.sum())