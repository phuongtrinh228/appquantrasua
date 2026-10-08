import streamlit as st
from datetime import datetime
from io import BytesIO

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Trà Sữa POS",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# DỮ LIỆU MENU
# Bạn có thể sửa giá ở đây
# =========================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa caramel": 38000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Trà tắc": 25000,
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000,
    "XL": 10000
}

TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Trân châu + pudding": 10000
}

SUGAR_LEVELS = [
    "0% đường",
    "30% đường",
    "50% đường",
    "70% đường",
    "100% đường"
]

ICE_LEVELS = [
    "Không đá",
    "30% đá",
    "50% đá",
    "70% đá",
    "100% đá"
]

# =========================================================
# KHỞI TẠO SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def format_money(number):
    return f"{number:,.0f}đ".replace(",", ".")


def calculate_item_price(drink, size, topping):
    return (
        MENU[drink]
        + SIZE_PRICE[size]
        + TOPPING_PRICE[topping]
    )


def create_invoice_text(invoice):
    lines = []

    lines.append("=" * 50)
    lines.append("             TRÀ SỮA POS")
    lines.append("             HÓA ĐƠN THANH TOÁN")
    lines.append("=" * 50)

    lines.append(f"Khách hàng: {invoice['customer_name']}")
    lines.append(f"Thời gian: {invoice['time']}")
    lines.append(f"Mã hóa đơn: {invoice['invoice_id']}")
    lines.append("-" * 50)

    for i, item in enumerate(invoice["items"], 1):
        lines.append(
            f"{i}. {item['drink']} - Size {item['size']}"
        )
        lines.append(
            f"   Topping: {item['topping']}"
        )
        lines.append(
            f"   Đường: {item['sugar']} | Đá: {item['ice']}"
        )
        lines.append(
            f"   SL: {item['quantity']} x "
            f"{format_money(item['unit_price'])}"
        )
        lines.append(
            f"   Thành tiền: {format_money(item['total'])}"
        )

    lines.append("-" * 50)
    lines.append(
        f"TỔNG CỘNG: {format_money(invoice['total'])}"
    )
    lines.append("=" * 50)
    lines.append("       Cảm ơn quý khách! 🧋")
    lines.append("=" * 50)

    return "\n".join(lines)


# =========================================================
# HEADER
# =========================================================

st.title("🧋 TRÀ SỮA POS")
st.caption("Ứng dụng quản lý và tính tiền hóa đơn trà sữa")

st.divider()


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

col1, col2 = st.columns([2, 1])

with col1:
    customer_name = st.text_input(
        "👤 Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng..."
    )

with col2:
    if st.session_state.paid:
        st.success("✅ Hóa đơn đã thanh toán")


st.divider()


# =========================================================
# KHU VỰC CHỌN MÓN
# =========================================================

st.subheader("🧋 Thêm món")

if not st.session_state.paid:

    col1, col2, col3 = st.columns(3)

    with col1:
        drink = st.selectbox(
            "Loại trà sữa / nước",
            list(MENU.keys())
        )

    with col2:
        size = st.selectbox(
            "Size",
            list(SIZE_PRICE.keys())
        )

    with col3:
        topping = st.selectbox(
            "Topping",
            list(TOPPING_PRICE.keys())
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        sugar = st.selectbox(
            "Mức độ đường",
            SUGAR_LEVELS
        )

    with col5:
        ice = st.selectbox(
            "Mức độ đá",
            ICE_LEVELS
        )

    with col6:
        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=50,
            value=1,
            step=1
        )

    unit_price = calculate_item_price(
        drink,
        size,
        topping
    )

    total_item_price = unit_price * quantity

    st.info(
        f"💰 Đơn giá: **{format_money(unit_price)}**  "
        f"| Thành tiền: **{format_money(total_item_price)}**"
    )

    if st.button(
        "➕ Thêm món vào hóa đơn",
        use_container_width=True
    ):

        if not customer_name.strip():
            st.warning("⚠️ Vui lòng nhập tên khách hàng.")
        else:

            item = {
                "drink": drink,
                "size": size,
                "topping": topping,
                "sugar": sugar,
                "ice": ice,
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total_item_price
            }

            st.session_state.cart.append(item)
            st.session_state.customer_name = customer_name

            st.success(
                f"Đã thêm {quantity} x {drink} vào hóa đơn!"
            )

            st.rerun()


# =========================================================
# GIỎ HÀNG
# =========================================================

st.divider()

st.subheader("🧾 Danh sách món trong hóa đơn")

if len(st.session_state.cart) == 0:

    st.info(
        "Chưa có món nào. Hãy chọn món ở phía trên và bấm "
        "'Thêm món vào hóa đơn'."
    )

else:

    grand_total = 0

    for index, item in enumerate(st.session_state.cart):

        col1, col2, col3, col4 = st.columns(
            [3, 2, 2, 1]
        )

        with col1:
            st.markdown(
                f"**{index + 1}. {item['drink']}**  \n"
                f"Size {item['size']} • "
                f"{item['topping']}  \n"
                f"Đường: {item['sugar']} • "
                f"Đá: {item['ice']}"
            )

        with col2:
            st.write(
                f"Số lượng: **{item['quantity']}**"
            )

        with col3:
            st.write(
                f"**{format_money(item['total'])}**"
            )

        with col4:
            if not st.session_state.paid:
                if st.button(
                    "🗑️",
                    key=f"delete_{index}"
                ):
                    st.session_state.cart.pop(index)
                    st.rerun()

        grand_total += item["total"]

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write(
            f"**Tổng số món:** "
            f"{sum(item['quantity'] for item in st.session_state.cart)}"
        )

    with col2:
        st.markdown(
            f"### Tổng tiền: {format_money(grand_total)}"
        )


# =========================================================
# THANH TOÁN
# =========================================================

if (
    len(st.session_state.cart) > 0
    and not st.session_state.paid
):

    st.divider()

    st.subheader("💳 Thanh toán")

    col1, col2 = st.columns(2)

    with col1:
        payment_method = st.selectbox(
            "Phương thức thanh toán",
            [
                "Tiền mặt",
                "Chuyển khoản",
                "Thẻ ngân hàng"
            ]
        )

    with col2:
        st.metric(
            "Số tiền cần thanh toán",
            format_money(grand_total)
        )

    if st.button(
        "💰 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        now = datetime.now()

        invoice = {
            "invoice_id": now.strftime("%Y%m%d%H%M%S"),
            "customer_name": customer_name,
            "time": now.strftime("%d/%m/%Y %H:%M:%S"),
            "items": st.session_state.cart.copy(),
            "total": grand_total,
            "payment_method": payment_method
        }

        st.session_state.invoice = invoice
        st.session_state.paid = True

        st.rerun()


# =========================================================
# HIỂN THỊ HÓA ĐƠN SAU KHI THANH TOÁN
# =========================================================

if st.session_state.paid and st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()

    st.success("🎉 Thanh toán thành công!")

    st.subheader("🧾 HÓA ĐƠN")

    st.markdown(
        f"""
        ### 🧋 TRÀ SỮA POS

        **Mã hóa đơn:** {invoice['invoice_id']}  
        **Khách hàng:** {invoice['customer_name']}  
        **Thời gian:** {invoice['time']}  
        **Thanh toán:** {invoice['payment_method']}
        """
    )

    st.divider()

    for i, item in enumerate(invoice["items"], 1):

        st.markdown(
            f"""
            **{i}. {item['drink']} - Size {item['size']}**

            - Topping: {item['topping']}
            - Đường: {item['sugar']}
            - Đá: {item['ice']}
            - Số lượng: {item['quantity']}
            - Đơn giá: {format_money(item['unit_price'])}
            - Thành tiền: **{format_money(item['total'])}**
            """
        )

    st.divider()

    st.markdown(
        f"## 💰 TỔNG CỘNG: {format_money(invoice['total'])}"
    )

    # =====================================================
    # XUẤT HÓA ĐƠN
    # =====================================================

    invoice_text = create_invoice_text(invoice)

    st.download_button(
        label="📥 Xuất hóa đơn",
        data=invoice_text.encode("utf-8"),
        file_name=f"hoa_don_{invoice['invoice_id']}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.divider()

    if st.button(
        "🆕 Tạo hóa đơn mới",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.invoice = None
        st.session_state.customer_name = ""

        st.rerun()
