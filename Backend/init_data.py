from datetime import datetime
import mysql.connector


def initialize_data():
    # 连接到MySQL数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="system",
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    try:
        # 初始化 Role 表默认数据
        cursor.executemany(
            'INSERT INTO Role (role_name) VALUES (%s)',
            [
                ('商户',),
                ('顾客',),
            ]
        )

        # 初始化 Profile 表默认数据
        cursor.executemany(
            'INSERT INTO Profile (username, name, gender, phone, email, role_id, dept, avatar, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [
                ('admin', '小王', '男', '13333333333', '1333333@qq.com', None, '学校', 'avatars/default.png',
                 'pbkdf2_sha256$720000$QjNMoyOKbcqrdfPk6ltxIZ$paQpZQieBWcUvXvtJa08N/8uUdwYXVGPo/NOfJhvTm8='),
                ('merchant', '王00', '男', '10000000000', '1000000@qq.com', 1, '学校', 'avatars/default.png',
                 'pbkdf2_sha256$720000$QjNMoyOKbcqrdfPk6ltxIZ$paQpZQieBWcUvXvtJa08N/8uUdwYXVGPo/NOfJhvTm8='),
                ('customer', '王11', '男', '11111111111', '1111111@qq.com', 2, '学校', 'avatars/default.png',
                 'pbkdf2_sha256$720000$QjNMoyOKbcqrdfPk6ltxIZ$paQpZQieBWcUvXvtJa08N/8uUdwYXVGPo/NOfJhvTm8='),
            ]
        )

        # 初始化 Canteen 表测试数据
        cursor.execute(
            "INSERT INTO `Canteen` (name, description, address, contact_person, contact_phone, created_at) VALUES (%s, %s, %s, %s, %s, NOW())",
            ('名称1', '描述1', '地址1', '联系人1', '联系电话1'))

        # 初始化 Window 表测试数据
        cursor.execute(
            "INSERT INTO `Window` (canteen_id, name, description, business_hours, contact_person, contact_phone, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
            (1, '名称1', '描述1', '营业时间1', '联系人1', '联系电话1'))

        # 初始化 Dish 表测试数据
        cursor.execute(
            "INSERT INTO `Dish` (window_id, name, description, price, image, stock_quantity, time) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
            (1, '名称1', '描述1', 0.00, None, 16))

        # 初始化 Address 表测试数据
        cursor.execute(
            "INSERT INTO `Address` (user_id, address, phone, is_default, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (1, '地址1', '联系电话1', '默认地址1'))

        conn.commit()
        print('初始化数据完成!')
    except Exception as e:
        conn.rollback()
        print(f"发生错误: {e}")
    finally:
        cursor.close()
        conn.close()


initialize_data()