import streamlit as st
2
import pandas as pd
3
 
4
# --------------------------------------------------
5
# PAGE
6
# --------------------------------------------------
7
 
8
st.set_page_config(
9
page_title="9 Star Foods Database",
10
layout="wide"
11
)
12
 
13
# --------------------------------------------------
14
# LOAD FILES
15
# --------------------------------------------------
16
 
17
products_df = pd.read_excel("Products Price table Web.xlsx")
18
ingredients_df = pd.read_excel("Ingredients Price table Web.xlsx")
19
 
20
# 컬럼 공백 제거
21
products_df.columns = products_df.columns.astype(str).str.strip()
22
ingredients_df.columns = ingredients_df.columns.astype(str).str.strip()
23
 
24
# --------------------------------------------------
25
# MENU
26
# --------------------------------------------------
27
 
28
page = st.sidebar.radio(
29
"Database",
30
["Products", "Ingredients"]
31
)
32
 
33
# ==================================================
34
# PRODUCTS
35
# ==================================================
36
 
37
if page == "Products":
38
 
39
st.title("9 Star Foods Product Database")
40
 
41
selected_category = st.selectbox(
42
"Select Category",
43
sorted(products_df["Category"].dropna().unique())
44
)
45
 
46
category_df = products_df[
47
products_df["Category"] == selected_category
48
]
49
 
50
selected_product = st.selectbox(
51
"Select Product",
52
sorted(category_df["Items"].dropna().unique())
53
)
54
 
55
product_df = category_df[
56
category_df["Items"] == selected_product
57
]
58
 
59
selected_customer = st.selectbox(
60
"Select Customer",
61
sorted(product_df["Remarks"].fillna("N/A").unique())
62
)
63
 
64
result = product_df[
65
product_df["Remarks"].fillna("N/A")
66
== selected_customer
67
]
68
 
69
if not result.empty:
70
 
71
row = result.iloc[0]
72
 
73
st.subheader(selected_product)
74
 
75
col1, col2 = st.columns(2)
76
 
77
with col1:
78
 
79
st.write("**SKU**")
80
st.write(row.get("SKU", "N/A"))
81
 
82
st.write("**Manufacturing Cost**")
83
st.write(row.get("manufacturing cost", "N/A"))
84
 
85
st.write("**Price/LB**")
86
st.write(row.get("price/lb", "N/A"))
87
 
88
st.write("**Margin Ratio (%)**")
89
st.write(row.get("margin ratio(%)", "N/A"))
90
 
91
with col2:
92
 
93
st.write("**Price/Bag**")
94
st.write(row.get("price/bag", "N/A"))
95
 
96
st.write("**Box Price**")
97
st.write(row.get("box price", "N/A"))
98
 
99
st.write("**Pallet Price**")
100
st.write(row.get("pallet price", "N/A"))
101
 
102
st.write("**PCS/CS**")
103
st.write(row.get("pcs/cs", "N/A"))
104
 
105
st.divider()
106
 
107
st.dataframe(
108
result,
109
use_container_width=True
110
)
111
 
112
# ==================================================
113
# INGREDIENTS
114
# ==================================================
115
 
116
if page == "Ingredients":
117
 
118
st.title("9 Star Foods Ingredients Database")
119
 
120
# 디버그용 컬럼확인
121
# st.write(ingredients_df.columns.tolist())
122
 
123
ingredient_column = None
124
 
125
for col in ingredients_df.columns:
126
if str(col).strip().lower() == "ingredients":
127
ingredient_column = col
128
break
129
 
130
if ingredient_column is None:
131
 
132
st.error(
133
f"'Ingredients' 컬럼을 찾을 수 없습니다.\n\n"
134
f"현재 컬럼명:\n{ingredients_df.columns.tolist()}"
135
)
136
 
137
else:
138
 
139
ingredient_list = sorted(
140
ingredients_df[ingredient_column]
141
.dropna()
142
.astype(str)
143
.unique()
144
)
145
 
146
selected_ingredient = st.selectbox(
147
"Select Ingredient",
148
ingredient_list
149
)
150
 
151
result = ingredients_df[
152
ingredients_df[ingredient_column]
153
.astype(str)
154
== selected_ingredient
155
]
156
 
157
if not result.empty:
158
 
159
display_cols = []
160
 
161
for c in [
162
"Code",
163
"Brand",
164
"Vendor",
165
"$/lb"
166
]:
167
if c in result.columns:
168
display_cols.append(c)
169
 
170
st.dataframe(
171
result[display_cols],
172
use_container_width=True
173
)
174
 
175
if "$/lb" in result.columns:
176
 
177
prices = pd.to_numeric(
178
result["$/lb"],
179
errors="coerce"
180
)
181
 
182
valid = result.loc[
183
prices.notna()
184
]
185
 
186
if not valid.empty:
187
 
188
lowest_row = valid.loc[
189
pd.to_numeric(
190
valid["$/lb"]
191
).idxmin()
192
]
193
 
194
st.success(
195
f"Lowest Price : "
196
f"{lowest_row['Vendor']} "
197
f"(${float(lowest_row['$/lb']):.2f}/lb)"
198
)