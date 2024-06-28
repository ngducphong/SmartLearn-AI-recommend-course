Content-based filtering.

chương trình gợi ý sản phẩm:
- Dataframe
- Xử lý ngôn ngữ, tìm và gom các đặc trưng của một sản phẩm (mô tả, giá, thể loại, ...)
- Chuyển đỏi Dataframe thành các vector TF_IDF
- Sử dụng công thức tính độ tương đồng Cosin (dùng thư viện) cho ra out put từ -1 -> 1 (cần gần về 1 thì càng giống)
- lựa ra 5 sản phẩm có độ tương đồng giống nhất

------
dùng thư viện 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tf-idf: 

