import pandas as pd
import matplotlib.pyplot as plt

# 顧客データ。名前、性別など
customer_master = pd.read_csv('customer_master.csv')
customer_master.head()

# 取り扱っている商品データ。商品名・価格等
itme_master = pd.read_csv('item_master.csv')
itme_master.head()

# 購入明細データ
transaction_1 = pd.read_csv('transaction_1.csv')
transaction_1.head()

# 購入明細の詳細データ
transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')
transaction_detail_1.head()

# 購入明細データ 2
transaction_2 = pd.read_csv('transaction_2.csv')

# concat で結合 （ユニオン）
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
transaction.head()

### 出力
# print(len(transaction_1))
# print(len(transaction_2))
# print(len(transaction))

transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)
transaction_detail.head()

##### 売上データ同士の結合（ジョイン）
join_data = pd.merge(transaction_detail, transaction[["transaction_id","payment_date",
                            "customer_id"]], on="transaction_id", how="left")
join_data.head()

##### マスターデータ 結合（ジョイン）
join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
join_data = pd.merge(join_data, itme_master, on="item_id", how="left")

##### 売上データを作成
join_data["price"] = join_data["quantity"] * join_data["item_price"]
join_data[["quantity", "item_price", "price"]].head()

##### ノック6 データの検算
# print(join_data["price"].sum())
# print(transaction["price"].sum())

##### ノック7 各種統計量を把握

### データの欠損値
join_data.isnull().sum()

### 各種統計量  => describe 数値データの集計
join_data.describe()

##### 2019-02-01 01:36:57 ～　2019-07-31 23:41:380
# print(join_data["payment_date"].min())
# print(join_data["payment_date"].max())

##### 8: 月別でデータを集計

# payment_date 確認
join_data.dtypes

# 年月列の作成。 object型 => datetime型　へ変換
join_data["payment_date"] = pd.to_datetime(join_data["payment_date"]) # datetime へ 変換
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")

join_data[["payment_date", "payment_month"]].head()

# 月別集計
# join_data.groupby("payment_month").sum()["price"]
join_data["price"] = pd.to_numeric(join_data["price"], errors="coerce") # 数値型へ変換
price_sum = join_data.groupby("payment_month")["price"].sum()
# print(price_sum)

##### 9: 月別、商品別でデータ集計

# 月別、かつ商品別集計
# join_data.groupby(["payment_month", "item_name"]).sum()[["price", "quantity"]]
join_data.groupby(["payment_month", "item_name"])[["price", "quantity"]].sum()

# 月別、商品別 price、quantity の集計
pd.pivot_table(join_data, index="item_name", columns="payment_month", values=['price', 'quantity'], aggfunc='sum')

##### 10: 商品別の売上推移を可視化
graph_data = pd.pivot_table(join_data,index='payment_month',columns='item_name',values='price',aggfunc='sum',fill_value=0)  # 欠損値を 0 に

graph_data.head()

%matplotlib inline 
plt.plot(list(graph_data.index), graph_data["PC-A"], label='PC-A')
plt.plot(list(graph_data.index), graph_data["PC-B"], label='PC-B')
plt.plot(list(graph_data.index), graph_data["PC-C"], label='PC-C')
plt.plot(list(graph_data.index), graph_data["PC-D"], label='PC-D')
plt.plot(list(graph_data.index), graph_data["PC-E"], label='PC-E')
plt.legend()

#################################################
##### 11:商品別の売上推移を可視化
#################################################

uriage_data = pd.read_csv('uriage.csv')
uriage_data.head()

kokyaku_data = pd.read_excel('kokyaku_daicho.xlsx')
kokyaku_data.head()

##### 12:データの揺れを見る
# print("12==========")
# 売上履歴
uriage_data["item_name"].head()
# 商品金額
uriage_data["item_price"].head()

##### 13:データに揺れがあるまま集計
# print("13==========")
uriage_data["purchase_date"] = pd.to_datetime(uriage_data["purchase_date"])

uriage_data["purchase_month"] = uriage_data["purchase_date"].dt.strftime("%Y%m")

res = uriage_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# print(res)

##### 14: 商品名の揺れを補正

# ユニーク数の確認
# 出力 99
# print(len(pd.unique(uriage_data["item_name"])))

# データの揺れ（欠損）を解消
uriage_data["item_name"] = uriage_data["item_name"].str.upper() # 小文字を大文字に変換
uriage_data["item_name"] = uriage_data["item_name"].str.replace(" ", "") # 空白除去
uriage_data["item_name"] = uriage_data["item_name"].str.replace("　", "") # 空白除去
uriage_data.sort_values(by=["item_name"], ascending=True)

print(pd.unique(uriage_data["item_name"]))
print(len(pd.unique(uriage_data["item_name"])))

##### 15: 金額欠損値の補完

# データ全体から、欠損値が含まれているか確認
uriage_data.isnull().any(axis=0)

flg_is_null = uriage_data["item_price"].isnull() # 欠損値のある箇所を特定し、変数にどの行に欠損値が存在するか保持

# .loc 関数は、条件を付与して、それに合致するデータを抽出する事ができる。
for trg in list(uriage_data.loc[flg_is_null, "item_name"].unique()) : 
  price = uriage_data.loc[(~flg_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
  uriage_data.loc[(flg_is_null) & (uriage_data["item_name"] == trg), "item_price"] = price

uriage_data.head()

# 欠損値が含まれているか確認
uriage_data.isnull().any(axis=0)

### 各商品の金額が正しく補完されたか確認
for trg in list(uriage_data["item_name"].sort_values().unique()) :
  print(trg + "の最大額:" + str(uriage_data.loc[uriage_data["item_name"] == trg]["item_price"].max()) +  
  "の最小額:" + str(uriage_data.loc[uriage_data["item_name"] == trg]["item_price"].min(skipna=False)))

