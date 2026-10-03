import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.write("Nhập các thông tin dưới đây để tính toán tiền lãi ngân hàng thu được.")

# Form nhập liệu từ người dùng
with st.form("savings_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        principal = st.number_input(
            "Số tiền gửi (VNĐ):",
            min_value=1_000_000,
            value=100_000_000,
            step=1_000_000,
            format="%d"
        )
        
        term_months = st.number_input(
            "Kỳ hạn gửi (tháng):",
            min_value=1,
            max_value=60,
            value=12,
            step=1
        )

    with col2:
        annual_rate = st.number_input(
            "Lãi suất (%/năm):",
            min_value=0.1,
            max_value=20.0,
            value=6.0,
            step=0.1,
            format="%.2f"
        )
        
        payout_option = st.selectbox(
            "Hình thức nhận lãi:",
            options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
        )

    submit_button = st.form_submit_button("Tính lãi", use_container_width=True)

# Tính toán kết quả khi nhấn nút hoặc khởi tạo
if submit_button or principal:
    # 1. Tính tổng tiền lãi cơ bản (Tính theo ngày chuẩn 365/năm hoặc theo kỳ tháng)
    # Lãi cơ bản cả kỳ = (Số tiền * Lãi suất năm / 12) * Số tháng
    total_interest = principal * (annual_rate / 100) * (term_months / 12)

    # 2. Xử lý theo từng hình thức nhận lãi
    if payout_option == "Cuối kỳ":
        periodic_interest = total_interest
        payout_label = "Tiền lãi nhận khi đáo hạn"
    elif payout_option == "Hàng tháng":
        periodic_interest = principal * (annual_rate / 100) / 12
        payout_label = "Tiền lãi nhận mỗi tháng"
    elif payout_option == "Hàng quý":
        periodic_interest = principal * (annual_rate / 100) / 4
        payout_label = "Tiền lãi nhận mỗi quý (3 tháng)"

    total_payout = principal + total_interest

    st.markdown("---")
    st.subheader("📊 Kết Quả Tính Toán")

    # Hiển thị số liệu dạng Metric
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric(
            label=payout_label,
            value=f"{periodic_interest:,.0f} VNĐ"
        )
    with m2:
        st.metric(
            label="Tổng tiền lãi",
            value=f"{total_interest:,.0f} VNĐ"
        )
    with m3:
        st.metric(
            label="Tổng tiền gốc + lãi",
            value=f"{total_payout:,.0f} VNĐ"
        )

    # Bảng chi tiết tóm tắt
    st.markdown("### 📋 Tóm tắt giao dịch")
    st.table({
        "Thông tin": ["Số tiền gửi ban đầu", "Kỳ hạn", "Lãi suất năm", "Hình thức nhận lãi", "Tổng số tiền nhận về"],
        "Giá trị": [
            f"{principal:,.0f} VNĐ",
            f"{term_months} tháng",
            f"{annual_rate:.2f}%",
            payout_option,
            f"{total_payout:,.0f} VNĐ"
        ]
    })
