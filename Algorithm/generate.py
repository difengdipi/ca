import pandas as pd
import numpy as np

np.random.seed(42)

num_users = 500
num_items = 20
num_ratings = 5000

users = np.random.randint(1001, 1001 + num_users, num_ratings)
items = np.random.randint(1, num_items + 1, num_ratings)
ratings = np.random.randint(1, 6, num_ratings)

# 用户特征
user_ages = np.random.choice(['18-22', '23-27', '28-35'], num_users)
user_genders = np.random.choice(['男', '女'], num_users)
user_taste_preferences = np.round(np.random.rand(num_users, 4), 2)  # 保留两位小数
user_dietary_habits = np.random.choice(['素食', '荤素搭配', '无特殊要求'], num_users)
user_consumption_levels = np.random.choice(['高', '中', '低'], num_users)

user_df = pd.DataFrame({
    '用户ID': range(1001, 1001 + num_users),
    '年龄': user_ages,
    '性别': user_genders,
    '口味偏好_辣': user_taste_preferences[:, 0],
    '口味偏好_甜': user_taste_preferences[:, 1],
    '口味偏好_酸': user_taste_preferences[:, 2],
    '口味偏好_清淡': user_taste_preferences[:, 3],
    '饮食习惯': user_dietary_habits,
    '消费能力': user_consumption_levels
})

# 菜品特征
item_types = np.random.choice(['主食', '炒菜', '汤', '小吃'], num_items)
item_tastes = np.round(np.random.rand(num_items, 4), 2)  # 保留两位小数
item_main_ingredients = np.random.choice(['鸡肉', '猪肉', '牛肉', '蔬菜', '面食'], num_items)
item_prices = np.random.randint(5, 20, num_items)
item_health_levels = np.random.choice(['健康', '一般', '不健康'], num_items)

item_df = pd.DataFrame({
    '菜品ID': range(1, num_items + 1),
    '菜品类型': item_types,
    '口味_辣': item_tastes[:, 0],
    '口味_甜': item_tastes[:, 1],
    '口味_酸': item_tastes[:, 2],
    '口味_清淡': item_tastes[:, 3],
    '主要食材': item_main_ingredients,
    '价格': item_prices,
    '健康程度': item_health_levels
})

df = pd.DataFrame({'用户': users, '菜品': items, '评分': ratings})
df = pd.merge(df, user_df, left_on='用户', right_on='用户ID').drop('用户ID', axis=1)
df = pd.merge(df, item_df, left_on='菜品', right_on='菜品ID').drop('菜品ID', axis=1)

# 应用关联规则
for index, row in df.iterrows():
    user_age = row['年龄']
    user_gender = row['性别']
    user_dietary_habit = row['饮食习惯']
    user_consumption_level = row['消费能力']
    item_main_ingredient = row['主要食材']
    item_price = row['价格']
    item_taste_preferences = np.array([row['口味_辣'],row['口味_甜'],row['口味_酸'],row['口味_清淡']])
    user_taste_preferences_user = np.array([row['口味偏好_辣'],row['口味偏好_甜'],row['口味偏好_酸'],row['口味偏好_清淡']])

    # 年龄与饮食习惯
    if user_age == '18-22' and user_dietary_habit == '素食':
        df.loc[index, '饮食习惯'] = np.random.choice(['荤素搭配', '无特殊要求'])
    elif user_age == '28-35' and user_dietary_habit != '素食':
        df.loc[index, '饮食习惯'] = '素食'

    # 性别与口味偏好（简化示例）
    if user_gender == '男' and row['口味偏好_甜'] > 0.5:
        df.loc[index, '口味偏好_甜'] = np.round(np.random.rand() * 0.5, 2)
    elif user_gender == '女' and row['口味偏好_辣'] > 0.5:
        df.loc[index, '口味偏好_辣'] = np.round(np.random.rand() * 0.5, 2)

    # 饮食习惯与主要食材
    if user_dietary_habit == '素食' and item_main_ingredient not in ['蔬菜', '面食']:
        df.loc[index, '主要食材'] = np.random.choice(['蔬菜', '面食'])
        df.loc[index, '评分'] = np.random.randint(4, 6) #素食用户对于素食菜品给予更高分数。
    # 消费能力与价格（简化示例）
    if user_consumption_level == '高' and item_price < 10:
        df.loc[index, '价格'] = np.random.randint(10, 20)
    elif user_consumption_level == '低' and item_price > 15:
        df.loc[index, '价格'] = np.random.randint(5, 15)
    #口味匹配
    taste_score = np.dot(user_taste_preferences_user,item_taste_preferences)
    df.loc[index,'评分'] = np.clip(np.round(row['评分'] + taste_score,2),1,5)

# 保存为 CSV 文件
df.to_csv('campus_food_ratings.csv', index=False)

print("数据已保存到 campus_food_ratings.csv")