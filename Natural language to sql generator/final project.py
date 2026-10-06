import streamlit as st
import ollama
import sqlite3
import re

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Shopping SQL Generator",
    page_icon="🛍️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title-box {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

.title-box h1 {
    color: white;
    font-size: 38px;
    margin-bottom: 5px;
}

.title-box p {
    color: white;
    font-size: 18px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
    margin-bottom: 15px;
}

.section-title {
    color: #6a11cb;
    font-size: 25px;
    font-weight: bold;
}

.success-box {
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

.info-box {
    background-color: #e7f1ff;
    color: #084298;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<div class="title-box">
    <h1>🛍️ Natural Language to SQL Shopping Generator</h1>
    <p>Ask questions in English and get SQL results using AI</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect("shopping.db")
cursor = conn.cursor()

# =====================================================
# CREATE TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS shopping (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price INTEGER,
    quantity INTEGER
)
""")

# =====================================================
# SAMPLE PRODUCTS
# =====================================================

products = [
    (1, "Laptop", "Electronics", 50000, 10),
    (2, "Mobile Phone", "Electronics", 20000, 15),
    (3, "Headphones", "Electronics", 2000, 25),
    (4, "T-Shirt", "Clothing", 800, 30),
    (5, "Shoes", "Footwear", 1500, 20)
]

for product in products:
    cursor.execute("""
    INSERT OR IGNORE INTO shopping
    (id, product_name, category, price, quantity)
    VALUES (?, ?, ?, ?, ?)
    """, product)

conn.commit()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("🛍️ Shopping Menu")

    st.markdown("""
    **Available Categories**
    
    💻 Electronics  
    👕 Clothing  
    👟 Footwear
    """)

    st.divider()

    st.subheader("💡 Example Questions")

    example = st.selectbox(
        "Choose a question",
        [
            "Show all products",
            "Show products below 5000",
            "Show electronics products",
            "Show the most expensive product",
            "Show the cheapest product",
            "Show products with quantity greater than 20",
            "Show product names and prices"
        ]
    )

# =====================================================
# DATABASE STATISTICS
# =====================================================

cursor.execute("SELECT COUNT(*) FROM shopping")
total_products = cursor.fetchone()[0]

cursor.execute("SELECT SUM(quantity) FROM shopping")
total_quantity = cursor.fetchone()[0]

cursor.execute("SELECT MAX(price) FROM shopping")
highest_price = cursor.fetchone()[0]

# =====================================================
# DASHBOARD
# =====================================================

st.markdown(
    '<div class="section-title">📊 Shopping Dashboard</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🛍️ Total Products",
        total_products
    )

with col2:
    st.metric(
        "📦 Total Quantity",
        total_quantity
    )

with col3:
    st.metric(
        "💰 Highest Price",
        f"₹{highest_price:,}"
    )

st.write("")

# =====================================================
# QUESTION INPUT
# =====================================================

st.markdown(
    '<div class="section-title">🔎 Ask Your Shopping Question</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Enter your question:",
    value=example,
    placeholder="Example: Show products below 5000"
)

# =====================================================
# BUTTONS
# =====================================================

col1, col2 = st.columns([1, 1])

with col1:
    generate = st.button(
        "🚀 Generate SQL",
        use_container_width=True
    )

with col2:
    clear = st.button(
        "🧹 Clear",
        use_container_width=True
    )

if clear:
    st.rerun()

# =====================================================
# GENERATE SQL
# =====================================================

if generate:

    if not question.strip():

        st.warning("⚠️ Please enter a question.")

    else:

        try:

            # =================================================
            # OLLAMA
            # =================================================

            with st.spinner("🤖 AI is generating SQL..."):

                response = ollama.chat(
                    model="llama3.2:3b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are an SQL generator.

Database table:
shopping

Columns:
id, product_name, category, price, quantity

Convert the user's question into SQLite SQL.

Rules:
1. Return ONLY one SELECT query.
2. Do not give explanations.
3. Do not use markdown.
4. Do not use ```sql.
5. Do not write any text before or after the SQL.
6. Use only the shopping table.
"""
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

            # =================================================
            # GET SQL
            # =================================================

            sql_query = response["message"]["content"].strip()

            # Remove markdown
            sql_query = re.sub(
                r"```sql\s*",
                "",
                sql_query,
                flags=re.IGNORECASE
            )

            sql_query = re.sub(
                r"```",
                "",
                sql_query
            )

            sql_query = sql_query.strip()

            # =================================================
            # EXTRACT SELECT QUERY
            # =================================================

            match = re.search(
                r"SELECT\s+.*?(?:;|$)",
                sql_query,
                flags=re.IGNORECASE | re.DOTALL
            )

            if not match:

                st.error(
                    "❌ Ollama did not generate a valid SQL query."
                )

            else:

                sql_query = match.group(0).strip()

                # =================================================
                # SECURITY CHECK
                # =================================================

                if not sql_query.upper().startswith("SELECT"):

                    st.error(
                        "❌ Only SELECT queries are allowed."
                    )

                else:

                    # =================================================
                    # GENERATED SQL
                    # =================================================

                    st.markdown(
                        '<div class="section-title">💻 Generated SQL</div>',
                        unsafe_allow_html=True
                    )

                    st.code(
                        sql_query,
                        language="sql"
                    )

                    # =================================================
                    # EXECUTE SQL
                    # =================================================

                    cursor.execute(sql_query)

                    result = cursor.fetchall()

                    # =================================================
                    # RESULT
                    # =================================================

                    st.markdown(
                        '<div class="section-title">🛒 Shopping Result</div>',
                        unsafe_allow_html=True
                    )

                    if result:

                        st.success(
                            f"✅ {len(result)} record(s) found!"
                        )

                        st.dataframe(
                            result,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "ℹ️ No products found."
                        )

        except ollama.ResponseError as e:

            st.error(
                f"🤖 Ollama Error: {e}"
            )

        except sqlite3.Error as e:

            st.error(
                f"🗄️ SQLite Error: {e}"
            )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )