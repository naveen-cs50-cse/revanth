import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt  # ✅ Correct import

st.title('💰 Crypto Currency Dashboard')
st.subheader('📈 Live Updates')

# Define coins and currency
coins = ["bitcoin", "ethereum", "solana", "cardano"]
currency = "usd"
prices = {}

# Fetch prices from CoinGecko API
for coin in coins:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
    response = requests.get(url)
    data = response.json()
    try:
        prices[coin] = data[coin][currency]
    except KeyError:
        prices[coin] = None  # Avoid crash if coin not found

# Display prices in table
df = pd.DataFrame(prices.items(), columns=["Coin", "Price (USD)"])
st.table(df)

# Bar chart
st.subheader("📊 Price Chart")
x = list(prices.keys())
height = list(prices.values())

# Ensure all prices are numeric
df["Price (USD)"] = pd.to_numeric(df["Price (USD)"], errors='coerce')

# Drop any rows with invalid (NaN) prices
df = df.dropna()

# Plot using dynamic colors matching data length
fig, ax = plt.subplots()
colors = ['red', 'yellow', 'green', 'pink'][:len(df)]  # Adjust to match number of coins
ax.bar(df["Coin"], df["Price (USD)"], color=colors)
ax.set_ylabel("Price in USD")
ax.set_title("Current Prices of Selected Cryptos")
st.pyplot(fig)


# Sidebar: refresh settings
st.sidebar.title("⚙️ Settings")
refresh_rate = st.sidebar.slider("⏱️ Refresh every N seconds", 5, 60, 10)
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh")

# Auto-refresh logic
import time
if auto_refresh:
    time.sleep(refresh_rate)
    st.experimental_rerun()

