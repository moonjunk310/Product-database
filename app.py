import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="9 Star Foods Database",
    layout="wide"
)

# =========================
# LOAD FILES
# =========================

products_df = pd.read_excel("Products Price table Web.xlsx")
ingredients_df = pd.read_excel("Ingredients Price table Web.xlsx")

products_df.columns = products_df.columns.astype(str).str.strip()
ingredients_df.columns = ingredients_df.columns.astype(str).str.strip()

# =========================
# MENU
# =========================

page = st.sidebar.radio(
    "Database",
    ["Products", "Ingredients"]
)

# =========================
# PRODUCTS
# =========================

if page == "Products":

    st.title("9 Star Foods Product Database")

    category_list = sorted(
        products_df["Category"].dropna().unique()
    )

    selected_category = st.selectbox(
        "Select Category",
        category_list
    )

    category_df = products_df[
        products_df["Category"] == selected_category
    ]

    product_list = sorted(
        category_df["Items"].dropna().unique()
    )

    selected_product = st.selectbox(
        "Select Product",
        product_list
    )

    product_df = category_df[
        category_df["Items"] == selected_product
    ]

    customer_list = sorted(
        product_df["Remarks"]
        .fillna("N/A")
        .unique()
    )

    selected_customer = st.selectbox(
        "Select Customer",
        customer_list
    )

    result = product_df[
        product_df["Remarks"]
        .fillna("N/A")
        == selected_customer
    ]

    if not result.empty:
        st.dataframe(
            result,
            use_container_width=True
        )

# =========================
# INGREDIENTS
# =========================

if page == "Ingredients":

    st.title("9 Star Foods Ingredients Database")

    ingredient_column = None

    for col in ingredients_df.columns:
        if "ingredient" in col.lower():
            ingredient_column = col
            break

    if ingredient_column is None:

        st.error("Ingredients 컬럼을 찾을 수 없습니다.")
        st.write(ingredients_df.columns.tolist())

    else:

        ingredient_list = sorted(
            ingredients_df[ingredient_column]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_ingredient = st.selectbox(
            "Select Ingredient",
            ingredient_list
        )

        result = ingredients_df[
            ingredients_df[ingredient_column]
            .astype(str)
            == selected_ingredient
        ]

        display_columns = []

        for col in ["Code", "Brand", "Vendor", "$/lb"]:
            if col in result.columns:
                display_columns.append(col)

        st.dataframe(
            result[display_columns],
            use_container_width=True
        )

        if "$/lb" in result.columns:

            price_series = pd.to_numeric(
                result["$/lb"],
                errors="coerce"
            )

            if price_series.notna().any():

                lowest_idx = price_series.idxmin()

                lowest_row = result.loc[lowest_idx]

                st.success(
                    f"Lowest Price: "
                    f"{lowest_row['Vendor']} "
                    f"(${float(lowest_row['$/lb']):.2f}/lb)"
                )