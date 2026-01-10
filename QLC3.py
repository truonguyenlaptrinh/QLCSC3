import streamlit as st
import pandas as pd
from datetime import datetime
import os
import qrcode
from io import BytesIO
import socket

# Cấu hình trang
st.set_page_config(
    page_title="PHẦN MỀM ĐĂNG KÝ, QUẢN LÝ THĂM TIẾP KHÁCH",
    page_icon="🇻🇳",
    layout="centered"
)

# CSS giao diện + marquee
st.markdown(
    """
    <style>
    /* Nền trắng */
    .stApp {
        background-color: #ffffff !important;
        background-image: none !important;
    }

    /* Khối nội dung chính */
    .main .block-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

        /* Chừa khoảng trống để không bị che bởi dòng chữ chạy */
        padding-top: 95px !important;
    }

    /* Màu heading chung */
    h1, h2, h3, h4, h5, h6 {
        color: #c41e3a !important;
        font-weight: bold;
    }

    /* H1 chung */
    h1 {
        text-align: center;
        border-bottom: 3px solid #006400;
        padding-bottom: 10px;
    }

    /* Tiêu đề chính (xanh lá đậm #006400) */
    .main-title { color: #006400 !important; font-weight: 900 !important; }
    h1.main-title { color: #006400 !important; font-weight: 900 !important; }

    p, label, .stMarkdown { color: #333333 !important; }

    .stTextInput label, .stSelectbox label, .stNumberInput label,
    .stDateInput label, .stTimeInput label {
        color: #c41e3a !important;
        font-weight: 600;
    }

    .stTextInput input, .stSelectbox select, .stNumberInput input,
    .stDateInput input, .stTimeInput input {
        color: #333333 !important;
        background-color: #ffffff !important;
        border: 2px solid #c41e3a !important;
        border-radius: 5px;
    }

    .stSelectbox select option { color: #333333 !important; }

    .stButton > button {
        background-color: #c41e3a !important;
        color: white !important;
        border: none !important;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover { background-color: #a01a2e !important; }

    .stDataFrame { color: #333333 !important; }

    div[data-testid="stMetricValue"] {
        color: #c41e3a !important;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] { color: #666666 !important; }

    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-left: 4px solid #28a745;
    }
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 4px solid #dc3545;
    }
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 4px solid #ffc107;
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-left: 4px solid #17a2b8;
    }

    .stSidebar { background-color: #f8f9fa; }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 { color: #c41e3a !important; }

    /* ===== DÒNG CHỮ CHẠY TRÊN CÙNG (NỀN ĐỎ - CHỮ VÀNG) ===== */
    .marquee-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #c41e3a;        /* NỀN ĐỎ */
        padding: 12px 0;
        z-index: 999;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.35);
        border-bottom: 3px solid #FFD700; /* viền vàng */
    }

    .marquee-text {
        display: inline-block;
        color: #FFD700;                   /* CHỮ VÀNG */
        font-size: 32px;
        font-weight: 900;
        white-space: nowrap;
        letter-spacing: 3px;
        text-transform: uppercase;
        animation: marquee-right-to-left 18s linear infinite; /* chạy liên tục */
    }

    @keyframes marquee-right-to-left {
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Box liên hệ */
    .contact-info-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 3px solid #c41e3a;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .contact-info-title {
        color: #c41e3a;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        text-transform: uppercase;
        border-bottom: 2px solid #c41e3a;
        padding-bottom: 10px;
    }
    .contact-info-content { color: #333333; line-height: 1.8; font-size: 16px; }
    .contact-info-name { font-weight: bold; color: #c41e3a; font-size: 18px; margin: 10px 0; }
    .contact-info-detail { margin: 8px 0; padding-left: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Khởi tạo session state cho admin
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Khởi tạo session state cho URL QR code
if "qr_url" not in st.session_state:
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if local_ip == "127.0.0.1" or local_ip.startswith("127."):
            st.session_state.qr_url = "http://localhost:8501"
        else:
            st.session_state.qr_url = f"http://{local_ip}:8501"
    except Exception:
        st.session_state.qr_url = "http://localhost:8501"


def generate_qr_code(url: str) -> BytesIO:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer


# Sidebar cho máy chủ/admin
with st.sidebar:
    st.header("📱 Mã QR truy cập")
    st.markdown("---")

    try:
        qr_image = generate_qr_code(st.session_state.qr_url)
        st.image(qr_image, caption="Quét mã QR để truy cập", use_container_width=True)
        st.caption(f"URL: {st.session_state.qr_url}")

        if st.session_state.is_admin:
            with st.expander("⚙️ Cấu hình URL"):
                new_url = st.text_input(
                    "Nhập URL mới:",
                    value=st.session_state.qr_url,
                    help="Nhập URL đầy đủ (ví dụ: http://192.168.1.100:8501)",
                )
                if st.button("Cập nhật URL", use_container_width=True):
                    if new_url and new_url.startswith(("http://", "https://")):
                        st.session_state.qr_url = new_url
                        st.success("✅ Đã cập nhật URL!")
                        st.rerun()
                    else:
                        st.error("⚠️ URL không hợp lệ! Phải bắt đầu bằng http:// hoặc https://")
    except Exception as e:
        st.error(f"Lỗi tạo mã QR: {str(e)}")

    st.markdown("---")
    st.header("🛡️ Chế độ máy chủ")
    st.markdown("---")

    if st.session_state.is_admin:
        st.success("✅ Đã đăng nhập với tư cách máy chủ")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()
    else:
        with st.form("admin_login_form"):
            admin_password = st.text_input("🔐 Mật khẩu máy chủ", type="password", help="Mật khẩu mặc định: admin123")
            login_button = st.form_submit_button("🔑 Đăng nhập", use_container_width=True)

            if login_button:
                if admin_password == "admin123":
                    st.session_state.is_admin = True
                    st.rerun()
                elif admin_password == "":
                    st.warning("⚠️ Vui lòng nhập mật khẩu!")
                else:
                    st.error("❌ Mật khẩu không đúng!")


# Dòng chữ chạy trên cùng
st.markdown(
    """
    <div class="marquee-container">
        <div class="marquee-text">ĐOÀN KẾT - XÂY DỰNG GIỎI - ĐI TỐT - ĐÁNH THẮNG</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Tiêu đề ứng dụng
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 class="main-title">PHẦN MỀM ĐĂNG KÝ, QUẢN LÝ THĂM TIẾP KHÁCH</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

DATA_FILE = "dang_ky_tham.csv"


def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(
            columns=[
                "Họ và tên",
                "Họ và tên chiến sĩ",
                "Mối quan hệ",
                "Số lượng khách",
                "Đơn vị",
                "Thời gian",
                "Ngày đăng ký",
            ]
        )
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    return pd.DataFrame(
        columns=[
            "Họ và tên",
            "Họ và tên chiến sĩ",
            "Mối quan hệ",
            "Số lượng khách",
            "Đơn vị",
            "Thời gian",
            "Ngày đăng ký",
        ]
    )


def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


init_data_file()

# Form đăng ký
with st.form("form_dang_ky", clear_on_submit=True):
    st.subheader("📝 Điền thông tin đăng ký")
    st.markdown("---")

    ho_ten = st.text_input("👤 Họ và tên *", placeholder="Nhập họ và tên của bạn")
    ten_chien_si = st.text_input("🪖 Họ và tên chiến sĩ *", placeholder="Nhập họ và tên chiến sĩ cần thăm")
    moi_quan_he = st.text_input(
        "👨‍👩‍👧‍👦 Mối quan hệ với chiến sĩ *",
        placeholder="Nhập mối quan hệ (ví dụ: Bố, Mẹ, Anh, Chị...)",
    )
    so_luong_khach = st.number_input("👥 Số lượng khách *", min_value=1, max_value=50, value=1, step=1)
    don_vi = st.selectbox("🏛️ Đơn vị *", ["Trung đội 7", "Trung đội 8", "Trung đội 9", "Tiểu đội Đại liên", "Tiểu đội Co60"])

    col1, col2 = st.columns(2)
    with col1:
        ngay = st.date_input("📅 Ngày thăm *", min_value=datetime.now().date())
    with col2:
        gio = st.time_input("🕐 Giờ thăm *", value=datetime.now().time())

    thoi_gian = f"{ngay.strftime('%d/%m/%Y')} - {gio.strftime('%H:%M')}"

    submitted = st.form_submit_button("✅ Đăng ký", use_container_width=True)

    if submitted:
        if not ho_ten or not ten_chien_si or not moi_quan_he or not so_luong_khach or not don_vi:
            st.error("⚠️ Vui lòng điền đầy đủ thông tin bắt buộc (*)")
        else:
            df = load_data()
            new_row = {
                "Họ và tên": ho_ten,
                "Họ và tên chiến sĩ": ten_chien_si,
                "Mối quan hệ": moi_quan_he,
                "Số lượng khách": int(so_luong_khach),
                "Đơn vị": don_vi,
                "Thời gian": thoi_gian,
                "Ngày đăng ký": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)

            st.success("✅ Đăng ký thành công!")
            st.balloons()

# Hiển thị danh sách đăng ký (chỉ dành cho máy chủ)
if st.session_state.is_admin:
    st.markdown("---")
    st.subheader("📋 Danh sách đăng ký")
    st.markdown("---")

    df = load_data()

    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Xóa tất cả dữ liệu", use_container_width=True):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.success("✅ Đã xóa tất cả dữ liệu!")
                st.rerun()

        st.markdown("---")
        st.subheader("📊 Thống kê tổng quan")

        st.markdown(
            """
            <style>
            .white-bg-table {
                background-color: white !important;
                color: black !important;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .white-bg-table table {
                background-color: white !important;
                color: black !important;
                width: 100%;
            }
            .white-bg-table table th {
                background-color: #f0f0f0 !important;
                color: black !important;
                padding: 10px;
                text-align: left;
            }
            .white-bg-table table td {
                background-color: white !important;
                color: black !important;
                padding: 8px;
            }
            .white-bg-metric {
                background-color: white !important;
                color: black !important;
                padding: 15px;
                border-radius: 10px;
                margin: 5px;
            }
            .white-bg-metric div[data-testid="stMetricValue"] { color: black !important; }
            .white-bg-metric div[data-testid="stMetricLabel"] { color: black !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="white-bg-metric">', unsafe_allow_html=True)
            st.metric("📝 Tổng số đăng ký", len(df))
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="white-bg-metric">', unsafe_allow_html=True)
            st.metric("🪖 Số chiến sĩ", df["Họ và tên chiến sĩ"].nunique())
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="white-bg-metric">', unsafe_allow_html=True)
            st.metric("🏛️ Số đơn vị", df["Đơn vị"].nunique())
            st.markdown("</div>", unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="white-bg-metric">', unsafe_allow_html=True)
            tong_khach = df["Số lượng khách"].sum() if "Số lượng khách" in df.columns else 0
            st.metric("👥 Tổng số khách", int(tong_khach))
            st.markdown("</div>", unsafe_allow_html=True)

        if "sort_option" not in st.session_state:
            st.session_state.sort_option = "📅 Theo thời gian thăm"

        def parse_thoi_gian(thoi_gian_str: str):
            try:
                date_part = thoi_gian_str.split(" - ")[0]
                return datetime.strptime(date_part, "%d/%m/%Y")
            except Exception:
                return datetime.min

        def parse_ngay_dang_ky(ngay_str: str):
            try:
                date_part = ngay_str.split(" ")[0]
                return datetime.strptime(date_part, "%d/%m/%Y")
            except Exception:
                return datetime.min

        df_sorted = df.copy()
        df_sorted["Thời gian_sort"] = df_sorted["Thời gian"].apply(parse_thoi_gian)
        df_sorted["Ngày đăng ký_sort"] = df_sorted["Ngày đăng ký"].apply(parse_ngay_dang_ky)

        st.markdown("### 📋 Danh sách đăng ký chi tiết")
        sort_options = [
            "📅 Theo thời gian thăm",
            "🏛️ Theo đơn vị",
            "👤 Theo tên người đăng ký",
            "🪖 Theo tên chiến sĩ",
            "⏰ Theo ngày đăng ký",
        ]

        selected_sort = st.selectbox(
            "🔀 Sắp xếp theo:",
            sort_options,
            index=sort_options.index(st.session_state.sort_option)
            if st.session_state.sort_option in sort_options
            else 0,
            key="sort_selectbox",
        )
        st.session_state.sort_option = selected_sort

        if "Theo thời gian thăm" in selected_sort:
            df_display = df_sorted.sort_values("Thời gian_sort")
        elif "Theo đơn vị" in selected_sort:
            df_display = df_sorted.sort_values(["Đơn vị", "Thời gian_sort"])
        elif "Theo tên người đăng ký" in selected_sort:
            df_display = df_sorted.sort_values("Họ và tên")
        elif "Theo tên chiến sĩ" in selected_sort:
            df_display = df_sorted.sort_values("Họ và tên chiến sĩ")
        elif "Theo ngày đăng ký" in selected_sort:
            df_display = df_sorted.sort_values("Ngày đăng ký_sort", ascending=False)
        else:
            df_display = df_sorted

        df_display = df_display.drop(columns=["Thời gian_sort", "Ngày đăng ký_sort"])

        def display_white_table(df_to_show: pd.DataFrame):
            html_table = df_to_show.to_html(index=False, escape=False, classes="white-bg-table")
            html_table = html_table.replace(
                "<table",
                '<table style="background-color: white; color: black; width: 100%;">',
            )
            html_table = html_table.replace(
                "<th>",
                '<th style="background-color: #f0f0f0; color: black; padding: 10px; text-align: left;">',
            )
            html_table = html_table.replace(
                "<td>",
                '<td style="background-color: white; color: black; padding: 8px;">',
            )
            st.markdown(f'<div class="white-bg-table">{html_table}</div>', unsafe_allow_html=True)

        display_white_table(df_display)

        st.markdown("---")
        st.markdown("### 📈 Thống kê theo đơn vị")
        unit_stats = (
            df.groupby("Đơn vị")
            .agg({"Họ và tên": "count", "Họ và tên chiến sĩ": "nunique", "Số lượng khách": "sum"})
            .reset_index()
        )
        unit_stats.columns = ["Đơn vị", "Số lượt đăng ký", "Số chiến sĩ", "Tổng số khách"]
        display_white_table(unit_stats)
    else:
        st.info("📭 Chưa có đăng ký nào. Hãy đăng ký thăm chiến sĩ ở form phía trên.")

# Thông tin liên hệ
st.markdown("---")
st.markdown(
    """
    <div class="contact-info-box">
        <div class="contact-info-title">THÔNG TIN LIÊN HỆ</div>
        <div class="contact-info-content">
            <div class="contact-info-name">Đồng chí NGUYỄN VĂN TRƯỜNG</div>
            <div class="contact-info-detail"><strong>Đơn vị:</strong> Đại đội 3, Tiểu đoàn 4</div>
            <div class="contact-info-detail"><strong>Chức vụ:</strong> Chính trị viên phó Đại đội</div>
            <div class="contact-info-detail"><strong>SĐT:</strong> 0362876113</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
