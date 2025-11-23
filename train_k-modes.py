import numpy as np
import pandas as pd
from kmodes.kmodes import KModes
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import OneHotEncoder

# Load dataset
df = pd.read_csv('/home/artha/Documents/Cluster/Customer Purchase Behaviour.csv')
X1 = df.drop(columns=['Customer ID'])

print("== First 5 Rows of the Dataset ==")
print(df.head())

# Null value check
print("\n \n== Null Value Check ==")
print(df.isnull().sum())

# cols = df.columns
# n_cols = 3  # jumlah plot per baris (boleh diubah)
# n_rows = math.ceil(len(cols) / n_cols)

# plt.figure(figsize=(5*n_cols, 4*n_rows))

# for i, col in enumerate(cols, 1):
#     plt.subplot(n_rows, n_cols, i)
#     sns.countplot(x=df[col])
#     plt.title(col)
#     plt.xticks(rotation=45)

# plt.tight_layout()
# Elbow Method pakai cost

X_np = X1.values
costs = []
K = range(2, 11)

for k in K:
    km = KModes(n_clusters=k, init='Huang', n_init=5, verbose=0, random_state=111)
    km.fit_predict(X_np)
    costs.append(km.cost_)

plt.figure(figsize=(10,5))
plt.plot(K, costs, marker='o')
plt.title("Elbow Plot K-Modes")
plt.xlabel("Number of Clusters K")
plt.ylabel("Cost")
plt.show()

# One-hot encode untuk silhouette score
encoder = OneHotEncoder()
X_enc = encoder.fit_transform(X_np).toarray()

# Pilih K terbaik berdasarkan hasil elbow kamu
k_best = 3
km = KModes(n_clusters=k_best, init='Huang', n_init=10, verbose=0, random_state=111)
labels = km.fit_predict(X_np)

sil_score = silhouette_score(X_enc, labels, metric='hamming')
print("Silhouette Score:", sil_score)

# Tambahkan label ke DataFrame
df['Cluster'] = labels
print(df.head())

# Cek distribusi cluster
print(df['Cluster'].value_counts())