# Rate-Limiter

Rate-Limiter is a Flask-Redis limiter that can be plugged to any web application.

## Installation

'pip install -r requirements.txt' to install required packages 

## Testing 

Configure your variables in .env, and test in tests folder

## Importing the Grafana Dashboard for Rate Limiting
This project includes a pre-built Grafana dashboard for monitoring rate limits.

### **Steps to Import the Dashboard**
1️⃣ Open **Grafana**  
2️⃣ Go to **"Dashboards"** → Click **"Import"**  
3️⃣ **Upload the file** `grafana/rate_limiting_dashboard.json`  
4️⃣ Select your **Prometheus data source**  
5️⃣ Click **"Import"**  

## Working-on:

Working on creating alternate ways of Rate-Limiting (Token, Api-Key based, Cookie-Based)

