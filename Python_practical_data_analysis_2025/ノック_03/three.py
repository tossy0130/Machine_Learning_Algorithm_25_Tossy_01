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

# 顧客データの整形
customer_join = pd.merge(customer, class_master, on="class", how="left")
customer_join = pd.merge(customer_join, campaign_master, on="campaign_id", how="left")
customer_join.head()

print(len(customer))
print(len(customer_join))

# 欠損値の確認
customer_join.isnull().sum()

# データ毎で count
customer_join.groupby("class_name_x").count()["customer_id"]
customer_join.groupby("campaign_name_x").count()["customer_id"]
customer_join.groupby("gender").count()["customer_id"]
customer_join.groupby("is_deleted").count()["customer_id"]
#customer_join.head()