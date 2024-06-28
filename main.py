import mysql.connector
import pandas as pd
from mysql.connector import Error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

try:
    # Thực hiện kết nối đến MySQL
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,  # Port của MySQL mặc định là 3306
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database="db_elearning_doan"
    )

    # Kiểm tra xem kết nối đã thành công chưa
    if connection.is_connected():
        print("Kết nối thành công đến MySQL")

        query = "SELECT * FROM course"
        df_sanpham = pd.read_sql(query, connection)

        # In kết quả ra màn hình
        print(df_sanpham.head())

except Error as e: 
    print(f"Lỗi: {e}")
    df_sanpham = pd.DataFrame()  # Đặt DataFrame rỗng nếu kết nối thất bại

finally:
    # Đảm bảo đóng kết nối khi không cần thiết nữa
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Đã đóng kết nối đến MySQL")

if not df_sanpham.empty:
    features = ['description', 'price']

    def combineFeatures(row):
        return str(row['price']) + " " + str(row['description'])

    # Lấy ra các đặc chưng thêm cột SQL
    df_sanpham['combinedFeatures'] = df_sanpham.apply(combineFeatures, axis=1)
    
    # Tạo vector của các cột
    tf = TfidfVectorizer()
    ftMatrix = tf.fit_transform(df_sanpham['combinedFeatures'])
    
    simiar = cosine_similarity(ftMatrix)

@app.route('/api', methods=['GET'])
def get_data():
    if df_sanpham.empty:
        return jsonify({'error': 'Không thể kết nối đến cơ sở dữ liệu'}), 500
    
    ketqua = []
    productid = request.args.get('id')
    number = request.args.get('number', default=5, type=int)  # Thêm tham số number với giá trị mặc định là 5
    
    if not productid:
        return jsonify({'lỗi': 'Thiếu tham số id'}), 400
    
    try:
        productid = int(productid)
    except ValueError:
        return jsonify({'lỗi': 'id phải là một số nguyên'}), 400

    if productid not in df_sanpham['id'].values:
        return jsonify({'lỗi': 'id không hợp lệ'}), 404
    
    indexproduc = df_sanpham[df_sanpham['id'] == productid].index[0]
    simiarProduct = list(enumerate(simiar[indexproduc]))
    sortedSimiarProduct = sorted(simiarProduct, key=lambda x: x[1], reverse=True)

    def lay_id(index):
        return int(df_sanpham[df_sanpham.index == index]['id'].values[0])

    for i in range(1, min(number + 1, len(sortedSimiarProduct))):
        ketqua.append(lay_id(sortedSimiarProduct[i][0]))

    data = {'data': ketqua}
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=9999)
