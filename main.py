import mysql.connector
import pandas as pd
from mysql.connector import Error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request

app = Flask(__name__)

try:
    # Thực hiện kết nối đến MySQL
    connection = mysql.connector.connect(
        host="localhost",
        port=3306,  # Port của MySQL mặc định là 3306
        user="root",
        password="root",
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

finally:
    # Đảm bảo đóng kết nối khi không cần thiết nữa
    if 'connection' in locals() and connection.is_connected():
        # cursor.close()
        connection.close()
        print("Đã đóng kết nối đến MySQL")


features = ['description', 'price']

def combineFeatures(row):
    return str(row['price']) + " " + str(row['description'])

# lấy ra các đặc chưng them cái cột sql
df_sanpham['combinedFeatures'] = df_sanpham.apply(combineFeatures , axis=1)

print(df_sanpham['combinedFeatures'] )

# tạo vector của các cột
tf = TfidfVectorizer()
ftMatrix = tf.fit_transform(df_sanpham['combinedFeatures'])

simiar = cosine_similarity(ftMatrix)

number = 5
@app.route('/api', methods=['GET'])
def get_data():
    ketqua = []
    productid = request.args.get('id')
    productid = int(productid)     

    if productid not in df_sanpham['id'].values:
        return jsonify({{'lỗi':'íd không hợp lệ'}})
    
    indexproduc = df_sanpham[df_sanpham['id'] == productid].index[0]

    simiarProduct = list(enumerate(simiar[indexproduc]))

    print(simiarProduct)

    sortedSimiarProduct = sorted(simiarProduct, key=lambda x: x[1], reverse=True)

    def lay_ten (index):
        return (df_sanpham[df_sanpham.index == index]['title'].values[0])

    for i in range(1, number + 1):
        print(lay_ten(sortedSimiarProduct[i][0]))
        ketqua.append(lay_ten(sortedSimiarProduct[i][0]))

    data = {'san pham goi y':ketqua }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=9999)