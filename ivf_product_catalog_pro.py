import streamlit as st
import pandas as pd
import json
from datetime import datetime
import sqlite3
import os

# Cấu hình trang
st.set_page_config(
    page_title="IVF Product Catalog Pro",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
    }
    .category-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: white;
    }
    .stat-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    .stTextArea textarea {
        min-height: 100px;
    }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo database SQLite với schema mở rộng
def init_database():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    
    # Bảng Companies (không thay đổi)
    c.execute('''CREATE TABLE IF NOT EXISTS companies
                 (company_id TEXT PRIMARY KEY,
                  company_name TEXT NOT NULL,
                  country TEXT,
                  headquarters_address TEXT,
                  website TEXT,
                  contact_email TEXT,
                  contact_phone TEXT,
                  year_established INTEGER,
                  certifications TEXT,
                  description TEXT,
                  logo_url TEXT,
                  created_date TEXT,
                  updated_date TEXT)''')
    
    # Bảng Products với các trường mới
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (product_id TEXT PRIMARY KEY,
                  product_name TEXT NOT NULL,
                  company_id TEXT,
                  product_code TEXT,
                  category TEXT,
                  subcategory TEXT,
                  description TEXT,
                  specifications TEXT,
                  application_areas TEXT,
                  package_size TEXT,
                  unit TEXT,
                  storage_conditions TEXT,
                  shelf_life TEXT,
                  composition TEXT,
                  list_price REAL,
                  currency TEXT,
                  availability_status TEXT,
                  distributor_vietnam TEXT,
                  special_features TEXT,
                  advantages TEXT,
                  rating REAL,
                  product_image_url TEXT,
                  brochure_url TEXT,
                  strengths TEXT,
                  weaknesses TEXT,
                  qa_qc_certifications TEXT,
                  validation_evidence TEXT,
                  expert_review_1 TEXT,
                  expert_review_2 TEXT,
                  expert_review_3 TEXT,
                  created_date TEXT,
                  updated_date TEXT,
                  status TEXT,
                  FOREIGN KEY (company_id) REFERENCES companies (company_id))''')
    
    # Bảng Categories - quản lý danh mục
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category_name TEXT UNIQUE NOT NULL,
                  description TEXT,
                  created_date TEXT,
                  is_active INTEGER DEFAULT 1)''')
    
    # Bảng Subcategories - quản lý danh mục phụ
    c.execute('''CREATE TABLE IF NOT EXISTS subcategories
                 (subcategory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category_name TEXT NOT NULL,
                  subcategory_name TEXT NOT NULL,
                  description TEXT,
                  created_date TEXT,
                  is_active INTEGER DEFAULT 1,
                  UNIQUE(category_name, subcategory_name))''')
    
    # Bảng Application Areas - quản lý lĩnh vực ứng dụng
    c.execute('''CREATE TABLE IF NOT EXISTS application_areas
                 (area_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  area_name TEXT UNIQUE NOT NULL,
                  description TEXT,
                  created_date TEXT,
                  is_active INTEGER DEFAULT 1)''')
    
    # Bảng Currencies - quản lý đơn vị tiền tệ
    c.execute('''CREATE TABLE IF NOT EXISTS currencies
                 (currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  currency_code TEXT UNIQUE NOT NULL,
                  currency_name TEXT,
                  symbol TEXT,
                  created_date TEXT,
                  is_active INTEGER DEFAULT 1)''')
    
    # Bảng Status Options - quản lý tình trạng
    c.execute('''CREATE TABLE IF NOT EXISTS status_options
                 (status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  status_name TEXT UNIQUE NOT NULL,
                  description TEXT,
                  created_date TEXT,
                  is_active INTEGER DEFAULT 1)''')
    
    conn.commit()
    conn.close()

# Hàm thêm dữ liệu mặc định
def add_default_data():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    
    # Kiểm tra và thêm categories mặc định
    c.execute("SELECT COUNT(*) FROM categories")
    if c.fetchone()[0] == 0:
        default_categories = [
            ('Equipment', 'Thiết bị y tế IVF'),
            ('Consumables', 'Vật tư tiêu hao'),
            ('Media', 'Môi trường nuôi cấy'),
            ('Chemicals', 'Hóa chất'),
            ('Devices', 'Dụng cụ y tế'),
            ('Software/AI', 'Phần mềm và AI')
        ]
        for cat, desc in default_categories:
            c.execute("INSERT INTO categories (category_name, description, created_date) VALUES (?, ?, ?)",
                     (cat, desc, datetime.now().isoformat()))
    
    # Thêm subcategories mặc định
    c.execute("SELECT COUNT(*) FROM subcategories")
    if c.fetchone()[0] == 0:
        default_subcategories = [
            ('Equipment', 'Incubator', 'Tủ ấm'),
            ('Equipment', 'Microscope', 'Kính hiển vi'),
            ('Equipment', 'Workstation', 'Trạm làm việc'),
            ('Equipment', 'Centrifuge', 'Máy ly tâm'),
            ('Consumables', 'Needles', 'Kim'),
            ('Consumables', 'Catheters', 'Catheter'),
            ('Consumables', 'Pipettes', 'Pipette'),
            ('Consumables', 'Dishes', 'Đĩa'),
            ('Consumables', 'Plates', 'Plate'),
            ('Media', 'Culture Medium', 'Môi trường nuôi cấy'),
            ('Media', 'Vitrification Medium', 'Môi trường đông lạnh'),
            ('Media', 'Thawing Medium', 'Môi trường rã đông'),
            ('Chemicals', 'Enzymes', 'Enzyme'),
            ('Chemicals', 'Oils', 'Dầu'),
            ('Devices', 'Vitrification Device', 'Dụng cụ đông lạnh'),
            ('Devices', 'Transfer Device', 'Dụng cụ chuyển'),
            ('Software/AI', 'Embryo Selection', 'Chọn phôi'),
            ('Software/AI', 'Sperm Analysis', 'Phân tích tinh trùng')
        ]
        for cat, subcat, desc in default_subcategories:
            c.execute("INSERT INTO subcategories (category_name, subcategory_name, description, created_date) VALUES (?, ?, ?, ?)",
                     (cat, subcat, desc, datetime.now().isoformat()))
    
    # Thêm application areas mặc định
    c.execute("SELECT COUNT(*) FROM application_areas")
    if c.fetchone()[0] == 0:
        default_areas = [
            ('Oocyte Retrieval', 'Thu nhận noãn'),
            ('ICSI', 'Tiêm tinh trùng vào bào tương'),
            ('C-IVF', 'Thụ tinh thông thường'),
            ('Embryo Culture', 'Nuôi cấy phôi'),
            ('Vitrification', 'Đông lạnh thủy tinh hóa'),
            ('Embryo Transfer', 'Cấy phôi'),
            ('IUI', 'Thụ tinh nhân tạo'),
            ('Andrology', 'Xử lý tinh trùng'),
            ('IVM', 'Trưởng thành noãn'),
            ('PGT', 'Sinh thiết phôi'),
            ('Evaluation', 'Đánh giá')
        ]
        for area, desc in default_areas:
            c.execute("INSERT INTO application_areas (area_name, description, created_date) VALUES (?, ?, ?)",
                     (area, desc, datetime.now().isoformat()))
    
    # Thêm currencies mặc định
    c.execute("SELECT COUNT(*) FROM currencies")
    if c.fetchone()[0] == 0:
        default_currencies = [
            ('USD', 'US Dollar', '$'),
            ('EUR', 'Euro', '€'),
            ('VND', 'Vietnamese Dong', '₫'),
            ('JPY', 'Japanese Yen', '¥'),
            ('GBP', 'British Pound', '£')
        ]
        for code, name, symbol in default_currencies:
            c.execute("INSERT INTO currencies (currency_code, currency_name, symbol, created_date) VALUES (?, ?, ?, ?)",
                     (code, name, symbol, datetime.now().isoformat()))
    
    # Thêm status options mặc định
    c.execute("SELECT COUNT(*) FROM status_options")
    if c.fetchone()[0] == 0:
        default_statuses = [
            ('Available', 'Có sẵn hàng'),
            ('Out of Stock', 'Hết hàng'),
            ('Discontinued', 'Ngừng sản xuất'),
            ('Pre-order', 'Đặt hàng trước'),
            ('Coming Soon', 'Sắp ra mắt')
        ]
        for status, desc in default_statuses:
            c.execute("INSERT INTO status_options (status_name, description, created_date) VALUES (?, ?, ?)",
                     (status, desc, datetime.now().isoformat()))
    
    # Thêm dữ liệu mẫu công ty nếu chưa có
    c.execute("SELECT COUNT(*) FROM companies")
    if c.fetchone()[0] == 0:
        sample_companies = [
            ('KTZ001', 'Kitazato Corporation', 'Japan', 'Shizuoka, Japan', 
             'https://www.kitazato.co.jp/en/', 'info@kitazato.co.jp', '+81-3-3434-1653',
             1996, 'ISO 13485, CE, FDA', 'Leading Japanese company in ART products', '', 
             datetime.now().isoformat(), datetime.now().isoformat())
        ]
        c.executemany('''INSERT INTO companies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                      sample_companies)
    
    conn.commit()
    conn.close()

# Hàm lấy danh sách từ database
def get_categories():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT category_name FROM categories WHERE is_active = 1 ORDER BY category_name")
    categories = [row[0] for row in c.fetchall()]
    conn.close()
    return categories

def get_subcategories(category=None):
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    if category:
        c.execute("SELECT subcategory_name FROM subcategories WHERE category_name = ? AND is_active = 1 ORDER BY subcategory_name", (category,))
    else:
        c.execute("SELECT subcategory_name FROM subcategories WHERE is_active = 1 ORDER BY subcategory_name")
    subcategories = [row[0] for row in c.fetchall()]
    conn.close()
    return subcategories

def get_application_areas():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT area_name FROM application_areas WHERE is_active = 1 ORDER BY area_name")
    areas = [row[0] for row in c.fetchall()]
    conn.close()
    return areas

def get_currencies():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT currency_code FROM currencies WHERE is_active = 1 ORDER BY currency_code")
    currencies = [row[0] for row in c.fetchall()]
    conn.close()
    return currencies

def get_status_options():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT status_name FROM status_options WHERE is_active = 1 ORDER BY status_name")
    statuses = [row[0] for row in c.fetchall()]
    conn.close()
    return statuses

def get_company_list():
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT company_name FROM companies ORDER BY company_name")
    companies = [row[0] for row in c.fetchall()]
    conn.close()
    return companies

def get_company_name(company_id):
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT company_name FROM companies WHERE company_id = ?", (company_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "Unknown"

def get_company_id(company_name):
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT company_id FROM companies WHERE company_name = ?", (company_name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Khởi tạo session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=IVF+Catalog+Pro", width=200)
    st.markdown("---")
    
    menu_items = {
        "🏠 Trang chủ": "home",
        "🔍 Tìm kiếm sản phẩm": "search",
        "🏢 Danh sách công ty": "companies",
        "➕ Thêm sản phẩm": "add_product",
        "✏️ Sửa sản phẩm": "edit_product",
        "➕ Thêm công ty": "add_company",
        "⚙️ Quản lý danh mục": "manage_categories",
        "📊 Thống kê": "statistics",
        "📥 Import/Export": "import_export",
        "ℹ️ Hướng dẫn": "guide"
    }
    
    for label, page in menu_items.items():
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page

# Hàm hiển thị trang chủ
def show_home():
    st.markdown('<p class="main-header">🧬 IVF Product Catalog Pro</p>', unsafe_allow_html=True)
    st.markdown("### Hệ thống quản lý thông tin sản phẩm IVF toàn cầu - Phiên bản nâng cao")
    
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM companies")
    total_companies = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM products")
    total_products = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM categories WHERE is_active = 1")
    total_categories = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM application_areas WHERE is_active = 1")
    total_areas = c.fetchone()[0]
    
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <h2>{total_companies}</h2>
                <p>Công ty</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <h2>{total_products}</h2>
                <p>Sản phẩm</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-box">
                <h2>{total_categories}</h2>
                <p>Danh mục</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-box">
                <h2>{total_areas}</h2>
                <p>Ứng dụng</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ✨ Tính năng mới trong phiên bản Pro")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **🆕 Đánh giá chuyên gia:**
        - Điểm mạnh / Điểm yếu
        - Chứng nhận QA/QC
        - Minh chứng Validation
        - Nhận định từ 3 chuyên gia
        """)
    
    with col2:
        st.success("""
        **⚙️ Quản lý linh hoạt:**
        - Tùy chỉnh danh mục
        - Quản lý lĩnh vực ứng dụng
        - Thêm đơn vị tiền tệ
        - Chỉnh sửa tình trạng
        """)

# Hàm tìm kiếm sản phẩm (giữ nguyên)
def show_search():
    st.markdown("## 🔍 Tìm kiếm sản phẩm")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔎 Từ khóa", placeholder="Nhập tên sản phẩm, mã sản phẩm...")
    
    with col2:
        categories = get_categories()
        category_filter = st.selectbox("📁 Danh mục", ["Tất cả"] + categories)
    
    with col3:
        company_filter = st.selectbox("🏢 Công ty", ["Tất cả"] + get_company_list())
    
    col4, col5 = st.columns(2)
    with col4:
        areas = get_application_areas()
        application_filter = st.multiselect("🎯 Lĩnh vực ứng dụng", areas)
    
    with col5:
        statuses = get_status_options()
        status_filter = st.selectbox("📊 Tình trạng", ["Tất cả"] + statuses)
    
    if st.button("🔍 Tìm kiếm", type="primary", use_container_width=True):
        results = search_products(search_term, category_filter, company_filter, 
                                 application_filter, status_filter)
        
        if results:
            st.success(f"Tìm thấy {len(results)} sản phẩm")
            
            for product in results:
                with st.expander(f"**{product[1]}** - {product[3]}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Mã sản phẩm:** {product[3]}")
                        st.markdown(f"**Công ty:** {get_company_name(product[2])}")
                        st.markdown(f"**Danh mục:** {product[4]} - {product[5]}")
                        st.markdown(f"**Mô tả:** {product[6]}")
                        if product[23]:  # strengths
                            st.markdown(f"**Điểm mạnh:** {product[23]}")
                        if product[24]:  # weaknesses
                            st.markdown(f"**Điểm yếu:** {product[24]}")
                    
                    with col2:
                        st.markdown(f"**Giá:** {product[14]} {product[15]}")
                        st.markdown(f"**Tình trạng:** {product[16]}")
                        if product[19]:
                            st.markdown(f"**Đánh giá:** {'⭐' * int(product[19])}")
                        
                        if st.button("Chi tiết", key=f"detail_{product[0]}"):
                            st.session_state.selected_product = product[0]
                            st.session_state.page = 'product_detail'
                            st.rerun()
        else:
            st.warning("Không tìm thấy sản phẩm phù hợp")

def search_products(search_term, category, company, applications, status):
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    
    query = "SELECT * FROM products WHERE status = 'Active'"
    params = []
    
    if search_term:
        query += " AND (product_name LIKE ? OR product_code LIKE ? OR description LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
    
    if category != "Tất cả":
        query += " AND category = ?"
        params.append(category)
    
    if company != "Tất cả":
        company_id = get_company_id(company)
        if company_id:
            query += " AND company_id = ?"
            params.append(company_id)
    
    if applications:
        app_conditions = " OR ".join(["application_areas LIKE ?" for _ in applications])
        query += f" AND ({app_conditions})"
        params.extend([f"%{app}%" for app in applications])
    
    if status != "Tất cả":
        query += " AND availability_status = ?"
        params.append(status)
    
    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    
    return results

# Hàm thêm sản phẩm với các trường mới
def show_add_product():
    st.markdown("## ➕ Thêm sản phẩm mới")
    
    with st.form("add_product_form"):
        st.markdown("### 📋 Thông tin cơ bản")
        col1, col2 = st.columns(2)
        
        with col1:
            product_id = st.text_input("Product ID *", placeholder="PRD001")
            product_name = st.text_input("Tên sản phẩm *", placeholder="Tên sản phẩm...")
            company = st.selectbox("Công ty *", get_company_list())
            product_code = st.text_input("Mã sản phẩm", placeholder="SKU-001")
            
            categories = get_categories()
            category = st.selectbox("Danh mục *", categories)
            
            subcategories = get_subcategories(category)
            subcategory = st.selectbox("Danh mục phụ *", subcategories)
        
        with col2:
            description = st.text_area("Mô tả", placeholder="Mô tả chi tiết sản phẩm...")
            
            areas = get_application_areas()
            applications = st.multiselect("Lĩnh vực ứng dụng", areas)
            
            package_size = st.text_input("Quy cách đóng gói", placeholder="10 pieces/box")
            
            currencies = get_currencies()
            currency = st.selectbox("Đơn vị tiền tệ", currencies)
            list_price = st.number_input("Giá niêm yết", min_value=0.0, step=0.01)
            
            statuses = get_status_options()
            availability = st.selectbox("Tình trạng", statuses)
        
        st.markdown("---")
        st.markdown("### 🔬 Thông tin kỹ thuật")
        
        col3, col4 = st.columns(2)
        with col3:
            specifications = st.text_area("Thông số kỹ thuật", placeholder="Chi tiết kỹ thuật...")
            storage_conditions = st.text_input("Điều kiện bảo quản", placeholder="2-8°C")
            shelf_life = st.text_input("Hạn sử dụng", placeholder="24 months")
        
        with col4:
            composition = st.text_area("Thành phần", placeholder="Thành phần cấu tạo...")
            distributor_vietnam = st.text_input("Nhà phân phối VN", placeholder="Tên nhà phân phối...")
            rating = st.slider("Đánh giá", 0.0, 5.0, 0.0, 0.1)
        
        st.markdown("---")
        st.markdown("### ✅ Đánh giá chất lượng (MỚI)")
        
        col5, col6 = st.columns(2)
        with col5:
            strengths = st.text_area("💪 Điểm mạnh", 
                placeholder="Các ưu điểm nổi bật của sản phẩm...",
                help="Mô tả các điểm mạnh, ưu điểm của sản phẩm")
            
            weaknesses = st.text_area("⚠️ Điểm yếu", 
                placeholder="Các hạn chế của sản phẩm...",
                help="Mô tả các điểm yếu, hạn chế cần lưu ý")
            
            qa_qc_certifications = st.text_area("📜 Chứng nhận QA/QC", 
                placeholder="ISO 13485, CE Mark, FDA 510(k)...",
                help="Các chứng nhận về chất lượng và kiểm soát")
        
        with col6:
            validation_evidence = st.text_area("🔬 Minh chứng Validation", 
                placeholder="Các nghiên cứu, báo cáo validation...",
                help="Bằng chứng về tính hiệu quả, độ tin cậy")
            
            expert_review_1 = st.text_area("👨‍⚕️ Nhận định CVPH 1", 
                placeholder="Đánh giá từ chuyên gia 1...",
                help="Nhận định, đánh giá từ chuyên gia phôi học 1")
            
            expert_review_2 = st.text_area("👨‍⚕️ Nhận định CVPH 2", 
                placeholder="Đánh giá từ chuyên gia 2...",
                help="Nhận định, đánh giá từ chuyên gia phôi học 2")
            
            expert_review_3 = st.text_area("👨‍⚕️ Nhận định CVPH 3", 
                placeholder="Đánh giá từ chuyên gia 3...",
                help="Nhận định, đánh giá từ chuyên gia phôi học 3")
        
        submitted = st.form_submit_button("💾 Lưu sản phẩm", type="primary", use_container_width=True)
        
        if submitted:
            if product_id and product_name and company:
                conn = sqlite3.connect('ivf_products_pro.db')
                c = conn.cursor()
                
                company_id = get_company_id(company)
                app_str = ", ".join(applications)
                
                try:
                    c.execute('''INSERT INTO products 
                                (product_id, product_name, company_id, product_code, category, 
                                subcategory, description, specifications, application_areas, 
                                package_size, list_price, currency, availability_status, 
                                storage_conditions, shelf_life, composition, distributor_vietnam,
                                rating, strengths, weaknesses, qa_qc_certifications, 
                                validation_evidence, expert_review_1, expert_review_2, 
                                expert_review_3, created_date, updated_date, status)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                             (product_id, product_name, company_id, product_code, category,
                              subcategory, description, specifications, app_str,
                              package_size, list_price, currency, availability,
                              storage_conditions, shelf_life, composition, distributor_vietnam,
                              rating, strengths, weaknesses, qa_qc_certifications,
                              validation_evidence, expert_review_1, expert_review_2,
                              expert_review_3, datetime.now().isoformat(), 
                              datetime.now().isoformat(), 'Active'))
                    conn.commit()
                    st.success("✅ Đã thêm sản phẩm thành công!")
                except sqlite3.IntegrityError:
                    st.error("❌ Product ID đã tồn tại!")
                finally:
                    conn.close()
            else:
                st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc (*)")

# Hàm sửa sản phẩm
def show_edit_product():
    st.markdown("## ✏️ Sửa/Cập nhật sản phẩm")
    
    # Chọn sản phẩm để sửa
    conn = sqlite3.connect('ivf_products_pro.db')
    df = pd.read_sql_query("SELECT product_id, product_name, company_id FROM products WHERE status = 'Active'", conn)
    conn.close()
    
    if df.empty:
        st.info("Chưa có sản phẩm nào trong hệ thống")
        return
    
    # Tạo dictionary để map tên sản phẩm với ID
    product_dict = {f"{row['product_name']} ({row['product_id']})": row['product_id'] 
                   for _, row in df.iterrows()}
    
    selected_product_name = st.selectbox("Chọn sản phẩm cần sửa", list(product_dict.keys()))
    selected_product_id = product_dict[selected_product_name]
    
    # Load thông tin sản phẩm
    conn = sqlite3.connect('ivf_products_pro.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE product_id = ?", (selected_product_id,))
    product = c.fetchone()
    conn.close()
    
    if not product:
        st.error("Không tìm thấy sản phẩm")
        return
    
    # Form sửa sản phẩm
    with st.form("edit_product_form"):
        st.markdown("### 📋 Thông tin cơ bản")
        col1, col2 = st.columns(2)
        
        with col1:
            product_id = st.text_input("Product ID *", value=product[0], disabled=True)
            product_name = st.text_input("Tên sản phẩm *", value=product[1])
            
            current_company_name = get_company_name(product[2])
            company = st.selectbox("Công ty *", get_company_list(), 
                                  index=get_company_list().index(current_company_name) if current_company_name in get_company_list() else 0)
            
            product_code = st.text_input("Mã sản phẩm", value=product[3] or "")
            
            categories = get_categories()
            category = st.selectbox("Danh mục *", categories,
                                   index=categories.index(product[4]) if product[4] in categories else 0)
            
            subcategories = get_subcategories(category)
            subcategory = st.selectbox("Danh mục phụ *", subcategories,
                                      index=subcategories.index(product[5]) if product[5] in subcategories else 0)
        
        with col2:
            description = st.text_area("Mô tả", value=product[6] or "")
            
            areas = get_application_areas()
            current_apps = product[8].split(", ") if product[8] else []
            applications = st.multiselect("Lĩnh vực ứng dụng", areas, default=current_apps)
            
            package_size = st.text_input("Quy cách đóng gói", value=product[9] or "")
            
            currencies = get_currencies()
            currency = st.selectbox("Đơn vị tiền tệ", currencies,
                                   index=currencies.index(product[15]) if product[15] in currencies else 0)
            list_price = st.number_input("Giá niêm yết", value=float(product[14]) if product[14] else 0.0, step=0.01)
            
            statuses = get_status_options()
            availability = st.selectbox("Tình trạng", statuses,
                                       index=statuses.index(product[16]) if product[16] in statuses else 0)
        
        st.markdown("---")
        st.markdown("### 🔬 Thông tin kỹ thuật")
        
        col3, col4 = st.columns(2)
        with col3:
            specifications = st.text_area("Thông số kỹ thuật", value=product[7] or "")
            storage_conditions = st.text_input("Điều kiện bảo quản", value=product[11] or "")
            shelf_life = st.text_input("Hạn sử dụng", value=product[12] or "")
        
        with col4:
            composition = st.text_area("Thành phần", value=product[13] or "")
            distributor_vietnam = st.text_input("Nhà phân phối VN", value=product[17] or "")
            rating = st.slider("Đánh giá", 0.0, 5.0, float(product[20]) if product[20] else 0.0, 0.1)
        
        st.markdown("---")
        st.markdown("### ✅ Đánh giá chất lượng")
        
        col5, col6 = st.columns(2)
        with col5:
            strengths = st.text_area("💪 Điểm mạnh", value=product[23] or "")
            weaknesses = st.text_area("⚠️ Điểm yếu", value=product[24] or "")
            qa_qc_certifications = st.text_area("📜 Chứng nhận QA/QC", value=product[25] or "")
        
        with col6:
            validation_evidence = st.text_area("🔬 Minh chứng Validation", value=product[26] or "")
            expert_review_1 = st.text_area("👨‍⚕️ Nhận định CVPH 1", value=product[27] or "")
            expert_review_2 = st.text_area("👨‍⚕️ Nhận định CVPH 2", value=product[28] or "")
            expert_review_3 = st.text_area("👨‍⚕️ Nhận định CVPH 3", value=product[29] or "")
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            submitted = st.form_submit_button("💾 Cập nhật sản phẩm", type="primary", use_container_width=True)
        with col_btn2:
            delete = st.form_submit_button("🗑️ Xóa", type="secondary", use_container_width=True)
        
        if submitted:
            conn = sqlite3.connect('ivf_products_pro.db')
            c = conn.cursor()
            
            company_id = get_company_id(company)
            app_str = ", ".join(applications)
            
            try:
                c.execute('''UPDATE products SET 
                            product_name=?, company_id=?, product_code=?, category=?, 
                            subcategory=?, description=?, specifications=?, application_areas=?, 
                            package_size=?, list_price=?, currency=?, availability_status=?, 
                            storage_conditions=?, shelf_life=?, composition=?, distributor_vietnam=?,
                            rating=?, strengths=?, weaknesses=?, qa_qc_certifications=?, 
                            validation_evidence=?, expert_review_1=?, expert_review_2=?, 
                            expert_review_3=?, updated_date=?
                            WHERE product_id=?''',
                         (product_name, company_id, product_code, category,
                          subcategory, description, specifications, app_str,
                          package_size, list_price, currency, availability,
                          storage_conditions, shelf_life, composition, distributor_vietnam,
                          rating, strengths, weaknesses, qa_qc_certifications,
                          validation_evidence, expert_review_1, expert_review_2,
                          expert_review_3, datetime.now().isoformat(), product_id))
                conn.commit()
                st.success("✅ Đã cập nhật sản phẩm thành công!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
            finally:
                conn.close()
        
        if delete:
            if st.session_state.get('confirm_delete', False):
                conn = sqlite3.connect('ivf_products_pro.db')
                c = conn.cursor()
                c.execute("UPDATE products SET status='Inactive' WHERE product_id=?", (product_id,))
                conn.commit()
                conn.close()
                st.success("✅ Đã xóa sản phẩm!")
                st.session_state.confirm_delete = False
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("⚠️ Nhấn 'Xóa' lần nữa để xác nhận xóa sản phẩm này!")

# Hàm quản lý danh mục
def show_manage_categories():
    st.markdown("## ⚙️ Quản lý danh mục hệ thống")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📁 Danh mục", "📂 Danh mục phụ", "🎯 Lĩnh vực ứng dụng", "💰 Đơn vị tiền tệ", "📊 Tình trạng"])
    
    # Tab 1: Categories
    with tab1:
        st.markdown("### Quản lý Danh mục chính")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_category_form"):
                st.markdown("**Thêm danh mục mới**")
                new_category = st.text_input("Tên danh mục", placeholder="Equipment, Media...")
                new_category_desc = st.text_input("Mô tả", placeholder="Mô tả ngắn...")
                
                if st.form_submit_button("➕ Thêm danh mục"):
                    if new_category:
                        conn = sqlite3.connect('ivf_products_pro.db')
                        c = conn.cursor()
                        try:
                            c.execute("INSERT INTO categories (category_name, description, created_date) VALUES (?, ?, ?)",
                                     (new_category, new_category_desc, datetime.now().isoformat()))
                            conn.commit()
                            st.success(f"✅ Đã thêm danh mục: {new_category}")
                        except sqlite3.IntegrityError:
                            st.error("❌ Danh mục đã tồn tại!")
                        finally:
                            conn.close()
                    else:
                        st.error("❌ Vui lòng nhập tên danh mục!")
        
        with col2:
            st.markdown("**Danh sách danh mục**")
            conn = sqlite3.connect('ivf_products_pro.db')
            df = pd.read_sql_query("SELECT category_name, is_active FROM categories ORDER BY category_name", conn)
            conn.close()
            
            for _, row in df.iterrows():
                status = "✅" if row['is_active'] else "❌"
                st.text(f"{status} {row['category_name']}")
    
    # Tab 2: Subcategories
    with tab2:
        st.markdown("### Quản lý Danh mục phụ")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_subcategory_form"):
                st.markdown("**Thêm danh mục phụ mới**")
                parent_category = st.selectbox("Danh mục chính", get_categories())
                new_subcategory = st.text_input("Tên danh mục phụ", placeholder="Incubator, Needles...")
                new_subcategory_desc = st.text_input("Mô tả", placeholder="Mô tả ngắn...")
                
                if st.form_submit_button("➕ Thêm danh mục phụ"):
                    if new_subcategory:
                        conn = sqlite3.connect('ivf_products_pro.db')
                        c = conn.cursor()
                        try:
                            c.execute("INSERT INTO subcategories (category_name, subcategory_name, description, created_date) VALUES (?, ?, ?, ?)",
                                     (parent_category, new_subcategory, new_subcategory_desc, datetime.now().isoformat()))
                            conn.commit()
                            st.success(f"✅ Đã thêm danh mục phụ: {new_subcategory}")
                        except sqlite3.IntegrityError:
                            st.error("❌ Danh mục phụ đã tồn tại!")
                        finally:
                            conn.close()
                    else:
                        st.error("❌ Vui lòng nhập tên danh mục phụ!")
        
        with col2:
            st.markdown("**Danh sách danh mục phụ**")
            conn = sqlite3.connect('ivf_products_pro.db')
            df = pd.read_sql_query("SELECT category_name, subcategory_name, is_active FROM subcategories ORDER BY category_name, subcategory_name", conn)
            conn.close()
            
            for _, row in df.iterrows():
                status = "✅" if row['is_active'] else "❌"
                st.text(f"{status} {row['category_name']} → {row['subcategory_name']}")
    
    # Tab 3: Application Areas
    with tab3:
        st.markdown("### Quản lý Lĩnh vực ứng dụng")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_area_form"):
                st.markdown("**Thêm lĩnh vực ứng dụng mới**")
                new_area = st.text_input("Tên lĩnh vực", placeholder="ICSI, Vitrification...")
                new_area_desc = st.text_input("Mô tả", placeholder="Mô tả ngắn...")
                
                if st.form_submit_button("➕ Thêm lĩnh vực"):
                    if new_area:
                        conn = sqlite3.connect('ivf_products_pro.db')
                        c = conn.cursor()
                        try:
                            c.execute("INSERT INTO application_areas (area_name, description, created_date) VALUES (?, ?, ?)",
                                     (new_area, new_area_desc, datetime.now().isoformat()))
                            conn.commit()
                            st.success(f"✅ Đã thêm lĩnh vực: {new_area}")
                        except sqlite3.IntegrityError:
                            st.error("❌ Lĩnh vực đã tồn tại!")
                        finally:
                            conn.close()
                    else:
                        st.error("❌ Vui lòng nhập tên lĩnh vực!")
        
        with col2:
            st.markdown("**Danh sách lĩnh vực**")
            conn = sqlite3.connect('ivf_products_pro.db')
            df = pd.read_sql_query("SELECT area_name, is_active FROM application_areas ORDER BY area_name", conn)
            conn.close()
            
            for _, row in df.iterrows():
                status = "✅" if row['is_active'] else "❌"
                st.text(f"{status} {row['area_name']}")
    
    # Tab 4: Currencies
    with tab4:
        st.markdown("### Quản lý Đơn vị tiền tệ")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_currency_form"):
                st.markdown("**Thêm đơn vị tiền tệ mới**")
                new_currency_code = st.text_input("Mã tiền tệ", placeholder="USD, EUR, VND...")
                new_currency_name = st.text_input("Tên tiền tệ", placeholder="US Dollar, Euro...")
                new_currency_symbol = st.text_input("Ký hiệu", placeholder="$, €, ₫...")
                
                if st.form_submit_button("➕ Thêm tiền tệ"):
                    if new_currency_code:
                        conn = sqlite3.connect('ivf_products_pro.db')
                        c = conn.cursor()
                        try:
                            c.execute("INSERT INTO currencies (currency_code, currency_name, symbol, created_date) VALUES (?, ?, ?, ?)",
                                     (new_currency_code.upper(), new_currency_name, new_currency_symbol, datetime.now().isoformat()))
                            conn.commit()
                            st.success(f"✅ Đã thêm tiền tệ: {new_currency_code}")
                        except sqlite3.IntegrityError:
                            st.error("❌ Tiền tệ đã tồn tại!")
                        finally:
                            conn.close()
                    else:
                        st.error("❌ Vui lòng nhập mã tiền tệ!")
        
        with col2:
            st.markdown("**Danh sách tiền tệ**")
            conn = sqlite3.connect('ivf_products_pro.db')
            df = pd.read_sql_query("SELECT currency_code, symbol, is_active FROM currencies ORDER BY currency_code", conn)
            conn.close()
            
            for _, row in df.iterrows():
                status = "✅" if row['is_active'] else "❌"
                symbol = row['symbol'] if row['symbol'] else ""
                st.text(f"{status} {row['currency_code']} {symbol}")
    
    # Tab 5: Status Options
    with tab5:
        st.markdown("### Quản lý Tình trạng sản phẩm")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_status_form"):
                st.markdown("**Thêm tình trạng mới**")
                new_status = st.text_input("Tên tình trạng", placeholder="Available, Out of Stock...")
                new_status_desc = st.text_input("Mô tả", placeholder="Mô tả ngắn...")
                
                if st.form_submit_button("➕ Thêm tình trạng"):
                    if new_status:
                        conn = sqlite3.connect('ivf_products_pro.db')
                        c = conn.cursor()
                        try:
                            c.execute("INSERT INTO status_options (status_name, description, created_date) VALUES (?, ?, ?)",
                                     (new_status, new_status_desc, datetime.now().isoformat()))
                            conn.commit()
                            st.success(f"✅ Đã thêm tình trạng: {new_status}")
                        except sqlite3.IntegrityError:
                            st.error("❌ Tình trạng đã tồn tại!")
                        finally:
                            conn.close()
                    else:
                        st.error("❌ Vui lòng nhập tên tình trạng!")
        
        with col2:
            st.markdown("**Danh sách tình trạng**")
            conn = sqlite3.connect('ivf_products_pro.db')
            df = pd.read_sql_query("SELECT status_name, is_active FROM status_options ORDER BY status_name", conn)
            conn.close()
            
            for _, row in df.iterrows():
                status = "✅" if row['is_active'] else "❌"
                st.text(f"{status} {row['status_name']}")

# Các hàm còn lại giữ nguyên
def show_companies():
    st.markdown("## 🏢 Danh sách công ty")
    
    conn = sqlite3.connect('ivf_products_pro.db')
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    
    if not df.empty:
        for _, company in df.iterrows():
            with st.expander(f"**{company['company_name']}** ({company['country']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Trụ sở:** {company['headquarters_address']}")
                    st.markdown(f"**Website:** {company['website']}")
                    st.markdown(f"**Email:** {company['contact_email']}")
                    st.markdown(f"**Điện thoại:** {company['contact_phone']}")
                
                with col2:
                    st.markdown(f"**Năm thành lập:** {company['year_established']}")
                    st.markdown(f"**Chứng nhận:** {company['certifications']}")
                    st.markdown(f"**Mô tả:** {company['description']}")
    else:
        st.info("Chưa có công ty nào trong cơ sở dữ liệu")

def show_add_company():
    st.markdown("## ➕ Thêm công ty mới")
    
    with st.form("add_company_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_id = st.text_input("Company ID *", placeholder="COM001")
            company_name = st.text_input("Tên công ty *", placeholder="Tên công ty...")
            country = st.text_input("Quốc gia *", placeholder="Japan")
            headquarters = st.text_input("Địa chỉ trụ sở", placeholder="123 Street...")
            website = st.text_input("Website", placeholder="https://...")
        
        with col2:
            contact_email = st.text_input("Email", placeholder="info@company.com")
            contact_phone = st.text_input("Điện thoại", placeholder="+81-...")
            year_established = st.number_input("Năm thành lập", min_value=1900, max_value=2024, value=2000)
            certifications = st.text_input("Chứng nhận", placeholder="ISO 13485, CE, FDA")
        
        description = st.text_area("Mô tả", placeholder="Mô tả về công ty...")
        
        submitted = st.form_submit_button("💾 Lưu công ty", type="primary", use_container_width=True)
        
        if submitted:
            if company_id and company_name and country:
                conn = sqlite3.connect('ivf_products_pro.db')
                c = conn.cursor()
                
                try:
                    c.execute('''INSERT INTO companies 
                                (company_id, company_name, country, headquarters_address,
                                website, contact_email, contact_phone, year_established,
                                certifications, description, created_date, updated_date)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                             (company_id, company_name, country, headquarters, website,
                              contact_email, contact_phone, year_established, certifications,
                              description, datetime.now().isoformat(), datetime.now().isoformat()))
                    conn.commit()
                    st.success("✅ Đã thêm công ty thành công!")
                except sqlite3.IntegrityError:
                    st.error("❌ Company ID đã tồn tại!")
                finally:
                    conn.close()
            else:
                st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc (*)")

def show_statistics():
    st.markdown("## 📊 Thống kê")
    
    conn = sqlite3.connect('ivf_products_pro.db')
    
    st.markdown("### Sản phẩm theo danh mục")
    df_category = pd.read_sql_query(
        "SELECT category, COUNT(*) as count FROM products WHERE status='Active' GROUP BY category", conn)
    if not df_category.empty:
        st.bar_chart(df_category.set_index('category'))
    
    st.markdown("### Sản phẩm theo công ty")
    df_company = pd.read_sql_query('''
        SELECT c.company_name, COUNT(p.product_id) as count 
        FROM companies c 
        LEFT JOIN products p ON c.company_id = p.company_id 
        WHERE p.status='Active' OR p.status IS NULL
        GROUP BY c.company_name
    ''', conn)
    if not df_company.empty:
        st.bar_chart(df_company.set_index('company_name'))
    
    st.markdown("### Công ty theo quốc gia")
    df_country = pd.read_sql_query(
        "SELECT country, COUNT(*) as count FROM companies GROUP BY country", conn)
    if not df_country.empty:
        st.bar_chart(df_country.set_index('country'))
    
    conn.close()

def show_import_export():
    st.markdown("## 📥 Import/Export dữ liệu")
    
    tab1, tab2 = st.tabs(["📥 Import", "📤 Export"])
    
    with tab1:
        st.markdown("### Import dữ liệu từ CSV/Excel")
        
        data_type = st.radio("Loại dữ liệu", ["Products", "Companies"])
        uploaded_file = st.file_uploader("Chọn file", type=['csv', 'xlsx'])
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.dataframe(df.head())
                
                if st.button("Import vào database"):
                    conn = sqlite3.connect('ivf_products_pro.db')
                    table_name = 'products' if data_type == 'Products' else 'companies'
                    df.to_sql(table_name, conn, if_exists='append', index=False)
                    conn.close()
                    st.success(f"✅ Đã import {len(df)} dòng thành công!")
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
    
    with tab2:
        st.markdown("### Export dữ liệu ra CSV/Excel")
        
        data_type = st.radio("Loại dữ liệu", ["Products", "Companies"], key="export_type")
        export_format = st.radio("Định dạng", ["CSV", "Excel"])
        
        if st.button("Export"):
            conn = sqlite3.connect('ivf_products_pro.db')
            table_name = 'products' if data_type == 'Products' else 'companies'
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            conn.close()
            
            if export_format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{table_name}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

def show_guide():
    st.markdown("## ℹ️ Hướng dẫn sử dụng")
    
    st.markdown("""
    ### 📚 Hướng dẫn chi tiết - Phiên bản Pro
    
    #### 🆕 Tính năng mới
    
    **1. Đánh giá chuyên gia**
    - Điểm mạnh/Điểm yếu: Phân tích ưu nhược điểm
    - Chứng nhận QA/QC: Thông tin về chất lượng
    - Minh chứng Validation: Bằng chứng hiệu quả
    - Nhận định từ 3 chuyên gia phôi học
    
    **2. Quản lý danh mục linh hoạt**
    - Thêm/sửa danh mục và danh mục phụ
    - Quản lý lĩnh vực ứng dụng
    - Tùy chỉnh đơn vị tiền tệ
    - Cập nhật tình trạng sản phẩm
    
    **3. Chỉnh sửa sản phẩm**
    - Cập nhật thông tin sản phẩm dễ dàng
    - Xóa sản phẩm (chuyển sang Inactive)
    - Lưu lịch sử thay đổi
    
    #### 📖 Hướng dẫn sử dụng
    
    **Thêm sản phẩm:**
    1. Chọn "➕ Thêm sản phẩm" từ menu
    2. Điền thông tin cơ bản (bắt buộc)
    3. Thêm thông tin kỹ thuật
    4. Điền đánh giá chất lượng và nhận định chuyên gia
    5. Nhấn "Lưu sản phẩm"
    
    **Sửa sản phẩm:**
    1. Chọn "✏️ Sửa sản phẩm" từ menu
    2. Chọn sản phẩm cần sửa
    3. Cập nhật thông tin
    4. Nhấn "Cập nhật sản phẩm"
    
    **Quản lý danh mục:**
    1. Chọn "⚙️ Quản lý danh mục" từ menu
    2. Chọn tab tương ứng
    3. Thêm mới hoặc chỉnh sửa
    
    ### 📞 Hỗ trợ
    - Email: support@ivfcatalog.com
    - Version: Pro 2.0
    """)

# Main app
def main():
    init_database()
    add_default_data()
    
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'search':
        show_search()
    elif st.session_state.page == 'companies':
        show_companies()
    elif st.session_state.page == 'add_product':
        show_add_product()
    elif st.session_state.page == 'edit_product':
        show_edit_product()
    elif st.session_state.page == 'add_company':
        show_add_company()
    elif st.session_state.page == 'manage_categories':
        show_manage_categories()
    elif st.session_state.page == 'statistics':
        show_statistics()
    elif st.session_state.page == 'import_export':
        show_import_export()
    elif st.session_state.page == 'guide':
        show_guide()

if __name__ == "__main__":
    main()
