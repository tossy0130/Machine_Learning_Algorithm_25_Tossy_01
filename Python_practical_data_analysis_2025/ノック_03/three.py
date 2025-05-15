############################### ノック 21 -30
import pandas as pd
uselog = pd.read_csv("use_log.csv")
print(len(uselog))
uselog.head()

customer = pd.read_csv("customer_join.csv")
print(len(customer))
customer.head()

class_master = pd.read_csv("class_master.csv")
print(len(class_master))
class_master.head()

campaign_master = pd.read_csv("campaign_master.csv")
print(len(campaign_master))
campaign_master.head()

##### 22: 顧客データの整形
customer_join = pd.merge(customer, class_master, on="class", how="left")
customer_join = pd.merge(customer_join, campaign_master, on="campaign_id", how="left")
customer_join.head()

print(len(customer))
print(len(customer_join))

# 欠損値の確認
customer_join.isnull().sum()

##### 23: 顧客データの基礎集計

# データ毎で count
customer_join.groupby("class_name_x").count()["customer_id"]
customer_join.groupby("campaign_name_x").count()["customer_id"]
customer_join.groupby("gender").count()["customer_id"]
customer_join.groupby("is_deleted").count()["customer_id"]
#customer_join.head()

# 2018-04-01 --- 2019-03-31
customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180401")]
print(len(customer_start))

##### 24: 最新顧客データの基礎集計

# 最新月のユーザのみ絞り込み
customer_join["end_date"] = pd.to_datetime(customer_join["end_date"])
customer_newer = customer_join.loc[(customer_join["end_date"] >= pd.to_datetime("20190331")) | (customer_join["end_date"].isna())]
print(len(customer_newer))
customer_newer["end_date"].unique()

# 会員区分、キャンペーン区分、性別　毎
customer_newer.groupby("class_name_x").count()["customer_id"]
customer_newer.groupby("campaign_name_x").count()["customer_id"]
customer_newer.groupby("gender").count()["customer_id"]

##### 25: 利用履歴データの集計

# 月利用回数を集計したデータの作成
uselog["usedate"] = pd.to_datetime(uselog["usedate"])
uselog["年月"] = uselog["usedate"].dt.strftime("%Y%m")
uselog_months = uselog.groupby(["年月", "customer_id"], as_index=False).count()
# uselog_months = uselog.groupby(["年月", "customer_id"], as_index=True).count()
# uselog_months
uselog_months.rename(columns={"log_id":"count"}, inplace=True)
del uselog_months["usedate"]
uselog_months.head()

# 顧客ごとに絞り込み、　平均値、中央値、最大値、最小値　を集計