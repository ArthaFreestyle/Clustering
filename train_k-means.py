import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

# Load dataset
df = pd.read_csv('/home/artha/Documents/Cluster/Mall_Customers.csv')

print("== First 5 Rows of the Dataset ==")
print(df.head())

print("\n \n== Dataset Information ==")
print(df.describe())

# Null value check
print("\n \n== Null Value Check ==")
print(df.isnull().sum())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

#Check outliers using boxplot

sns.boxplot(data=df, ax=axes[0])
axes[0].set_title('Boxplot for Outlier Detection (before handling)')


Q1 = df['Annual Income (k$)'].quantile(0.25)
Q3 = df['Annual Income (k$)'].quantile(0.75)
IQR = Q3 - Q1

print("\n \n== Interquartile Range (IQR) ==")
print(IQR)

# Filter out outliers
batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR
outliers = df[(df['Annual Income (k$)'] < batas_bawah) | (df['Annual Income (k$)'] > batas_atas)]

print("\n \n== Outliers in 'Annual Income (k$)' ==")
print(outliers)


# turn outliers into IQR boundaries
df['Annual Income (k$)'] = df['Annual Income (k$)'].clip(lower=batas_bawah, upper=batas_atas)


# Filter out outliers
batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR
outliers = df[(df['Annual Income (k$)'] < batas_bawah) | (df['Annual Income (k$)'] > batas_atas)]

print("\n \n== Outliers in 'Annual Income (k$)' ==")
print(outliers)

#Check outliers using boxplot

sns.boxplot(data=df, ax=axes[1])
axes[1].set_title('Boxplot for Outlier Detection (after handling)')


# amati bentuk visual masing-masing fitur
plt.style.use('fivethirtyeight')
plt.figure(num=2 , figsize = (15 , 6))
n = 0
for x in ['Age' , 'Annual Income (k$)' , 'Spending Score (1-100)']:
    n += 1
    plt.subplot(1 , 3 , n)
    plt.subplots_adjust(hspace =0.5 , wspace = 0.5)
    sns.histplot(
    df[x], kde=True,
    stat="density", kde_kws=dict(cut=3), bins = 20)
    plt.title('Distplot of {}'.format(x))

# Ploting untuk mencari relasi antara Age , Annual Income and Spending Score
plt.figure(num=3 , figsize = (15 , 20))
n = 0
for x in ['Age' , 'Annual Income (k$)' , 'Spending Score (1-100)']:
    for y in ['Age' , 'Annual Income (k$)' , 'Spending Score (1-100)']:
        n += 1
        plt.subplot(3 , 3 , n)
        plt.subplots_adjust(hspace = 0.5 , wspace = 0.5)
        sns.regplot(x = x , y = y , data = df)
        plt.ylabel(y.split()[0]+' '+y.split()[1] if len(y.split()) > 1 else y )


# Melihat sebaran Spending Score dan Annual Income pada Gender
plt.figure(num=4 , figsize = (15 , 8))
for gender in ['Male' , 'Female']:
    plt.scatter(x = 'Annual Income (k$)',y = 'Spending Score (1-100)' ,
    data = df[df['Gender'] == gender] ,s = 200 , alpha = 0.5 ,
    label = gender)
    plt.xlabel('Annual Income (k$)'), plt.ylabel('Spending Score (1-100)')
    plt.title('Annual Income vs Spending Score')
plt.legend()


# Merancang K-Means untuk spending score vs annual income
# Menentukan nilai k yang sesuai dengan Elbow-Method
X1 = df[['Annual Income (k$)' , 'Spending Score (1-100)']].iloc[: , :].values
inertia = []
for n in range(1 , 11):
    algorithm = (KMeans(n_clusters = n ,init='k-means++', n_init = 10,max_iter=300, random_state= 111) )
    algorithm.fit(X1)
    inertia.append(algorithm.inertia_)
# Plot bentuk visual elbow
plt.figure(num=5 , figsize = (15 ,6))
plt.plot(range(1 , 11) , inertia , 'o')
plt.plot(range(1 , 11) , inertia , '-' , alpha = 0.5)
plt.xlabel('Number of Clusters') , plt.ylabel('Inertia')


# Membangun K-Means
algorithm = (KMeans(n_clusters = 3,tol=0.0001, random_state= 111 , algorithm='elkan') )
algorithm.fit(X1)
labels2 = algorithm.labels_
centroids2 = algorithm.cluster_centers_


# Menyiapkan data untuk bentuk visual cluster
labels2 = algorithm.labels_
centroids2 = algorithm.cluster_centers_
step = 0.02
x_min, x_max = X1[:, 0].min() - 1, X1[:, 0].max() + 1
y_min, y_max = X1[:, 1].min() - 1, X1[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, step),
np.arange(y_min, y_max, step))
Z1 = algorithm.predict(np.c_[xx.ravel(), yy.ravel()]) 
# array diratakan 1D


# Melihat bentuk visual cluster
plt.figure(num=6 , figsize = (15 , 7) )
plt.clf()
Z1 = Z1.reshape(xx.shape)
plt.imshow(Z1 , interpolation='nearest',
extent=(xx.min(), xx.max(), yy.min(), yy.max()),
cmap = plt.cm.Pastel2, aspect = 'auto', origin='lower')
plt.scatter( x = 'Annual Income (k$)' ,y = 'Spending Score (1-100)' , data= df , c = labels2 , s = 200 )
plt.scatter(x = centroids2[: , 0] , y = centroids2[: , 1] , s =
300 , c = 'red' , alpha = 0.5)
plt.ylabel('Spending Score (1-100)') , plt.xlabel('Annual Income(k$)')


plt.show()


score2 = silhouette_score(X1, labels2)
print("Silhouette Score: ", score2)