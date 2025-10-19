import streamlit as st
import datetime

# -----------------------------
# Users database
# -----------------------------
users_db = {
    "admin": "1234",
    "user1": "1111",
    "user2": "2222"
}

# -----------------------------
# Menu items with prices
# -----------------------------
menu = {
    "Pizza": {"Full": 200, "Half": 120},
    "Chicken Tandoori": {"Full": 450, "Half": 300},
    "Paneer Butter Masala": {"Full": 180, "Half": 110},
    "Fried Rice": {"Full": 150, "Half": 90},
    "Chicken Fried Rice": {"Full": 180, "Half": 100}
}

# -----------------------------
# Initialize session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "order_items" not in st.session_state:
    st.session_state.order_items = []

if "discount" not in st.session_state:
    st.session_state.discount = 0

if "gst" not in st.session_state:
    st.session_state.gst = 0

# -----------------------------
# Login Page
# -----------------------------
def login_page():
    st.title("🍴 Restaurant Billing - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users_db and users_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password!")

# -----------------------------
# Billing Page
# -----------------------------
def billing_page():
    st.title(f"🍴 Restaurant Billing - User: {st.session_state.current_user}")

    # Input row
    col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
    with col1:
        item_name = st.selectbox("Select Item", list(menu.keys()))
    with col2:
        item_type = st.selectbox("Type", ["Full","Half"])
    with col3:
        qty = st.number_input("Quantity", min_value=1, value=1, step=1)
    with col4:
        st.session_state.discount = st.number_input("Discount %", min_value=0, value=0)
    with col5:
        st.session_state.gst = st.number_input("GST %", min_value=0, value=0)

    # Add item button
    if st.button("Add Item"):
        price = menu[item_name][item_type]
        total = price * qty
        st.session_state.order_items.append({
            "item": item_name,
            "type": item_type,
            "qty": qty,
            "total": total
        })
        st.success(f"Added {item_name} ({item_type}) x {qty}")

    # Show current order
    if st.session_state.order_items:
        st.subheader("Order Items")
        for i, order in enumerate(st.session_state.order_items):
            st.write(f"{i+1}. {order['item']} ({order['type']}) x {order['qty']} = ₹{order['total']}")

        # Delete item
        delete_index = st.number_input("Enter item number to delete", min_value=1,
                                       max_value=len(st.session_state.order_items), step=1)
        if st.button("Delete Item"):
            removed_item = st.session_state.order_items.pop(delete_index-1)
            st.success(f"Removed {removed_item['item']} ({removed_item['type']}) x {removed_item['qty']}")

    # Calculate total
    total_amount = sum([o["total"] for o in st.session_state.order_items])
    discounted = total_amount - (total_amount * st.session_state.discount / 100)
    gst_total = discounted + (discounted * st.session_state.gst / 100)
    st.subheader(f"Total (after discount & GST): ₹{gst_total:.2f}")

    # Generate bill text
    if st.session_state.order_items:
        bill_text = f"🍴 Restaurant Billing - User: {st.session_state.current_user}\n"
        bill_text += f"Bill Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_text += "==============================\n"
        for order in st.session_state.order_items:
            bill_text += f"{order['item']} ({order['type']}) x {order['qty']} = ₹{order['total']}\n"
        bill_text += "==============================\n"
        bill_text += f"Discount: {st.session_state.discount}%\nGST: {st.session_state.gst}%\n"
        bill_text += f"Total: ₹{gst_total:.2f}\n"
        bill_text += "==============================\nThank you! Visit Again 🙏\n"

        # Show bill in browser
        st.subheader("Generated Bill")
        st.text(bill_text)

        # ✅ Corrected download button
        st.download_button(
            "💾 Download Bill",
            data=bill_text,  # Pass string directly
            file_name=f"bill_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # Print instructions
        st.info("To print the bill, use your browser's Print option (Ctrl+P or Cmd+P).")

# -----------------------------
# Main
# -----------------------------
def main():
    if st.session_state.logged_in:
        billing_page()
    else:
        login_page()

main()
