# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H32VLvvHSJ4JMRoGHUAuv2wgflgFhz1L
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans

# Load the data
file_path = 'walmart_cleaned.csv'
data = pd.read_csv(file_path)

# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'])

# 1. Weekly Sales Trends by Store
stores_to_plot = [1, 2, 3]
plot_data = data[data['Store'].isin(stores_to_plot)]

plt.figure(figsize=(14, 8))
for store in stores_to_plot:
    store_data = plot_data[plot_data['Store'] == store]
    plt.plot(store_data['Date'], store_data['Weekly_Sales'], label=f'Store {store}')

plt.title('Weekly Sales Trends by Store')
plt.xlabel('Date')
plt.ylabel('Weekly Sales')
plt.legend()
plt.grid(True)
plt.savefig('weekly_sales_trends_by_store.png')
plt.close()

# 2. Impact of Holidays on Sales
holiday_sales = data[data['IsHoliday'] == 1]['Weekly_Sales']
non_holiday_sales = data[data['IsHoliday'] == 0]['Weekly_Sales']

sales_comparison = pd.DataFrame({
    'Type': ['Holiday'] * len(holiday_sales) + ['Non-Holiday'] * len(non_holiday_sales),
    'Weekly_Sales': list(holiday_sales) + list(non_holiday_sales)
})

plt.figure(figsize=(10, 6))
sns.boxplot(x='Type', y='Weekly_Sales', data=sales_comparison)
plt.title('Impact of Holidays on Weekly Sales')
plt.xlabel('Week Type')
plt.ylabel('Weekly Sales')
plt.grid(True)
plt.savefig('impact_of_holidays_on_sales.png')
plt.close()

# 3. Correlation between Sales and Economic Factors
correlation_data = data[['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Weekly Sales and Economic Factors')
plt.savefig('correlation_matrix.png')
plt.close()

# 4. Departmental Performance
dept_sales = data.groupby('Dept')['Weekly_Sales'].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.barplot(x='Dept', y='Weekly_Sales', data=dept_sales.sort_values(by='Weekly_Sales', ascending=False))
plt.title('Total Sales by Department')
plt.xlabel('Department')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('total_sales_by_department.png')
plt.close()

# 5. Seasonal Sales Analysis
data['Season'] = data['Date'].dt.month % 12 // 3 + 1
season_dict = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
data['Season'] = data['Season'].map(season_dict)

season_sales = data.groupby('Season')['Weekly_Sales'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='Season', y='Weekly_Sales', data=season_sales, palette='viridis')
plt.title('Average Sales by Season')
plt.xlabel('Season')
plt.ylabel('Average Weekly Sales')
plt.grid(True)
plt.savefig('average_sales_by_season.png')
plt.close()

# 6. Forecasting Future Sales
data['Week'] = data['Date'].dt.isocalendar().week
features = ['Store', 'Dept', 'Week', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
X = data[features]
y = data['Weekly_Sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

plt.figure(figsize=(14, 8))
plt.scatter(y_test, y_pred, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.title('Actual vs Predicted Sales')
plt.xlabel('Actual Sales')
plt.ylabel('Predicted Sales')
plt.grid(True)
plt.savefig('actual_vs_predicted_sales.png')
plt.close()

print(f'Mean Squared Error: {mse}')

# 7. Average Basket Value Analysis
average_basket = data.groupby(['Store', 'Dept'])['Weekly_Sales'].mean().reset_index()

plt.figure(figsize=(14, 8))
sns.barplot(x='Store', y='Weekly_Sales', data=average_basket, ci=None, palette='coolwarm')
plt.title('Average Basket Value by Store')
plt.xlabel('Store')
plt.ylabel('Average Basket Value (Average Weekly Sales)')
plt.grid(True)
plt.savefig('average_basket_value_by_store.png')
plt.close()

plt.figure(figsize=(14, 8))
sns.barplot(x='Dept', y='Weekly_Sales', data=average_basket, ci=None, palette='coolwarm')
plt.title('Average Basket Value by Department')
plt.xlabel('Department')
plt.ylabel('Average Basket Value (Average Weekly Sales)')
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('average_basket_value_by_department.png')
plt.close()

# 8. Store Clustering
clustering_features = ['Store', 'Weekly_Sales', 'Size', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
clustering_data = data.groupby('Store').mean().reset_index()

kmeans = KMeans(n_clusters=3, random_state=42)
clustering_data['Cluster'] = kmeans.fit_predict(clustering_data[clustering_features[1:]])

plt.figure(figsize=(10, 6))
sns.scatterplot(data=clustering_data, x='Store', y='Weekly_Sales', hue='Cluster', palette='viridis', s=100)
plt.title('Store Clustering by Performance')
plt.xlabel('Store')
plt.ylabel('Average Weekly Sales')
plt.grid(True)
plt.savefig('store_clustering_by_performance.png')
plt.close()