import yfinance as yf
import matplotlib.pyplot as plt
import seaborn

GME = yf.Ticker("GME")

# get stock info
# print(msft.info)

# get historical market data
hist = GME.history(period="50d")
print(hist)

# Plot
hist['Close'].plot(figsize=(16, 9))
plt.show()