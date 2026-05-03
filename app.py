from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import numpy as np # Calculations ke liye

app = Flask(__name__, template_folder="templates")

# Safe CSV path
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "smart_crime_data.csv")

# Load dataset
df = pd.read_csv(csv_path)

# --- 1. LIVE NEWS SCRAPER ---
def fetch_crime_news():
    try:
        url = "https://news.google.com/search?q=crime%20maharashtra"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news = [item.get_text() for item in soup.find_all('a', class_='J7Yfub')[:5]]
        return news if news else ["No live updates at the moment."]
    except:
        return ["Server busy: Unable to fetch live news."]

# --- 2. ADVANCED: CORRELATION ENGINE (Literacy vs Crime) ---
@app.route("/correlation-analysis")
def correlation_analysis():
    correlation_data = df[['City', 'Literacy', 'Crime_Rate']].to_dict(orient="records")
    return jsonify(correlation_data)

# --- 3. ADVANCED: CRIME FORECASTING (Simple Trend Projection) ---
@app.route("/forecast/<city_name>")
def forecast(city_name):
    city_data = df[df['City'].str.contains(city_name, case=False)]
    if city_data.empty:
        return jsonify({"error": "City not found"}), 404
    
    current_cases = int(city_data.iloc[0]['Total_Cases'])
    future_trend = [int(current_cases * (1 + (i * 0.02))) for i in range(1, 7)]
    
    return jsonify({
        "city": city_name,
        "current": current_cases,
        "forecast_6_months": future_trend,
        "labels": ["May", "June", "July", "Aug", "Sept", "Oct"]
    })

# --- 4. UPDATED: RED ALERT ZONE HEATMAP (Added New Logic Here) ---
@app.route("/heatmap-data")
def heatmap_data():
    heat_list = []
    # Hum Crime_Rate ka use karke intensity calculate karenge
    # Jitna zyada Crime Rate, utna gehra 'Red Glow' map par dikhega
    if not df.empty:
        max_rate = df['Crime_Rate'].max()
        for index, row in df.iterrows():
            if 'Lat' in row and 'Lon' in row:
                # Intensity scale: 0.1 (Low) se 1.0 (High/Red Alert)
                intensity = float(row['Crime_Rate'] / max_rate)
                # Ensure intensity isn't too low to be visible
                intensity = max(intensity, 0.4) 
                heat_list.append([row['Lat'], row['Lon'], intensity])
    return jsonify(heat_list)

# --- EXISTING ROUTES (KEEPING AS IT IS) ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all")
def all_data():
    return jsonify(df.to_dict(orient="records"))

@app.route("/city/<name>")
def city(name):
    name = name.strip().lower()
    df["City_clean"] = df["City"].str.strip().str.lower()
    row = df[df["City_clean"] == name]
    return jsonify(row.to_dict(orient="records"))

@app.route("/compare")
def compare():
    data = df[df["City"].isin(["Mumbai", "Pune", "Nagpur", "Chandrapur", "Thane"])]
    return jsonify(data.to_dict(orient="records"))

@app.route("/live-news")
def live_news():
    return jsonify({"news": fetch_crime_news()})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        cases = int(data.get("Total_Cases", 0))
        rate = int(data.get("Crime_Rate", 0))
        if cases > 5000 or rate > 400:
            result = "High"
        elif cases > 2000 or rate > 200:
            result = "Medium"
        else:
            result = "Low"
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/highrisk")
def highrisk():
    data = df[df["Risk_Level"] == "High"]
    return jsonify(data.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)