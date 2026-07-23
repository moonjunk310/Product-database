
import streamlit as st
import pandas as pd

# Excel 파일 읽기
df = pd.read_excel("Products Price table Web.xlsx")

st.title("9 Star Foods Product Database")

# ------------------------
# 표시 함수
# ------------------------

def money(v):
    if pd.isna(v):
        return "N/A"

    try:
        return f"${float(v):,.2f}"
    except:
        return "N/A"


def money_lb(v):
    if pd.isna(v):
        return "N/A"

    try:
        return f"${float(v):,.3f}"
    except:
        return "N/A"


def number(v):
    if pd.isna(v):
        return "N/A"

    try:
        return f"{float(v):.3f}".rstrip("0").rstrip(".")
    except:
        return str(v)


def margin(price, cost):

    if pd.isna(price) or pd.isna(cost):
        return "N/A"

    try:
        value = ((float(price) / float(cost)) - 1) * 100
        return f"{value:.0f}%"
    except:
        return "N/A"


# ------------------------
# Category 선택
# ------------------------

selected_category = st.selectbox(
    "Select Category",
    sorted(df["Category"].dropna().unique())
)

category_df = df[
    df["Category"] == selected_category
]

# ------------------------
# Product 선택
# ------------------------

selected_product = st.selectbox(
    "Select Product",
    sorted(category_df["Items"].dropna().unique())
)

product_df = category_df[
    category_df["Items"] == selected_product
]

# ------------------------
# Customer 선택
# ------------------------

selected_customer = st.selectbox(
    "Select Customer",
    sorted(product_df["Remarks"].fillna("N/A").unique())
)

result = product_df[
    product_df["Remarks"] == selected_customer
]

# ------------------------
# 결과 표시
# ------------------------

if not result.empty:

    row = result.iloc[0]

    st.markdown("---")

    st.title(row["Items"])

    st.write(f"**Customer:** {row['Remarks']}")
    st.write(f"**SKU:** {row['SKU']}")
    st.write(f"**USDA Category:** {row['USDA Category']}")

    st.markdown("---")

    st.subheader("💰 Pricing")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Manufacturing Cost",
            money(row["manufacturing cost"])
        )

        st.metric(
            "Price / lb",
            money_lb(row["price/lb"])
        )

        st.metric(
            "Margin",
            margin(
                row["price/lb"],
                row["manufacturing cost"]
            )
        )

    with col2:
        st.metric(
            "Price / bag",
            money(row["price/bag"])
        )

        st.metric(
            "Box Price",
            money(row["box price"])
        )

        st.metric(
            "Pallet Price",
            money(row["pallet price"])
        )

    st.markdown("---")

    st.subheader("📦 Packaging")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "lb / bag",
            number(row["lb/bag"])
        )

        st.metric(
            "lb / cs",
            number(row["lb/cs"])
        )

    with col2:
        st.metric(
            "pcs / cs",
            number(row["pcs/cs"])
        )

        st.metric(
            "cs / pallet",
            number(row["cs/pallet"])
        )

    st.markdown("---")

    st.subheader("🚚 Shipping")

    st.metric(
        "lb / pallet",
        number(row["lb/pallet"])
    )
