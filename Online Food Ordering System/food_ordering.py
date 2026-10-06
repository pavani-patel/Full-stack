import streamlit as st
import ollama

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="Foodie AI",
    page_icon="🍔",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff1eb, #e8f8ff, #f5eaff);
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #ff4b4b;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #555555;
    margin-bottom: 30px;
}

/* Food cards */
.food-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.12);
    text-align: center;
    border: 2px solid #eeeeee;
}

.food-name {
    font-size: 22px;
    font-weight: bold;
    color: #ff4b4b;
}

.food-price {
    font-size: 20px;
    font-weight: bold;
    color: #16a085;
}

/* Section headings */
.section-title {
    background: linear-gradient(90deg, #ff4b4b, #ff8c42);
    color: white;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
}

/* AI box */
.ai-box {
    background: linear-gradient(135deg, #e8d9ff, #d8f3ff);
    padding: 20px;
    border-radius: 18px;
    border: 2px solid #9b59b6;
    margin-top: 10px;
}

/* Cart */
.cart-box {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.12);
}

/* Total */
.total-box {
    background: linear-gradient(90deg, #00b09b, #96c93d);
    color: white;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}

/* Footer */
.footer {
    text-align: center;
    color: #666666;
    padding: 25px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# TITLE
# --------------------------------
st.markdown(
    '<div class="main-title">🍔 Foodie AI 🍕</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Delicious Food • Smart Recommendations • Easy Ordering 🤖</div>',
    unsafe_allow_html=True
)


# --------------------------------
# FOOD MENU
# --------------------------------
food_menu = {
    "Pizza": 250,
    "Burger": 150,
    "Biryani": 220,
    "Fried Rice": 180,
    "Noodles": 160,
    "Dosa": 80,
    "Idli": 60,
    "Paneer Curry": 200,
    "Chicken Curry": 250,
    "Ice Cream": 100
}

# Food emojis
food_icons = {
    "Pizza": "🍕",
    "Burger": "🍔",
    "Biryani": "🍛",
    "Fried Rice": "🍚",
    "Noodles": "🍜",
    "Dosa": "🥞",
    "Idli": "⚪",
    "Paneer Curry": "🥘",
    "Chicken Curry": "🍗",
    "Ice Cream": "🍦"
}


# --------------------------------
# SESSION STATE
# --------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []


# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.markdown("## 🍽️ Food Menu")

selected_food = st.sidebar.selectbox(
    "Choose Food",
    list(food_menu.keys())
)

quantity = st.sidebar.number_input(
    "Quantity",
    min_value=1,
    max_value=10,
    value=1
)

if st.sidebar.button("🛒 Add to Cart", use_container_width=True):

    st.session_state.cart.append({
        "food": selected_food,
        "quantity": quantity,
        "price": food_menu[selected_food]
    })

    st.sidebar.success(
        f"✅ {quantity} × {selected_food} added!"
    )


# --------------------------------
# AVAILABLE FOOD
# --------------------------------
st.markdown(
    '<div class="section-title">🍽️ Available Food</div>',
    unsafe_allow_html=True
)

cols = st.columns(3)

for index, (food, price) in enumerate(food_menu.items()):

    with cols[index % 3]:

        st.markdown(
            f"""
            <div class="food-card">
                <div style="font-size:50px;">
                    {food_icons[food]}
                </div>
                <div class="food-name">
                    {food}
                </div>
                <div class="food-price">
                    ₹{price}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"➕ Add {food}",
            key=f"add_{food}",
            use_container_width=True
        ):

            st.session_state.cart.append({
                "food": food,
                "quantity": 1,
                "price": price
            })

            st.success(f"✅ {food} added!")


# --------------------------------
# AI FOOD ASSISTANT
# --------------------------------
st.markdown(
    '<div class="section-title">🤖 AI Food Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="ai-box">
    💡 <b>Ask our AI assistant!</b><br>
    Example: "Suggest a spicy food" or
    "What is the cheapest food?"
    </div>
    """,
    unsafe_allow_html=True
)

user_question = st.text_input(
    "💬 Ask your food question"
)

if st.button("🤖 Ask AI", use_container_width=True):

    if user_question:

        prompt = f"""
        You are a friendly food ordering assistant.

        Available foods:
        {list(food_menu.keys())}

        Food prices:
        {food_menu}

        Customer question:
        {user_question}

        Give a simple, friendly and useful answer.
        """

        try:

            with st.spinner("🤖 AI is thinking..."):

                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            st.success("🤖 AI Recommendation")

            st.write(
                response["message"]["content"]
            )

        except Exception as e:

            st.error(
                "❌ Ollama is not running or the model is unavailable."
            )

            st.info(
                "Run: ollama serve"
            )

    else:

        st.warning(
            "Please enter a question."
        )


# --------------------------------
# SHOPPING CART
# --------------------------------
st.markdown(
    '<div class="section-title">🛒 Your Shopping Cart</div>',
    unsafe_allow_html=True
)

if not st.session_state.cart:

    st.info(
        "🛒 Your cart is empty. Add some delicious food!"
    )

else:

    total = 0

    for item in st.session_state.cart:

        item_total = (
            item["price"] *
            item["quantity"]
        )

        total += item_total

        st.markdown(
            f"""
            <div class="cart-box">
            <b>{food_icons[item["food"]]} {item["food"]}</b>
            <br>
            Quantity: {item["quantity"]}
            <br>
            Price: ₹{item["price"]}
            <br>
            <b>Item Total: ₹{item_total}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")


    st.markdown(
        f"""
        <div class="total-box">
        💰 Total Amount: ₹{total}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------
    # CUSTOMER DETAILS
    # --------------------------------
    st.markdown(
        '<div class="section-title">👤 Customer Details</div>',
        unsafe_allow_html=True
    )

    name = st.text_input(
        "👤 Customer Name"
    )

    phone = st.text_input(
        "📱 Phone Number"
    )

    address = st.text_area(
        "🏠 Delivery Address"
    )


    # --------------------------------
    # PLACE ORDER
    # --------------------------------
    if st.button(
        "🍽️ Place Order",
        use_container_width=True
    ):

        if name and phone and address:

            st.balloons()

            st.success(
                "🎉 Order placed successfully!"
            )

            st.markdown(
                f"""
                ### 📦 Order Confirmation

                👤 **Customer:** {name}

                📱 **Phone:** {phone}

                🏠 **Address:** {address}

                💰 **Total Amount:** ₹{total}

                🍔 **Thank you for ordering!**
                """
            )

            st.session_state.cart = []

        else:

            st.warning(
                "⚠️ Please fill all customer details."
            )


# --------------------------------
# CLEAR CART
# --------------------------------
if st.button(
    "🗑️ Clear Cart",
    use_container_width=True
):

    st.session_state.cart = []

    st.success(
        "🛒 Cart cleared successfully!"
    )


# --------------------------------
# FOOTER
# --------------------------------
st.markdown(
    """
    <div class="footer">
    🍔 Foodie AI | Powered by Streamlit + Ollama 🤖
    <br>
    Fresh Food • Smart AI • Happy Customers ❤️
    </div>
    """,
    unsafe_allow_html=True
)
