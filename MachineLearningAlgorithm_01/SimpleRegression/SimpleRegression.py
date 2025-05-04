import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##### 単回帰分析 #####

dataset = pd.read_csv('Salary_Data.csv')
dataset.head()

X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

###　サーキットラン, 訓練用データセットと、テスト用データセットへの分割
from sklearn.model_selection import train_test_split
# テスト用データ 1/3
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

### 訓練用データを使った学習開始
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
# 学習をさせる。　切片と係数を求める。　fit で最小二乗法
regressor.fit(X_train, y_train)

# predict メソッドで、Y の値（年収を求める）
y_pred = regressor.predict(X_test)
y_pred

### グラフで表示
plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('Salary vs Experience (Training set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()


# テストデータを使って、グラフに表示
plt.scatter(X_test, y_test, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('Salary vs Experience (Test set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()