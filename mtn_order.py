import streamlit as st
from datetime import datetime
import pandas as pd

# Initialize all session state variables
def initialize_session_state():
    if 'orders' not in st.session_state:
        st.session_state.orders = []
    if 'products' not in st.session_state:
        st.session_state.products = [
            {"id": 1, "name": "MTN Mobile Data 1GB", "price": 10.00, "category": "Data Bundles", "available": True},
            {"id": 2, "name": "MTN Mobile Data 3GB", "price": 25.00, "category": "Data Bundles", "available": True},
            {"id": 3, "name": "MTN Mobile Data 5GB", "price": 40.00, "category": "Data Bundles", "available": True},
            {"id": 4, "name": "MTN Fiber Broadband 10MBPS", "price": 200.00, "category": "Broadband", "available": True},
            {"id": 5, "name": "MTN Fiber Broadband 20MBPS", "price": 350.00, "category": "Broadband", "available": True},
            {"id": 6, "name": "MTN Airtime ₵10", "price": 10.00, "category": "Airtime", "available": True},
            {"id": 7, "name": "MTN Airtime ₵20", "price": 20.00, "category": "Airtime", "available": True},
            {"id": 8, "name": "MTN Router", "price": 300.00, "category": "Devices", "available": True},
            {"id": 9, "name": "MTN 4G MiFi", "price": 250.00, "category": "Devices", "available": True},
        ]
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'current_order' not in st.session_state:
        st.session_state.current_order = None
    if 'delivery_address' not in st.session_state:
        st.session_state.delivery_address = ""
    if 'payment_method' not in st.session_state:
        st.session_state.payment_method = ""
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'show_admin_login' not in st.session_state:
        st.session_state.show_admin_login = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = None

# Call the initialization function
initialize_session_state()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def generate_response(user_input):
    """Generate response using rule-based system"""
    user_input = user_input.lower()
    
    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to MTN Ghana. How can I help you today?"
    elif "menu" in user_input or "products" in user_input:
        return "Our products are organized by categories. Please select a category from the sidebar to view available products."
    elif "price" in user_input or "how much" in user_input:
        for product in st.session_state.products:
            if product['name'].lower() in user_input:
                return f"The {product['name']} costs ₵{product['price']:.2f}"
        return "Please check the product prices in the sidebar."
    elif "order" in user_input or "buy" in user_input:
        return "You can add products to your cart from the sidebar, then proceed to checkout."
    elif "status" in user_input or "track" in user_input:
        if not st.session_state.orders:
            return "You haven't placed any orders yet."
        else:
            return "You can view your order status in the 'My Orders' section."
    elif "delivery" in user_input:
        return "We'll ask for your delivery address when you checkout. Physical products are delivered within 24 hours in Accra and 48 hours elsewhere."
    elif "payment" in user_input:
        return "We accept mobile money (MTN MoMo), credit cards, and cash on delivery."
    elif "cancel" in user_input:
        return "You can cancel orders from the 'My Orders' section if they haven't been processed yet."
    else:
        return "I'm here to help with your MTN product orders. You can ask about products, prices, or your orders."

def place_order():
    """Place the current order"""
    if not st.session_state.cart:
        return None
    
    order_id = len(st.session_state.orders) + 1
    order = {
        "id": order_id,
        "items": st.session_state.cart.copy(),
        "status": "Pending",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delivery_address": st.session_state.delivery_address,
        "payment_method": st.session_state.payment_method,
        "total": sum(item['price'] for item in st.session_state.cart)
    }
    st.session_state.orders.append(order)
    st.session_state.current_order = order
    st.session_state.cart = []
    return order_id

def cancel_order(order_id):
    """Cancel an order"""
    for order in st.session_state.orders:
        if order['id'] == order_id and order['status'] in ["Pending", "Processing"]:
            order['status'] = "Cancelled"
            return True
    return False

def admin_login():
    """Admin login page"""
    st.title("MTN Admin Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.session_state.show_admin_login = False
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def admin_dashboard():
    """Admin dashboard"""
    st.title("MTN Admin Dashboard")
    
    tab1, tab2 = st.tabs(["Orders", "Products"])
    
    with tab1:
        st.header("Order Management")
        
        if not st.session_state.orders:
            st.info("No orders yet")
        else:
            for order in st.session_state.orders:
                with st.expander(f"Order #{order['id']} - {order['status']} - ₵{order['total']:.2f}"):
                    st.write(f"**Time:** {order['timestamp']}")
                    st.write(f"**Delivery Address:** {order['delivery_address']}")
                    st.write(f"**Payment Method:** {order['payment_method']}")
                    st.write("**Items:**")
                    for item in order['items']:
                        st.write(f"- {item['name']} (₵{item['price']:.2f})")
                    
                    status_options = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
                    new_status = st.selectbox(
                        f"Update status for Order #{order['id']}",
                        status_options,
                        index=status_options.index(order['status']),
                        key=f"status_{order['id']}"
                    )
                    
                    if st.button(f"Update Order #{order['id']}", key=f"update_{order['id']}"):
                        order['status'] = new_status
                        st.success(f"Order #{order['id']} updated to {new_status}")
                        st.rerun()
    
    with tab2:
        st.header("Product Management")
        
        st.subheader("Add New Product")
        with st.form("add_product_form"):
            new_name = st.text_input("Product Name")
            new_price = st.number_input("Price (₵)", min_value=0.0, step=0.1, format="%.2f")
            new_category = st.selectbox("Category", ["Data Bundles", "Broadband", "Airtime", "Devices"])
            new_available = st.checkbox("Available", value=True)
            
            if st.form_submit_button("Add Product"):
                new_id = max(p['id'] for p in st.session_state.products) + 1 if st.session_state.products else 1
                st.session_state.products.append({
                    "id": new_id,
                    "name": new_name,
                    "price": new_price,
                    "category": new_category,
                    "available": new_available
                })
                st.success(f"Added {new_name} to products!")
                st.rerun()
        
        st.subheader("Current Products")
        for product in st.session_state.products:
            with st.expander(f"{product['name']} - ₵{product['price']:.2f}"):
                with st.form(f"edit_form_{product['id']}"):
                    edit_name = st.text_input("Name", value=product['name'], key=f"name_{product['id']}")
                    edit_price = st.number_input("Price", value=product['price'], key=f"price_{product['id']}")
                    edit_category = st.selectbox(
                        "Category",
                        ["Data Bundles", "Broadband", "Airtime", "Devices"],
                        index=["Data Bundles", "Broadband", "Airtime", "Devices"].index(product['category']),
                        key=f"category_{product['id']}"
                    )
                    edit_available = st.checkbox("Available", value=product['available'], key=f"available_{product['id']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update"):
                            product['name'] = edit_name
                            product['price'] = edit_price
                            product['category'] = edit_category
                            product['available'] = edit_available
                            st.success("Product updated!")
                            st.rerun()
                    with col2:
                        if st.form_submit_button("Delete"):
                            st.session_state.products = [p for p in st.session_state.products if p['id'] != product['id']]
                            st.success("Product deleted!")
                            st.rerun()
    
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

def checkout():
    """Checkout process"""
    st.title("Checkout")
    
    if not st.session_state.cart:
        st.warning("Your cart is empty")
        return
    
    st.subheader("Order Summary")
    for item in st.session_state.cart:
        st.write(f"- {item['name']} (₵{item['price']:.2f})")
    st.markdown(f"**Total: ₵{sum(item['price'] for item in st.session_state.cart):.2f}**")
    
    st.subheader("Delivery Information")
    st.session_state.delivery_address = st.text_area("Delivery Address", value=st.session_state.delivery_address)
    
    st.subheader("Payment Method")
    st.session_state.payment_method = st.radio(
        "Select Payment Method",
        ["MTN Mobile Money", "Credit Card", "Cash on Delivery"],
        index=0 if not st.session_state.payment_method else 
             ["MTN Mobile Money", "Credit Card", "Cash on Delivery"].index(st.session_state.payment_method)
    )
    
    if st.button("Place Order"):
        order_id = place_order()
        st.success(f"Order #{order_id} placed successfully! Total: ₵{st.session_state.current_order['total']:.2f}")
        st.session_state.current_step = "confirmation"
        st.rerun()

def user_interface():
    """Main user interface"""
    st.title("MTN Ghana Products Ordering")
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("How can we help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Product categories and cart
    st.sidebar.title("MTN Products")
    
    categories = set(p['category'] for p in st.session_state.products)
    for category in categories:
        with st.sidebar.expander(category):
            for product in [p for p in st.session_state.products if p['category'] == category and p['available']]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{product['name']}** - ₵{product['price']:.2f}")
                with col2:
                    if st.button("➕", key=f"add_{product['id']}"):
                        st.session_state.cart.append(product)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Added {product['name']} to your cart. Current total: ₵{sum(i['price'] for i in st.session_state.cart):.2f}"
                        })
                        st.rerun()
    
    # Cart management
    st.sidebar.markdown("---")
    st.sidebar.subheader("Your Cart")
    
    if not st.session_state.cart:
        st.sidebar.write("Cart is empty")
    else:
        for item in st.session_state.cart:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.sidebar.write(f"- {item['name']}")
            with col2:
                if st.sidebar.button("❌", key=f"remove_{item['id']}"):
                    st.session_state.cart = [i for i in st.session_state.cart if i['id'] != item['id']]
                    st.rerun()
        
        st.sidebar.markdown(f"**Total: ₵{sum(item['price'] for item in st.session_state.cart):.2f}**")
        
        if st.sidebar.button("Proceed to Checkout"):
            st.session_state.current_step = "checkout"
            st.rerun()
    
    # Order history
    st.sidebar.markdown("---")
    if st.sidebar.button("My Orders"):
        if not st.session_state.orders:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "You haven't placed any orders yet."
            })
        else:
            orders_summary = "Your Orders:\n\n"
            for order in st.session_state.orders:
                orders_summary += f"**Order #{order['id']}** ({order['status']}) - ₵{order['total']:.2f}\n"
                orders_summary += f"Date: {order['timestamp']}\n"
                orders_summary += f"Payment: {order['payment_method']}\n\n"
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": orders_summary
            })
        st.rerun()
    
    # Admin login
    st.sidebar.markdown("---")
    if st.sidebar.button("Admin Login"):
        st.session_state.show_admin_login = True
        st.rerun()
    
    # Checkout process
    if st.session_state.get('current_step') == "checkout":
        checkout()
    
    # Order confirmation
    elif st.session_state.get('current_step') == "confirmation" and st.session_state.current_order:
        st.title("Order Confirmation")
        st.success(f"Thank you for your order #{st.session_state.current_order['id']}!")
        st.write(f"**Total:** ₵{st.session_state.current_order['total']:.2f}")
        st.write(f"**Payment Method:** {st.session_state.current_order['payment_method']}")
        st.write(f"**Delivery Address:** {st.session_state.current_order['delivery_address']}")
        
        if st.button("Back to Shopping"):
            st.session_state.current_step = None
            st.session_state.current_order = None
            st.rerun()

def main():
    """Main app router"""
    if st.session_state.show_admin_login or st.session_state.admin_logged_in:
        if not st.session_state.admin_logged_in:
            admin_login()
        else:
            admin_dashboard()
    else:
        user_interface()

if __name__ == "__main__":
    main()