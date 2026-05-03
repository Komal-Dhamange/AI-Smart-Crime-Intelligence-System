import pandas as pd
import random

cities = {
    "Mumbai": 45000,
    "Pune": 32000,
    "Nagpur": 22000,
    "Thane": 28000,
    "Nashik": 18000,
    "Aurangabad": 15000,
    "Solapur": 13000,
    "Kolhapur": 11000,
    "Ratnagiri": 5000,

    "Chandrapur": 15000,
    "Ballarpur": 7000,
    "Bhadravati": 6500,
    "Rajura": 6000,
    "Mul": 4200,
    "Warora": 5200,
    "Gadchiroli": 9500,
    "Yavatmal": 12500,
    "Amravati": 16000,
    "Akola": 12000,
    "Wardha": 8500
}

rows = []

for year in range(2000, 2027):
    growth = (year - 2000) * 0.03

    for city, base in cities.items():
        total = int(base * (1 + growth) + random.randint(-800, 800))
        cyber = int(total * (0.005 + (year - 2000) * 0.0018))
        women = int(total * 0.14)
        theft = int(total * 0.32)
        murder = max(2, int(total * 0.004))

        if total > 30000:
            risk = "High"
        elif total > 12000:
            risk = "Medium"
        else:
            risk = "Low"

        rows.append([
            year, city, total, cyber, women, theft, murder, risk
        ])

df = pd.DataFrame(rows, columns=[
    "Year",
    "City",
    "Total_Cases",
    "Cyber_Crime",
    "Women_Crime",
    "Theft",
    "Murder",
    "Risk_Level"
])

df.to_csv("maharashtra_full_city_crime_2000_2026.csv", index=False)

print("CSV Created Successfully!")
print(df.head(25))