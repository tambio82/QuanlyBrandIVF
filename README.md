# IVF Product Catalog - Hướng dẫn chi tiết

## 📋 MỤC LỤC
1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt](#cài-đặt)
3. [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
4. [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
5. [Thu thập dữ liệu](#thu-thập-dữ-liệu)
6. [Mở rộng](#mở-rộng)

---

## 🎯 GIỚI THIỆU

Website IVF Product Catalog là hệ thống quản lý và tra cứu thông tin sản phẩm IVF từ các nhà sản xuất toàn cầu. Hệ thống giúp:
- Tổng hợp thông tin sản phẩm từ nhiều nguồn
- Tìm kiếm và so sánh sản phẩm dễ dàng
- Quản lý thông tin công ty và nhà phân phối
- Phân tích thị trường và xu hướng

---

## 🔧 CÀI ĐẶT

### Bước 1: Cài đặt Python
```bash
# Kiểm tra phiên bản Python (yêu cầu >= 3.8)
python --version

# Nếu chưa có, tải về từ: https://www.python.org/downloads/
```

### Bước 2: Cài đặt các thư viện cần thiết
```bash
pip install streamlit pandas openpyxl
```

### Bước 3: Chạy ứng dụng
```bash
streamlit run ivf_product_catalog.py
```

Ứng dụng sẽ mở tự động trên trình duyệt tại: http://localhost:8501

---

## 📊 CẤU TRÚC DỮ LIỆU

### 1. Bảng COMPANIES (Công ty)

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|--------|------|----------|-------|-------|
| company_id | TEXT | ✅ | ID duy nhất | KTZ001 |
| company_name | TEXT | ✅ | Tên công ty | Kitazato Corporation |
| country | TEXT | ✅ | Quốc gia | Japan |
| headquarters_address | TEXT | ❌ | Địa chỉ trụ sở | Shizuoka, Japan |
| website | TEXT | ❌ | Website | https://www.kitazato.co.jp |
| contact_email | TEXT | ❌ | Email | info@kitazato.co.jp |
| contact_phone | TEXT | ❌ | Số điện thoại | +81-3-3434-1653 |
| year_established | INTEGER | ❌ | Năm thành lập | 1996 |
| certifications | TEXT | ❌ | Chứng nhận | ISO 13485, CE, FDA |
| description | TEXT | ❌ | Mô tả công ty | Leading Japanese company... |
| logo_url | TEXT | ❌ | URL logo | https://... |
| created_date | TEXT | ✅ | Ngày tạo | 2024-10-31T10:00:00 |
| updated_date | TEXT | ✅ | Ngày cập nhật | 2024-10-31T10:00:00 |

### 2. Bảng PRODUCTS (Sản phẩm)

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|--------|------|----------|-------|-------|
| product_id | TEXT | ✅ | ID sản phẩm | PRD001 |
| product_name | TEXT | ✅ | Tên sản phẩm | Cryotop® Open System |
| company_id | TEXT | ✅ | ID công ty | KTZ001 |
| product_code | TEXT | ❌ | Mã sản phẩm/SKU | CT-001 |
| category | TEXT | ✅ | Danh mục chính | Devices |
| subcategory | TEXT | ✅ | Danh mục phụ | Vitrification Device |
| description | TEXT | ❌ | Mô tả chi tiết | Revolutionary device... |
| specifications | TEXT | ❌ | Thông số kỹ thuật | Cooling speed: -23,000°C/min |
| application_areas | TEXT | ❌ | Lĩnh vực ứng dụng | Vitrification, Embryo Culture |
| package_size | TEXT | ❌ | Quy cách đóng gói | 20 pieces/box |
| unit | TEXT | ❌ | Đơn vị | piece, ml, kit |
| storage_conditions | TEXT | ❌ | Điều kiện bảo quản | 2-8°C, Room temperature |
| shelf_life | TEXT | ❌ | Hạn sử dụng | 24 months, 5 years |
| composition | TEXT | ❌ | Thành phần | Polystyrene, Synthetic media |
| list_price | REAL | ❌ | Giá niêm yết | 120.00 |
| currency | TEXT | ❌ | Đơn vị tiền tệ | USD, EUR, VND |
| availability_status | TEXT | ❌ | Tình trạng | Available, Out of Stock |
| distributor_vietnam | TEXT | ❌ | Nhà phân phối VN | ABC Company |
| special_features | TEXT | ❌ | Tính năng đặc biệt | Ultra-rapid cooling |
| advantages | TEXT | ❌ | Ưu điểm | Market leader, High survival |
| rating | REAL | ❌ | Đánh giá (1-5) | 4.8 |
| product_image_url | TEXT | ❌ | URL hình ảnh | https://... |
| brochure_url | TEXT | ❌ | URL brochure | https://... |
| created_date | TEXT | ✅ | Ngày tạo | 2024-10-31T10:00:00 |
| updated_date | TEXT | ✅ | Ngày cập nhật | 2024-10-31T10:00:00 |
| status | TEXT | ✅ | Trạng thái | Active, Inactive, Draft |

### 3. Danh mục Categories

**Equipment (Thiết bị):**
- Incubator (Tủ ấm)
- Microscope (Kính hiển vi)
- Workstation (Trạm làm việc)
- Centrifuge (Máy ly tâm)
- Analyzer (Máy phân tích)
- Imaging System (Hệ thống hình ảnh)

**Consumables (Vật tư tiêu hao):**
- Needles (Kim)
- Catheters (Catheter)
- Pipettes (Pipette)
- Dishes (Đĩa)
- Plates (Plate)
- Tubes (Ống)
- Syringes (Ống tiêm)

**Media (Môi trường):**
- Culture Medium (Môi trường nuôi cấy)
- Vitrification Medium (Môi trường đông lạnh)
- Thawing Medium (Môi trường rã đông)
- Sperm Processing Medium (Môi trường xử lý tinh trùng)
- Buffers (Dung dịch đệm)

**Chemicals (Hóa chất):**
- Enzymes (Enzyme)
- Oils (Dầu)
- Reagents (Thuốc thử)
- Supplements (Chất bổ sung)
- Indicators (Chất chỉ thị)

**Devices (Dụng cụ y tế):**
- Vitrification Device (Dụng cụ đông lạnh)
- Transfer Device (Dụng cụ chuyển)
- Biopsy Device (Dụng cụ sinh thiết)
- Injection Device (Dụng cụ tiêm)

**Software/AI (Phần mềm):**
- Embryo Selection (Chọn phôi)
- Sperm Analysis (Phân tích tinh trùng)
- Lab Management (Quản lý phòng lab)
- Data Analysis (Phân tích dữ liệu)

### 4. Lĩnh vực ứng dụng (Application Areas)

1. **Oocyte Retrieval** - Thu nhận noãn
2. **ICSI** - Tiêm tinh trùng vào bào tương
3. **C-IVF** - Thụ tinh thông thường
4. **Embryo Culture** - Nuôi cấy phôi
5. **Vitrification** - Đông lạnh thủy tinh hóa
6. **Embryo Transfer** - Cấy phôi
7. **IUI** - Thụ tinh nhân tạo trong tử cung
8. **Andrology** - Xử lý tinh trùng
9. **IVM** - Trưởng thành noãn trong ống nghiệm
10. **PGT** - Sinh thiết phôi để chẩn đoán di truyền
11. **Evaluation** - Đánh giá và quan sát

---

## 📖 HƯỚNG DẪN SỬ DỤNG

### 1. Trang chủ (Home)
- Hiển thị tổng quan thống kê: số công ty, sản phẩm, danh mục
- Danh sách các category với subcategories
- Dashboard nhanh về hệ thống

### 2. Tìm kiếm sản phẩm (Search)
**Các bộ lọc:**
- Từ khóa: Tìm theo tên, mã sản phẩm, mô tả
- Danh mục: Lọc theo category
- Công ty: Lọc theo nhà sản xuất
- Lĩnh vực ứng dụng: Chọn nhiều lĩnh vực
- Tình trạng: Available, Out of Stock, Discontinued

**Kết quả:**
- Hiển thị dạng card với thông tin chính
- Nút "Chi tiết" để xem đầy đủ thông tin
- Có thể export kết quả tìm kiếm

### 3. Danh sách công ty (Companies)
- Xem tất cả công ty trong database
- Thông tin chi tiết từng công ty
- Số lượng sản phẩm của từng công ty

### 4. Thêm sản phẩm (Add Product)
**Form nhập liệu:**
- Các trường bắt buộc đánh dấu (*)
- Dropdown cho category, subcategory
- Multi-select cho application areas
- Validation tự động

**Quy trình:**
1. Điền thông tin cơ bản (ID, tên, công ty)
2. Chọn danh mục và phân loại
3. Nhập mô tả và thông số kỹ thuật
4. Thêm thông tin giá và tình trạng
5. Nhấn "Lưu sản phẩm"

### 5. Thêm công ty (Add Company)
**Thông tin cần nhập:**
- ID công ty (duy nhất)
- Tên công ty
- Quốc gia
- Thông tin liên hệ
- Chứng nhận và mô tả

### 6. Import/Export
**Import:**
- Hỗ trợ CSV và Excel
- Template có sẵn để download
- Validation dữ liệu trước khi import
- Hiển thị preview trước khi lưu

**Export:**
- Export toàn bộ hoặc theo bộ lọc
- Định dạng CSV hoặc Excel
- Tên file tự động theo ngày

### 7. Thống kê (Statistics)
**Các biểu đồ:**
- Sản phẩm theo danh mục (bar chart)
- Sản phẩm theo công ty (bar chart)
- Công ty theo quốc gia (bar chart)
- Xu hướng thời gian (line chart - nếu có)

---

## 🔍 THU THẬP DỮ LIỆU

### Phương pháp thu thập

#### 1. Từ Website chính thức
**Các công ty lớn:**
- Kitazato: https://www.kitazato.co.jp/en/products/
- Vitrolife: https://www.vitrolife.com/
- Irvine Scientific: https://www.irvinesci.com/
- Cooper Surgical: https://www.coopersurgical.com/
- Fujifilm Irvine Scientific
- LifeGlobal Group
- Origio (Cooper Surgical)

**Thông tin cần lấy:**
- Catalog sản phẩm (PDF/online)
- Brochure kỹ thuật
- Thông tin công ty
- Giá (nếu công khai)

**Công cụ:**
- Web scraping (BeautifulSoup, Selenium)
- PDF parsing (PyPDF2, pdfplumber)
- Manual data entry

#### 2. Từ nhà phân phối
**Liên hệ:**
- Gửi email yêu cầu catalog
- Gọi điện xin thông tin sản phẩm
- Tham dự hội thảo, triển lãm

**Thông tin thu thập:**
- Giá bán tại thị trường Việt Nam
- Điều kiện mua hàng
- Dịch vụ hậu mãi
- Tình trạng hàng

#### 3. Từ tài liệu khoa học
**Nguồn:**
- PubMed
- Google Scholar
- Reproductive BioMedicine Online
- Fertility and Sterility

**Thông tin:**
- Bằng chứng lâm sàng
- So sánh sản phẩm
- Tỷ lệ thành công
- User reviews

#### 4. Từ cộng đồng chuyên gia
**Kênh:**
- ESHRE (European Society of Human Reproduction and Embryology)
- ASRM (American Society for Reproductive Medicine)
- Facebook groups
- LinkedIn

**Thu thập:**
- Đánh giá từ người dùng
- Kinh nghiệm thực tế
- Vấn đề thường gặp
- Tips & tricks

### Checklist thu thập dữ liệu

**Cho mỗi sản phẩm:**
```
□ Thông tin cơ bản (tên, mã, công ty)
□ Phân loại (category, subcategory)
□ Mô tả chi tiết
□ Thông số kỹ thuật
□ Lĩnh vực ứng dụng
□ Quy cách đóng gói
□ Điều kiện bảo quản
□ Giá niêm yết (nếu có)
□ Tình trạng sẵn có
□ Hình ảnh sản phẩm
□ Brochure/manual
□ Nhà phân phối VN
□ Đánh giá/review
```

**Cho mỗi công ty:**
```
□ Tên công ty
□ Quốc gia
□ Năm thành lập
□ Website
□ Thông tin liên hệ
□ Chứng nhận (ISO, CE, FDA)
□ Mô tả về công ty
□ Logo
□ Danh sách sản phẩm chính
```

### Template Excel để Import

**Sheet 1: Companies**
| company_id | company_name | country | website | contact_email | year_established | certifications |
|-----------|--------------|---------|---------|---------------|------------------|----------------|
| KTZ001 | Kitazato Corp | Japan | www... | info@... | 1996 | ISO,CE,FDA |

**Sheet 2: Products**
| product_id | product_name | company_id | category | subcategory | price | currency |
|-----------|--------------|-----------|----------|-------------|-------|----------|
| PRD001 | Cryotop | KTZ001 | Devices | Vitrification | 120 | USD |

---

## 🚀 MỞ RỘNG

### Tính năng nâng cao có thể thêm:

#### 1. User Authentication
```python
import streamlit_authenticator as stauth
# Phân quyền: Admin, Editor, Viewer
```

#### 2. So sánh sản phẩm
- Chọn nhiều sản phẩm để so sánh
- Bảng so sánh side-by-side
- Highlight điểm khác biệt

#### 3. Review & Rating
- Người dùng đánh giá sản phẩm
- Comment và feedback
- Star rating system

#### 4. Price tracking
- Lưu lịch sử giá
- Biểu đồ biến động giá
- Cảnh báo giá tốt

#### 5. Advanced Search
- Full-text search
- Fuzzy matching
- Search suggestions

#### 6. Export PDF Report
- Tạo báo cáo so sánh
- Catalog theo danh mục
- Company profile

#### 7. API Integration
- REST API để truy vấn
- Webhook notifications
- Third-party integrations

#### 8. Multi-language
- Tiếng Việt
- English
- 日本語

#### 9. Mobile App
- React Native
- Flutter
- Progressive Web App

#### 10. AI Features
- Chatbot tư vấn sản phẩm
- Recommendation system
- Auto-categorization

---

## 📞 HỖ TRỢ

### Contact
- Email: support@ivfcatalog.com
- GitHub: https://github.com/username/ivf-catalog
- Documentation: https://docs.ivfcatalog.com

### Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### License
MIT License - See LICENSE file for details

---

## 📝 CHANGELOG

### Version 1.0.0 (2024-10-31)
- Initial release
- Basic CRUD operations
- Search and filter
- Import/Export CSV
- Statistics dashboard

### Roadmap
- v1.1: User authentication
- v1.2: Product comparison
- v1.3: Price tracking
- v2.0: Mobile app

---

**Happy cataloging! 🎉**
