from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fname = "Near Field ROV Laboratory TSS rev0.csv"
df = pd.read_csv(fname, index_col=0, parse_dates=[3])
df = df[['DateTime (UTC)', 'Total Suspended Solids (mg/L)', 'Seabird CTD Turbidity (NTU)']]
df.columns = ['datetime', 'ssc', 'ntu']
df.dropna(inplace=True)
reg = LinearRegression(fit_intercept=False).fit(df[["ssc"]], df["ntu"])
B = reg.coef_[0]
A = reg.intercept_

x = np.linspace(0.1, 1000, 100)
y = B * x + A


fig, ax = plt.subplots()
ax.scatter(df['ntu'], df['ssc'])
ax.plot(x, y, color='red', label=f'SSC = {B:.2f} * NTU + {A:.2f}')
ax.set_xlabel('NTU')
ax.set_ylabel('SSC (mg/L)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.1, 1000)
ax.set_ylim(0.1, 1000)
ax.legend()
plt.show()