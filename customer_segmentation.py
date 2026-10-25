import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Step 1: Load the Dataset
df = pd.read_excel('online_retail_dataset.xlsx')

print("Initial Shape:", df.shape)
df.head()

# Step 2: Data Cleaning and Preprocessing
# Drop missing CustomerIDs as CustomerID is essential for customer segmentation
df = df.dropna(subset=['CustomerID'])

# Remove negative quantities (cancellations) and zero unit prices
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

print("Cleaned Data Shape:", df.shape)

# Step 3: RFM Feature Engineering
# Set reference date (Maximum date in the dataset + 1 day)
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Create RFM DataFrame
rfm_df = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency: Days since last purchase
    'InvoiceNo': 'nunique',                                  # Frequency: Total unique transactions
    'TotalPrice': 'sum'                                      # Monetary: Total amount spent
})

# Rename columns to RFM
rfm_df.columns = ['Recency', 'Frequency', 'Monetary']

print(rfm_df.head())

# Step 4: Feature Scaling
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_df)

# Convert scaled data back to a DataFrame
rfm_scaled_df = pd.DataFrame(rfm_scaled, index=rfm_df.index, columns=['Recency', 'Frequency', 'Monetary'])

# Step 5: Finding Optimal Clusters using Elbow Method
inertia = []
K_range = range(1, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled_df)
    inertia.append(kmeans.inertia_)

# Plot the Elbow Curve
plt.figure(figsize=(8, 4))
plt.plot(K_range, inertia, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.savefig('elbow_method_plot.png', dpi=300)
plt.show()

# Step 6: K-Means Model Training & Customer Segmentation
# Train K-Means model with 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(rfm_scaled_df)
# Save Segmented Customer RFM Data to CSV
rfm_df.to_csv('customer_rfm_segments.csv')

# Assign cluster labels to the main RFM DataFrame
rfm_df['Cluster'] = cluster_labels

print(rfm_df['Cluster'].value_counts())

rfm_df.to_csv('customer_rfm_segments.csv', index=True)
print("RFM Segments with Cluster column saved successfully!")

# Step 7: Visualizing the Segments
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=rfm_df, 
    x='Frequency', 
    y='Monetary', 
    hue='Cluster', 
    palette='viridis', 
    s=100, 
    alpha=0.8
)
plt.title('Customer Segments based on Frequency and Monetary')
plt.xlabel('Frequency')
plt.ylabel('Monetary (Total Spend)')
plt.legend(title='Cluster')
plt.savefig('customer_segments_plot.png', dpi=300)
plt.show()

# Step 8: Cluster Analysis & Summary Statistics
cluster_summary = rfm_df.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']
})
print(cluster_summary)

# Cleaned data ko CSV file mein save karne ke liye yeh code likhein:
df.to_csv('cleaned_online_retail_data.csv', index=False)