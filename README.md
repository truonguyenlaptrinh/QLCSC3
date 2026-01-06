# App Đăng ký thăm chiến sĩ

Ứng dụng đăng ký thăm chiến sĩ được xây dựng bằng Streamlit.

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở trong trình duyệt tại địa chỉ `http://localhost:8501`

## Tính năng

- ✅ Form đăng ký với 4 trường:
  - Họ và tên người đăng ký
  - Họ và tên chiến sĩ
  - Đơn vị
  - Thời gian (ngày và giờ)
- ✅ Lưu trữ dữ liệu vào file CSV
- ✅ Hiển thị danh sách đăng ký
- ✅ Thống kê số liệu
- ✅ Xóa dữ liệu

## Dữ liệu

Dữ liệu được lưu trong file `dang_ky_tham.csv` trong cùng thư mục với ứng dụng.

## Thêm ảnh nền

Ứng dụng hỗ trợ thêm ảnh nền. Để thêm ảnh nền:

1. **Sử dụng file ảnh trong thư mục dự án:**
   - Đặt file ảnh (ví dụ: `background.jpg`) vào thư mục dự án
   - Trong file `app.py`, tìm dòng có comment về ảnh nền
   - Bỏ comment và điền tên file:
   ```python
   set_background_image(image_path="background.jpg", opacity=0.1)
   ```

2. **Sử dụng URL ảnh:**
   - Trong file `app.py`, bỏ comment và điền URL:
   ```python
   set_background_image(image_url="https://example.com/background.jpg", opacity=0.1)
   ```

   - `opacity`: Độ trong suốt của ảnh nền (0.0 - 1.0), giá trị càng nhỏ ảnh càng trong suốt

