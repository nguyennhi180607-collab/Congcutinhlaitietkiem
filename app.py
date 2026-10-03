import streamlit as st
import pandas as pd

# ==========================================
# 1. CẤU HÌNH TRANG (BẮT BUỘC ĐẶT Ở ĐẦU)
# ==========================================
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="🏦",
    layout="centered"
)

# Hiển thị Logo (tự động bỏ qua nếu chưa có file logo.jpg)
try:
    st.image("logo.jpg", width=150)
except Exception:
    pass

st.title("🏦 Công Cụ Tính Lãi Gửi Tiết Kiệm - Nguyễn Thị Yến Nhi❤️️")
st.write("Nhập các thông tin dưới đây để tính toán tiền lãi ngân hàng thu được.")

# ==========================================
# 2. BẢNG LÃI SUẤT THEO KỲ HẠN
# ==========================================
RATE_DICT = {
    1: 3.80,
    3: 4.50,
    6: 6.20,
    9: 6.60,
    12: 7.50,
    18: 7.90,
    24: 8.20,
    36: 8.80
}

def get_suggested_rate(months):
    """Tự động khớp mức lãi suất dựa trên số tháng gửi"""
    if months in RATE_DICT:
        return RATE_DICT[months]
    elif months < 3:
        return 3.80
    elif months < 6:
        return 4.50
    elif months < 9:
        return 6.20
    elif months < 12:
        return 6.60
    elif months < 18:
        return 7.50
    elif months < 24:
        return 7.90
    elif months < 36:
        return 8.20
    else:
        return 8.80

# Hàm callback tự động cập nhật lãi suất khi thay đổi kỳ hạn
def update_rate_by_term():
    st.session_state.annual_rate = get_suggested_rate(st.session_state.term_months)

# Khởi tạo giá trị ban đầu cho session_state
if "term_months" not in st.session_state:
    st.session_state.term_months = 12
if "annual_rate" not in st.session_state:
    st.session_state.annual_rate = get_suggested_rate(st.session_state.term_months)

# ==========================================
# 3. HIỂN THỊ BẢNG LÃI SUẤT Ở SIDEBAR
# ==========================================
st.sidebar.header("📌 Bảng Lãi Suất Ưu Đãi")
df_rates = pd.DataFrame({
    "Kỳ hạn": [f"{m} tháng" for m in RATE_DICT.keys()],
    "Lãi suất (%/năm)": [f"{r:.2f}%" for r in RATE_DICT.values()]
})
st.sidebar.dataframe(df_rates, use_container_width=True, hide_index=True)

# ==========================================
# 4. KHU VỰC NHẬP LIỆU
# ==========================================
col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "1. Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=5_000_000,
        format="%d"
    )
    
    term_months = st.number_input(
        "2. Kỳ hạn gửi (tháng):",
        min_value=1,
        max_value=60,
        key="term_months",
        on_change=update_rate_by_term,
        step=1
    )

    interest_type = st.radio(
        "3. Loại hình tính lãi:",
        options=["Lãi đơn", "Lãi kép (Lãi nhập gốc)"],
        help="Lãi đơn: Lãi cố định trên gốc ban đầu. Lãi kép: Lãi mỗi kỳ cộng vào gốc để tính lãi kỳ sau."
    )

with col2:
    annual_rate = st.number_input(
        "4. Lãi suất (%/năm) - *Tự động chọn*:",
        min_value=0.1,
        max_value=20.0,
        key="annual_rate",
        step=0.1,
        format="%.2f"
    )
    
    payout_option = st.selectbox(
        "5. Hình thức nhận lãi:",
        options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
    )

st.caption(f"💡 *Lãi suất áp dụng tự động cho kỳ hạn **{term_months} tháng** là **{annual_rate:.2f}%/năm**. Bạn vẫn có thể tùy chỉnh lại con số này.*")

# ==========================================
# 5. TÍNH TOÁN KẾT QUẢ
# ==========================================
r_monthly = (annual_rate / 100) / 12
r_quarterly = (annual_rate / 100) / 4

schedule = []

if interest_type == "Lãi đơn":
    # ----- TÍNH LÃI ĐƠN -----
    total_interest = principal * (annual_rate / 100) * (term_months / 12)
    total_payout = principal + total_interest

    if payout_option == "Cuối kỳ":
        periodic_interest = total_interest
        payout_label = "Lãi nhận khi đáo hạn"
    elif payout_option == "Hàng tháng":
        periodic_interest = principal * r_monthly
        payout_label = "Lãi nhận mỗi tháng"
        for m in range(1, term_months + 1):
            schedule.append({
                "Kỳ": f"Tháng {m}",
                "Gốc đầu kỳ (VNĐ)": f"{principal:,.0f}",
                "Lãi kỳ này (VNĐ)": f"{periodic_interest:,.0f}",
                "Lãi lũy kế (VNĐ)": f"{(periodic_interest * m):,.0f}"
            })
    elif payout_option == "Hàng quý":
        periodic_interest = principal * r_quarterly
        payout_label = "Lãi nhận mỗi quý"
        num_quarters = int(term_months // 3)
        for q in range(1, num_quarters + 1):
            schedule.append({
                "Kỳ": f"Quý {q} (Tháng {q*3})",
                "Gốc đầu kỳ (VNĐ)": f"{principal:,.0f}",
                "Lãi kỳ này (VNĐ)": f"{periodic_interest:,.0f}",
                "Lãi lũy kế (VNĐ)": f"{(periodic_interest * q):,.0f}"
            })

else:
    # ----- TÍNH LÃI KÉP (LÃI NHẬP GỐC) -----
    current_principal = float(principal)
    
    if payout_option == "Hàng tháng":
        for m in range(1, term_months + 1):
            interest_period = current_principal * r_monthly
            schedule.append({
                "Kỳ": f"Tháng {m}",
                "Gốc đầu kỳ (VNĐ)": f"{current_principal:,.0f}",
                "Lãi kỳ này (VNĐ)": f"{interest_period:,.0f}",
                "Gốc + Lãi cuối kỳ (VNĐ)": f"{(current_principal + interest_period):,.0f}"
            })
            current_principal += interest_period
        
        total_payout = current_principal
        total_interest = total_payout - principal
        periodic_interest = principal * r_monthly
        payout_label = "Lãi tháng đầu tiên"

    elif payout_option == "Hàng quý":
        num_quarters = int(term_months // 3)
        for q in range(1, num_quarters + 1):
            interest_period = current_principal * r_quarterly
            schedule.append({
                "Kỳ": f"Quý {q} (Tháng {q*3})",
                "Gốc đầu kỳ (VNĐ)": f"{current_principal:,.0f}",
                "Lãi kỳ này (VNĐ)": f"{interest_period:,.0f}",
                "Gốc + Lãi cuối kỳ (VNĐ)": f"{(current_principal + interest_period):,.0f}"
            })
            current_principal += interest_period
        
        remaining_months = term_months % 3
        if remaining_months > 0:
            interest_period = current_principal * r_monthly * remaining_months
            schedule.append({
                "Kỳ": f"Lẻ {remaining_months} tháng cuối",
                "Gốc đầu kỳ (VNĐ)": f"{current_principal:,.0f}",
                "Lãi kỳ này (VNĐ)": f"{interest_period:,.0f}",
                "Gốc + Lãi cuối kỳ (VNĐ)": f"{(current_principal + interest_period):,.0f}"
            })
            current_principal += interest_period

        total_payout = current_principal
        total_interest = total_payout - principal
        periodic_interest = principal * r_quarterly
        payout_label = "Lãi quý đầu tiên"

    else:  # Cuối kỳ (Ghép lãi hàng năm)
        years = term_months / 12
        total_payout = principal * ((1 + (annual_rate / 100)) ** years)
        total_interest = total_payout - principal
        periodic_interest = total_interest
        payout_label = "Tổng lãi nhận khi đáo hạn"

# ==========================================
# 6. HIỂN THỊ KẾT QUẢ TÍNH TOÁN
# ==========================================
st.markdown("---")
st.subheader(f"📊 Kết Quả Tính Toán ({interest_type})")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label=payout_label, value=f"{periodic_interest:,.0f} VNĐ")
with m2:
    st.metric(label="Tổng tiền lãi nhận được", value=f"{total_interest:,.0f} VNĐ")
with m3:
    st.metric(label="Tổng gốc + lãi thu về", value=f"{total_payout:,.0f} VNĐ")

# Bảng tóm tắt giao dịch
st.markdown("### 📋 Tóm tắt giao dịch")
st.table({
    "Thông tin": [
        "Số tiền gửi ban đầu", 
        "Kỳ hạn gửi", 
        "Lãi suất áp dụng", 
        "Phương pháp tính", 
        "Hình thức nhận lãi", 
        "Tổng tiền thực nhận"
    ],
    "Giá trị": [
        f"{principal:,.0f} VNĐ",
        f"{term_months} tháng",
        f"{annual_rate:.2f}% / năm",
        interest_type,
        payout_option,
        f"{total_payout:,.0f} VNĐ"
    ]
})

# Bảng lịch trình chi tiết nếu có
if schedule:
    st.markdown("### 📈 Lịch trình chi tiết từng kỳ")
    st.dataframe(pd.DataFrame(schedule), use_container_width=True, hide_index=True)
