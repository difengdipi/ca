import gradio as gr
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_user_recommendations(user_id, rating_matrix, user_similarity, df, k=5):
    """为指定用户生成推荐，并展示菜品详细信息。"""
    user_index = user_id - 1001
    similar_users_indices = user_similarity[user_index].argsort()[::-1][1:k + 1]

    recommended_items = []
    for item_id in rating_matrix.columns:
        if rating_matrix.loc[user_id, item_id] == 0:
            predicted_rating = 0
            similarity_sum = 0
            for neighbor_index in similar_users_indices:
                neighbor_user_id = neighbor_index + 1001
                similarity = user_similarity[user_index, neighbor_index]
                neighbor_rating = rating_matrix.loc[neighbor_user_id, item_id]
                if neighbor_rating > 0:
                    predicted_rating += similarity * neighbor_rating
                    similarity_sum += similarity
            if similarity_sum > 0:
                predicted_rating /= similarity_sum
                recommended_items.append((item_id, predicted_rating))

    recommended_items.sort(key=lambda x: x[1], reverse=True)

    detailed_recommendations = []
    for item_id, predicted_rating in recommended_items:
        item_details = df[df['菜品'] == item_id].iloc[0].to_dict()
        detailed_recommendations.append({
            '菜品ID': item_id,
            '预测评分': predicted_rating,
            '菜品类型': item_details['菜品类型'],
            '口味_辣': item_details['口味_辣'],
            '口味_甜': item_details['口味_甜'],
            '口味_酸': item_details['口味_酸'],
            '口味_清淡': item_details['口味_清淡'],
            '主要食材': item_details['主要食材'],
            '价格': item_details['价格'],
            '健康程度': item_details['健康程度']
        })

    return detailed_recommendations

def generate_recommendations(user_id):
    """生成推荐结果并返回美化后的HTML。"""
    try:
        user_id = int(user_id)  # 确保用户ID是整数
    except ValueError:
        return "<p style='color: red;'>请输入有效的用户ID（整数）。</p>"

    try:
        df = pd.read_csv('data.csv')
    except FileNotFoundError:
        return "<p style='color: red;'>错误：找不到 data.csv 文件。</p>"

    rating_matrix = df.pivot_table(index='用户', columns='菜品', values='评分').fillna(0)
    user_similarity = cosine_similarity(rating_matrix)
    recommendations = get_user_recommendations(user_id, rating_matrix, user_similarity, df)

    if not recommendations:
        return "<p>没有找到推荐结果。</p>"

    html = "<h3>推荐菜品：</h3><table style='width: 100%; border-collapse: collapse;'>"
    html += "<tr><th>菜品ID</th><th>预测评分</th><th>菜品类型</th><th>主要食材</th><th>价格</th><th>健康程度</th></tr>"
    for item in recommendations:
        html += f"<tr><td>{item['菜品ID']}</td><td>{item['预测评分']:.2f}</td><td>{item['菜品类型']}</td><td>{item['主要食材']}</td><td>{item['价格']}</td><td>{item['健康程度']}</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    css = """
    table, th, td {
      border: 1px solid black;
      padding: 8px;
      text-align: left;
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    body {
      font-family: sans-serif;
      padding: 20px;
    }
    """

    with gr.Blocks(css=css) as iface:
        gr.Markdown("## 校园食堂菜品推荐系统")
        with gr.Row():
            user_id_input = gr.Textbox(lines=1, placeholder="输入用户ID")
        with gr.Row():
            recommend_button = gr.Button("生成推荐")
        with gr.Row():
            output_html = gr.HTML()

        recommend_button.click(fn=generate_recommendations, inputs=user_id_input, outputs=output_html)

    iface.launch()