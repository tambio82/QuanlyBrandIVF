import streamlit as st
import pandas as pd
import json
from datetime import datetime
import sqlite3
import os

# Cấu hình trang
st.set_page_config(
    page_title="IVF Product Catalog",
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
    </style>
""", unsafe_allow_html=True)

# Khởi tạo database SQLite
def init_database():
    conn = sqlite3.connect('ivf_products.db')
    c = conn.cursor()
    
    # Bảng Companies
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
    
    # Bảng Products
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
                  created_date TEXT,
                  updated_date TEXT,
                  status TEXT,
                  FOREIGN KEY (company_id) REFERENCES companies (company_id))''')
    
    conn.commit()
    conn.close()

# Hàm thêm dữ liệu mẫu
def add_sample_data():
    conn = sqlite3.connect('ivf_products.db')
    c = conn.cursor()
    
    # Kiểm tra xem đã có dữ liệu chưa
    c.execute("SELECT COUNT(*) FROM companies")
    if c.fetchone()[0] == 0:
        # Thêm công ty mẫu
        sample_companies = [
            ('KTZ001', 'Kitazato Corporation', 'Japan', 'Shizuoka, Japan', 
             'https://www.kitazato.co.jp/en/', 'info@kitazato.co.jp', '+81-3-3434-1653',
             1996, 'ISO 13485, CE, FDA', 'Leading Japanese company in ART products', '', 
             datetime.now().isoformat(), datetime.now().isoformat()),
            ('IVT001', 'Irvine Scientific', 'USA', 'Santa Ana, CA, USA',
             'https://www.irvinesci.com/', 'info@irvinesci.com', '+1-949-261-7800',
             1970, 'ISO 13485, CE, FDA', 'Pioneer in cell culture media', '',
             datetime.now().isoformat(), datetime.now().isoformat()),
            ('VIT001', 'Vitrolife', 'Sweden', 'Gothenburg, Sweden',
             'https://www.vitrolife.com/', 'info@vitrolife.com', '+46-31-721-8000',
             1994, 'ISO 13485, CE, FDA', 'Global leader in IVF products', '',
             datetime.now().isoformat(), datetime.now().isoformat())
        ]
        c.executemany('''INSERT INTO companies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                      sample_companies)
        
        # Thêm sản phẩm mẫu
        sample_products = [
            ('PRD001', 'Cryotop® Open System', 'KTZ001', 'CT-001', 'Devices', 
             'Vitrification Device', 'Revolutionary vitrification device for oocytes and embryos',
             'Cooling speed: -23,000°C/min', 'Vitrification', '20 pieces/box', 'piece',
             'Room temperature', '5 years', 'Polystyrene strip with protective straw',
             120.00, 'USD', 'Available', 'Available through local distributors',
             'Ultra-rapid cooling, High survival rate', 'Market leader, Proven results',
             4.8, '', '', datetime.now().isoformat(), datetime.now().isoformat(), 'Active'),
            
            ('PRD002', 'VT601 Vitrification Media', 'KTZ001', 'VT-601', 'Media',
             'Vitrification Medium', 'Protein-free vitrification media for oocytes and embryos',
             'Contains HPC as non-protein supplement', 'Vitrification', '4 vials x 4ml', 'ml',
             '2-8°C', '18 months', 'Synthetic and plant derivatives with HPC',
             150.00, 'USD', 'Available', 'Available through local distributors',
             'Protein-free, High survival rate', 'Safe, Effective',
             4.7, '', '', datetime.now().isoformat(), datetime.now().isoformat(), 'Active'),
            
            ('PRD003', 'Single Lumen OPU Needle', 'KTZ001', 'OPU-17G', 'Consumables',
             'Oocyte Retrieval Needle', 'Single lumen needle with echo-marked tip',
             '17 Gauge, Echo-marked tip', 'Oocyte Retrieval', '25 pieces/box', 'piece',
             'Room temperature', '5 years', 'Medical grade stainless steel',
             45.00, 'USD', 'Available', 'Available through local distributors',
             'Echo-marked tip, Optimal grip design', 'Easy positioning',
             4.6, '', '', datetime.now().isoformat(), datetime.now().isoformat(), 'Active')
        ]
        c.executemany('''INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                      sample_products)
        
        conn.commit()
    conn.close()

# Danh sách categories và subcategories
CATEGORIES = {
    "Equipment": ["Incubator", "Microscope", "Workstation", "Centrifuge", "Analyzer", "Imaging System"],
    "Consumables": ["Needles", "Catheters", "Pipettes", "Dishes", "Plates", "Tubes", "Syringes"],
    "Media": ["Culture Medium", "Vitrification Medium", "Thawing Medium", "Sperm Processing Medium", "Buffers"],
    "Chemicals": ["Enzymes", "Oils", "Reagents", "Supplements", "Indicators"],
    "Devices": ["Vitrification Device", "Transfer Device", "Biopsy Device", "Injection Device"],
    "Software/AI": ["Embryo Selection", "Sperm Analysis", "Lab Management", "Data Analysis"]
}

APPLICATION_AREAS = [
    "Oocyte Retrieval", "ICSI", "C-IVF", "Embryo Culture", "Vitrification",
    "Embryo Transfer", "IUI", "Andrology", "IVM", "PGT", "Evaluation"
]

# Khởi tạo session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=IVF+Catalog", width=200)
    st.markdown("---")
    
    menu_items = {
        "🏠 Trang chủ": "home",
        "🔍 Tìm kiếm sản phẩm": "search",
        "🏢 Danh sách công ty": "companies",
        "➕ Thêm sản phẩm": "add_product",
        "➕ Thêm công ty": "add_company",
        "📊 Thống kê": "statistics",
        "📥 Import/Export": "import_export",
        "ℹ️ Hướng dẫn": "guide"
    }
    
    for label, page in menu_items.items():
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page

# Hàm hiển thị trang chủ
def show_home():
    st.markdown('<p class="main-header">🧬 IVF Product Catalog</p>', unsafe_allow_html=True)
    st.markdown("### Hệ thống quản lý thông tin sản phẩm IVF toàn cầu")
    
    # Thống kê nhanh
    conn = sqlite3.connect('ivf_products.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM companies")
    total_companies = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM products")
    total_products = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT category) FROM products")
    total_categories = c.fetchone()[0]
    
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
                <h2>{len(APPLICATION_AREAS)}</h2>
                <p>Ứng dụng</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Danh mục sản phẩm
    st.markdown("### 📦 Danh mục sản phẩm")
    cols = st.columns(3)
    for idx, (category, subcats) in enumerate(CATEGORIES.items()):
        with cols[idx % 3]:
            with st.expander(f"**{category}**"):
                for subcat in subcats:
                    st.markdown(f"- {subcat}")

# Hàm tìm kiếm sản phẩm
def show_search():
    st.markdown("## 🔍 Tìm kiếm sản phẩm")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔎 Từ khóa", placeholder="Nhập tên sản phẩm, mã sản phẩm...")
    
    with col2:
        category_filter = st.selectbox("📁 Danh mục", ["Tất cả"] + list(CATEGORIES.keys()))
    
    with col3:
        company_filter = st.selectbox("🏢 Công ty", ["Tất cả"] + get_company_list())
    
    col4, col5 = st.columns(2)
    with col4:
        application_filter = st.multiselect("🎯 Lĩnh vực ứng dụng", APPLICATION_AREAS)
    
    with col5:
        status_filter = st.selectbox("📊 Tình trạng", ["Tất cả", "Available", "Out of Stock", "Discontinued"])
    
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
                        st.markdown(f"**Ứng dụng:** {product[8]}")
                    
                    with col2:
                        st.markdown(f"**Giá:** {product[14]} {product[15]}")
                        st.markdown(f"**Tình trạng:** {product[16]}")
                        st.markdown(f"**Đánh giá:** {'⭐' * int(product[19]) if product[19] else 'N/A'}")
                        
                        if st.button("Chi tiết", key=f"detail_{product[0]}"):
                            st.session_state.selected_product = product[0]
                            st.session_state.page = 'product_detail'
                            st.rerun()
        else:
            st.warning("Không tìm thấy sản phẩm phù hợp")

# Hàm lấy danh sách công ty
def get_company_list():
    conn = sqlite3.connect('ivf_products.db')
    c = conn.cursor()
    c.execute("SELECT company_name FROM companies ORDER BY company_name")
    companies = [row[0] for row in c.fetchall()]
    conn.close()
    return companies

# Hàm lấy tên công ty từ ID
def get_company_name(company_id):
    conn = sqlite3.connect('ivf_products.db')
    c = conn.cursor()
    c.execute("SELECT company_name FROM companies WHERE company_id = ?", (company_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "Unknown"

# Hàm tìm kiếm sản phẩm
def search_products(search_term, category, company, applications, status):
    conn = sqlite3.connect('ivf_products.db')
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

# Hàm lấy company_id từ tên
def get_company_id(company_name):
    conn = sqlite3.connect('ivf_products.db')
    c = conn.cursor()
    c.execute("SELECT company_id FROM companies WHERE company_name = ?", (company_name,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Hàm hiển thị danh sách công ty
def show_companies():
    st.markdown("## 🏢 Danh sách công ty")
    
    conn = sqlite3.connect('ivf_products.db')
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

# Hàm thêm sản phẩm
def show_add_product():
    st.markdown("## ➕ Thêm sản phẩm mới")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_id = st.text_input("Product ID *", placeholder="PRD001")
            product_name = st.text_input("Tên sản phẩm *", placeholder="Tên sản phẩm...")
            company = st.selectbox("Công ty *", get_company_list())
            product_code = st.text_input("Mã sản phẩm", placeholder="SKU-001")
            category = st.selectbox("Danh mục *", list(CATEGORIES.keys()))
            subcategory = st.selectbox("Danh mục phụ *", CATEGORIES[category])
        
        with col2:
            description = st.text_area("Mô tả", placeholder="Mô tả chi tiết sản phẩm...")
            applications = st.multiselect("Lĩnh vực ứng dụng", APPLICATION_AREAS)
            package_size = st.text_input("Quy cách đóng gói", placeholder="10 pieces/box")
            list_price = st.number_input("Giá niêm yết", min_value=0.0, step=0.01)
            currency = st.selectbox("Đơn vị tiền tệ", ["USD", "EUR", "VND", "JPY"])
            availability = st.selectbox("Tình trạng", ["Available", "Out of Stock", "Discontinued"])
        
        specifications = st.text_area("Thông số kỹ thuật", placeholder="Chi tiết kỹ thuật...")
        storage_conditions = st.text_input("Điều kiện bảo quản", placeholder="2-8°C")
        
        submitted = st.form_submit_button("💾 Lưu sản phẩm", type="primary", use_container_width=True)
        
        if submitted:
            if product_id and product_name and company:
                conn = sqlite3.connect('ivf_products.db')
                c = conn.cursor()
                
                company_id = get_company_id(company)
                app_str = ", ".join(applications)
                
                try:
                    c.execute('''INSERT INTO products 
                                (product_id, product_name, company_id, product_code, category, 
                                subcategory, description, specifications, application_areas, 
                                package_size, list_price, currency, availability_status, 
                                storage_conditions, created_date, updated_date, status)
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                             (product_id, product_name, company_id, product_code, category,
                              subcategory, description, specifications, app_str,
                              package_size, list_price, currency, availability,
                              storage_conditions, datetime.now().isoformat(), 
                              datetime.now().isoformat(), 'Active'))
                    conn.commit()
                    st.success("✅ Đã thêm sản phẩm thành công!")
                except sqlite3.IntegrityError:
                    st.error("❌ Product ID đã tồn tại!")
                finally:
                    conn.close()
            else:
                st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc (*)")

# Hàm thêm công ty
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
                conn = sqlite3.connect('ivf_products.db')
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

# Hàm thống kê
def show_statistics():
    st.markdown("## 📊 Thống kê")
    
    conn = sqlite3.connect('ivf_products.db')
    
    # Thống kê theo danh mục
    st.markdown("### Sản phẩm theo danh mục")
    df_category = pd.read_sql_query(
        "SELECT category, COUNT(*) as count FROM products GROUP BY category", conn)
    st.bar_chart(df_category.set_index('category'))
    
    # Thống kê theo công ty
    st.markdown("### Sản phẩm theo công ty")
    df_company = pd.read_sql_query('''
        SELECT c.company_name, COUNT(p.product_id) as count 
        FROM companies c 
        LEFT JOIN products p ON c.company_id = p.company_id 
        GROUP BY c.company_name
    ''', conn)
    st.bar_chart(df_company.set_index('company_name'))
    
    # Thống kê theo quốc gia
    st.markdown("### Công ty theo quốc gia")
    df_country = pd.read_sql_query(
        "SELECT country, COUNT(*) as count FROM companies GROUP BY country", conn)
    st.bar_chart(df_country.set_index('country'))
    
    conn.close()

# Hàm import/export
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
                    conn = sqlite3.connect('ivf_products.db')
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
            conn = sqlite3.connect('ivf_products.db')
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
            else:
                # Excel export
                st.info("Export Excel - Cần cài đặt openpyxl: pip install openpyxl")

# Hàm hướng dẫn
def show_guide():
    st.markdown("## ℹ️ Hướng dẫn sử dụng")
    
    st.markdown("""
    ### 📚 Hướng dẫn chi tiết
    
    #### 1. Trang chủ
    - Xem tổng quan thống kê hệ thống
    - Duyệt qua các danh mục sản phẩm
    
    #### 2. Tìm kiếm sản phẩm
    - Sử dụng từ khóa để tìm kiếm
    - Lọc theo danh mục, công ty, ứng dụng
    - Xem chi tiết sản phẩm
    
    #### 3. Thêm sản phẩm/công ty
    - Điền đầy đủ thông tin vào form
    - Các trường có dấu (*) là bắt buộc
    - Nhấn "Lưu" để thêm vào database
    
    #### 4. Import/Export
    - Import: Tải lên file CSV/Excel để nhập dữ liệu hàng loạt
    - Export: Xuất dữ liệu ra file để backup hoặc chia sẻ
    
    #### 5. Thống kê
    - Xem biểu đồ thống kê theo nhiều tiêu chí
    - Phân tích xu hướng thị trường
    
    ### 🔧 Yêu cầu kỹ thuật
    - Python 3.8+
    - Streamlit
    - SQLite
    - Pandas
    
    ### 📞 Hỗ trợ
    - Email: support@ivfcatalog.com
    - Hotline: 1900-xxxx
    """)

# Main app
def main():
    # Khởi tạo database
    init_database()
    add_sample_data()
    
    # Hiển thị trang theo navigation
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'search':
        show_search()
    elif st.session_state.page == 'companies':
        show_companies()
    elif st.session_state.page == 'add_product':
        show_add_product()
    elif st.session_state.page == 'add_company':
        show_add_company()
    elif st.session_state.page == 'statistics':
        show_statistics()
    elif st.session_state.page == 'import_export':
        show_import_export()
    elif st.session_state.page == 'guide':
        show_guide()

if __name__ == "__main__":
    main()
