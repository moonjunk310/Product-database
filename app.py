import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="9 Star Foods Database",
    layout="wide"
)

# ------------------------
# Load Data
# ------------------------

products_df = pd.read_excel(
    "Products Price table Web.xlsx"
)

ingredients_df = pd.read_excel(
    "Ingredients Price table Web.xlsx"
)

# ------------------------
# Sidebar Menu
# ------------------------

page = st.sidebar.radio(
    "Database",
    ["Products", "Ingredients"]
)

# ==================================================
# PRODUCTS DATABASE
# ==================================================

if page == "Products":

    st.title("9 Star Foods Product Database")

    selected_category = st.selectbox(
        "Select Category",
        sorted(
            products_df["Category"]
            .dropna()
            .unique()
        )
    )

    category_df = products_df[
        products_df["Category"] == selected_category
    ]

    selected_product = st.selectbox(
        "Select Product",
        sorted(
            category_df["Items"]
            .dropna()
            .unique()
        )
    )

    product_df = category_df[
        category_df["Items"] == selected_product
    ]

    selected_customer = st.selectbox(
        "Select Customer",
        sorted(
            product_df["Remarks"]
            .fillna("N/A")
            .unique()
        )
    )

    result = product_df[
        product_df["Remarks"] == selected_customer
    ]

    if not result.empty:

        row = result.iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "SKU",
                row["SKU"]
            )

            st.metric(
                "Manufacturing Cost",
                f"${row['manufacturing cost']}"
                if pd.notna(row["manufacturing cost"])
                else "N/A"
            )

            st.metric(
                "Price/LB",
                f"${row['price/lb']}"
                if pd.notna(row["price/lb"])
                else "N/A"
            )

        with col2:
            st.metric(
                "Price/Bag",
                f"${row['price/bag']}"
                if pd.notna(row["price/bag"])
                else "N/A"
            )

            st.metric(
                "Box Price",
                f"${row['box price']}"
                if pd.notna(row["box price"])
                else "N/A"
            )

            st.metric(
                "Pallet Price",
                f"${row['pallet price']}"
                if pd.notna(row["pallet price"])
                else "N/A"
            )

        with col3:
            st.metric(
                "Margin %",
                f"{round(row['margin ratio(%)']*100,1)}%"
                if pd.notna(row["margin ratio(%)"])
                else "N/A"
            )

            st.metric(
                "PCS/CS",
                row["pcs/cs"]
                if pd.notna(row["pcs/cs"])
                else "N/A"
            )

            st.metric(
                "CS/Pallet",
                row["cs/pallet"]
                if pd.notna(row["cs/pallet"])
                else "N/A"
            )

        st.divider()

        st.subheader("Product Details")

        st.dataframe(
            result,
            use_container_width=True
        )

# ==================================================
# INGREDIENTS DATABASE
# ==================================================

if page == "Ingredients":

    st.title("9 Star Foods Ingredients Database")

    selected_ingredient = st.selectbox(
        "Select Ingredient",
        sorted(
            ingredients_df["Ingredients"]
            .dropna()
            .unique()
        )
    )

    result = ingredients_df[
        ingredients_df["Ingredients"]
        == selected_ingredient
    ]

    if not result.empty:

        display_df = result[
            [
                "Code",
                "Brand",
                "Vendor",
                "$/lb"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True
        )

        price_series = pd.to_numeric(
            result["$/lb"],
            errors="coerce"
        )

        if price_series.notna().any():

            lowest_row = result.loc[
                price_series.idxmin()
            ]

            st.success(
                f"Lowest Price: "
                f"{lowest_row['Vendor']} "
                f"(${float(lowest_row['$/lb']):.2f}/lb)"
            )