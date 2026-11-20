# Bài cuối kỳ - Lập trình Python nâng cao

Có 4 thư mục, mỗi câu gồm `main.py`, `requirements.txt`, `data/` và `output/`.

## Chạy nhanh

1. Cài thư viện: `pip install -r requirements.txt`
2. Tại thư mục gốc, chạy: `python -m http.server 8000`
3. Vào: http://localhost:8000

Cũng có thể mở `index.html` bằng tiện ích **Live Server** của VS Code. Không mở trực tiếp bằng `file://` vì trình duyệt sẽ chặn việc đọc CSV.

## Chạy riêng

- Câu 1: `python Cau_1_Brown/main.py` (xuất video MP4 30 giây, cần ffmpeg)
- Câu 2: `python Cau_2_Co_Phieu/main.py` (biểu đồ)
- Câu 3: `python Cau_3_Hoi_Quy/main.py` (hồi quy)
- Câu 4: `python Cau_4_GDP_Lam_Phat/main.py` (seaborn)

Câu 2 và câu 3 bắt buộc ipywidgets theo đề: mở Jupyter/Colab tại thư mục gốc và chạy `%run Cau_2_Co_Phieu/main.py` hoặc `%run Cau_3_Hoi_Quy/main.py`. Trang web là giao diện trình bày bổ sung, không thay thế widget gốc.

Câu 1 mô phỏng 3 hạt như video mẫu và giữ hạt trong [-5,5] ở cả 3 trục bằng phản xạ. Số khung: 180, FPS: 6, thời lượng: 30 giây. Các tệp gốc do người dùng cung cấp được lưu trong `documents/` để đối chiếu.

Câu 2: CSV không có tiêu đề và không có cột ngày. Mỗi dòng là một phiên; 7 giá trị trong dòng được dùng để tạo một nến thống kê, nên dùng `Phiên 1..365` trên trục ngang. Thân nến biểu diễn Q1–Q3, đường trắng là trung vị, râu nến là giá thấp nhất–cao nhất.

Câu 3: mô hình dùng đúng 18 dòng `health.csv`. Hai biểu đồ đầu thể hiện hồi quy đơn; biểu đồ 3D thể hiện cholesterol là hàm của tuổi và BMI. Dự đoán mang tính minh họa toán học, không dùng chẩn đoán sức khỏe.

## Đưa website lên mạng

Dự án là website tĩnh và có sẵn `render.yaml`, không cần Flask hoặc backend.

### 1. Đưa lên GitHub

Tạo một repository trống trên GitHub, sau đó chạy tại thư mục gốc của bài:

```powershell
git init
git add .
git commit -m "Hoan thanh bai cuoi ky"
git branch -M main
git remote add origin https://github.com/TEN_CUA_BAN/TEN_REPOSITORY.git
git push -u origin main
```

Thay `TEN_CUA_BAN` và `TEN_REPOSITORY` bằng thông tin GitHub thật.

### 2. Kết nối Render

1. Đăng nhập Render bằng GitHub.
2. Chọn **New > Blueprint**.
3. Chọn repository vừa đẩy lên.
4. Render sẽ đọc `render.yaml`; chọn **Deploy Blueprint**.
5. Sau khi deploy xong, mở đường dẫn có dạng `https://...onrender.com`.
