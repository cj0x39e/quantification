
import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt

# 1. 获取数据 (这里使用模拟数据，实际操作中需要从数据源获取)
np.random.seed(0)  # 设置随机种子以保证结果可重复
dates = pd.date_range('20230101', periods=365)
df = pd.DataFrame(np.random.randn(365, 1).cumsum() + 100, index=dates, columns=['Close'])

# 2. 计算技术指标 (例如：简单移动平均线 SMA)
df['SMA5'] = df['Close'].rolling(window=5).mean() # 5日均线
df['SMA20'] = df['Close'].rolling(window=20).mean() # 20日均线

# 3. 生成交易信号
df['Position'] = 0 # 初始化仓位
df.loc[df['SMA5'] > df['SMA20'], 'Position'] = 1 # 当5日均线高于20日均线时，买入（持有仓位1）
df.loc[df['SMA5'] < df['SMA20'], 'Position'] = 0 # 当5日均线低于20日均线时，卖出（空仓位0）

# 为了避免未来函数，我们将仓位信号滞后一天
df['Position'] = df['Position'].shift(1)
df.fillna(0, inplace=True) # 填充NaN值

# 4. 计算每日收益
df['Returns'] = df['Close'].pct_change()
df['Strategy_Returns'] = df['Position'] * df['Returns']

# 5. 计算累计收益
df['Cumulative_Returns'] = (1 + df['Returns']).cumprod()
df['Cumulative_Strategy_Returns'] = (1 + df['Strategy_Returns']).cumprod()

# 6. 绘制图表
plt.figure(figsize=(12, 6))
plt.plot(df['Cumulative_Returns'], label='Buy and Hold')
plt.plot(df['Cumulative_Strategy_Returns'], label='SMA Strategy')
plt.legend()
plt.title('Backtest Result')
plt.show()

# 7. 打印绩效指标 (可选)
total_return = df['Cumulative_Strategy_Returns'][-1] -1
print(f"Total Return: {total_return:.2%}")

# 计算年化收益率
days = (df.index[-1] - df.index[0]).days
annualized_return = (1 + total_return)**(365/days) - 1
print(f"Annualized Return: {annualized_return:.2%}")