# Hướng dẫn sửa lỗi và deploy ứng dụng Streamlit

## Vấn đề
Ứng dụng gặp lỗi khi build trên Streamlit Cloud do không tương thích giữa pandas và Python 3.13.

## Giải pháp
Các file sau đã được tạo để khắc phục lỗi:

### 1. `.python-version`
Chỉ định sử dụng Python 3.11 (phiên bản ổn định với pandas)

### 2. `runtime.txt`
File cấu hình runtime cho Streamlit Cloud

### 3. `requirements.txt`
Danh sách các package với phiên bản tương thích:
- pandas 2.1.x - 2.2.x
- numpy 1.24.x - 1.26.x
- streamlit 1.31.0+
- openpyxl cho hỗ trợ Excel

### 4. `.streamlit/config.toml` (Tùy chọn)
Cấu hình giao diện và server cho ứng dụng

## Cách triển khai

### Bước 1: Upload files lên GitHub
```bash
# Copy 3 file chính vào thư mục dự án của bạn
.python-version
runtime.txt
requirements.txt

# (Tùy chọn) Tạo thư mục .streamlit và copy file config
mkdir .streamlit
cp .streamlit_config.toml .streamlit/config.toml
```

### Bước 2: Commit và Push
```bash
git add .python-version runtime.txt requirements.txt
git add .streamlit/config.toml  # nếu có
git commit -m "Fix pandas compatibility issue with Python 3.13"
git push origin main
```

### Bước 3: Redeploy trên Streamlit Cloud
1. Đăng nhập vào https://streamlit.io/cloud
2. Tìm ứng dụng của bạn
3. Click "Reboot" hoặc đợi auto-deploy
4. Kiểm tra logs để đảm bảo build thành công

## Lưu ý quan trọng

### Nếu bạn có requirements.txt hiện tại:
- **Kiểm tra** các package đang sử dụng trong ứng dụng
- **Thêm vào** file requirements.txt mới (giữ lại các package cần thiết)
- **Chỉ định phiên bản** để tránh xung đột

### Ví dụ requirements.txt đầy đủ hơn:
```txt
streamlit>=1.31.0
pandas>=2.1.0,<2.3.0
numpy>=1.24.0,<2.0.0
openpyxl>=3.1.0
plotly>=5.18.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

## Troubleshooting

### Nếu vẫn gặp lỗi:
1. Kiểm tra logs trên Streamlit Cloud
2. Đảm bảo file `.python-version` ở root directory
3. Xóa cache và rebuild: Settings → Reboot app
4. Kiểm tra không có xung đột version trong requirements.txt

### Liên hệ hỗ trợ:
- Streamlit Community: https://discuss.streamlit.io
- GitHub Issues: Tạo issue trong repository của bạn

## Cấu trúc thư mục đề xuất
```
your-app/
├── .python-version
├── runtime.txt
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── app.py (hoặc tên file chính của bạn)
└── README.md
```
