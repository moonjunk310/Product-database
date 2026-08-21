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
products_df.columns = products_df.columns.astype(str).str.strip()
21
ingredients_df.columns = ingredients_df.columns.astype(str).str.strip()
22
 
23
# --------------------------------------------------
24
# MENU
25
# --------------------------------------------------
26
 
27
page = st.sidebar.radio(
28
"Database",
29
["Products", "Ingredients"]
30
)
31
 
32
# ==================================================
33
# FUNCTIONS
34
# ==================================================
35
 
36
def money(v):
37
if pd.isna(v):
38
return "N/A"
39
 
40
try:
41
return f"${float(v):,.2f}"
42
except:
43
return "N/A"
44
 
45
 
46
def money_lb(v):
47
if pd.isna(v):
48
return "N/A"
49
 
50
try:
51
return f"${float(v):,.3f}"
52
except:
53
return "N/A"
54
 
55
 
56
def number(v):
57
if pd.isna(v):
58
return "N/A"
59
 
60
try:
61
return f"{float(v):.3f}".rstrip("0").rstrip(".")
62
except:
63
return str(v)
64
 
65
 
66
def margin(price, cost):
67
 
68
if pd.isna(price) or pd.isna(cost):
69
return "N/A"
70
 
71
try:
72
 
73
price = float(price)
74
cost = float(cost)
75
 
76
if price <= 0 or cost <= 0:
77
return "N/A"
78
 
79
value = ((price / cost) - 1) * 100
80
 
81
return f"{value:.0f}%"
82
 
83
except:
84
return "N/A"
85
 
86
 
87
# ==================================================
88
# PRODUCTS
89
# ==================================================
90
 
91
if page == "Products":
92
 
93
df = products_df
94
 
95
st.title("9 Star Foods Product Database")
96
 
97
selected_category = st.selectbox(
98
"Select Category",
99
sorted(df["Category"].dropna().unique())
100
)
101
 
102
category_df = df[
103
df["Category"] == selected_category
104
]
105
 
106
selected_product = st.selectbox(
107
"Select Product",
108
sorted(category_df["Items"].dropna().unique())
109
)
110
 
111
product_df = category_df[
112
category_df["Items"] == selected_product
113
]
114
 
115
selected_customer = st.selectbox(
116
"Select Customer",
117
sorted(product_df["Remarks"].fillna("N/A").unique())
118
)
119
 
120
result = product_df[
121
product_df["Remarks"] == selected_customer
122
]
123
 
124
if not result.empty:
125
 
126
row = result.iloc[0]
127
 
128
st.markdown("---")
129
 
130
st.title(row["Items"])
131
 
132
st.write(f"**Customer:** {row['Remarks']}")
133
st.write(f"**SKU:** {row['SKU']}")
134
st.write(f"**USDA Category:** {row['USDA Category']}")
135
 
136
st.markdown("---")
137
 
138
st.subheader("💰 Pricing")
139
 
140
col1, col2 = st.columns(2)
141
 
142
with col1:
143
 
144
st.metric(
145
"Manufacturing Cost",
146
money(row["manufacturing cost"])
147
)
148
 
149
st.metric(
150
"Price / lb",
151
money_lb(row["price/lb"])
152
)
153
 
154
st.metric(
155
"Margin",
156
margin(
157
row["price/lb"],
158
row["manufacturing cost"]
159
)
160
)
161
 
162
with col2:
163
 
164
st.metric(
165
"Price / bag",
166
money(row["price/bag"])
167
)
168
 
169
st.metric(
170
"Box Price",
171
money(row["box price"])
172
)
173
 
174
st.metric(
175
"Pallet Price",
176
money(row["pallet price"])
177
)
178
 
179
st.markdown("---")
180
 
181
st.subheader("📦 Packaging")
182
 
183
col1, col2 = st.columns(2)
184
 
185
with col1:
186
 
187
st.metric(
188
"lb / bag",
189
number(row["lb/bag"])
190
)
191
 
192
st.metric(
193
"lb / cs",
194
number(row["lb/cs"])
195
)
196
 
197
with col2:
198
 
199
st.metric(
200
"pcs / cs",
201
number(row["pcs/cs"])
202
)
203
 
204
st.metric(
205
"cs / pallet",
206
number(row["cs/pallet"])
207
)
208
 
209
st.markdown("---")
210
 
211
st.subheader("🚚 Shipping")
212
 
213
st.metric(
214
"lb / pallet",
215
number(row["lb/pallet"])
216
)
217
 
218
# ==================================================
219
# INGREDIENTS
220
# ==================================================
221
 
222
if page == "Ingredients":
223
 
224
st.title("9 Star Foods Ingredients Database")
225
 
226
ingredient_column = None
227
 
228
for col in ingredients_df.columns:
229
if str(col).strip().lower() == "ingredients":
230
ingredient_column = col
231
 
232
if ingredient_column is None:
233
 
234
st.error(
235
"Ingredients column not found."
236
)
237
 
238
st.write(
239
ingredients_df.columns.tolist()
240
)
241
 
242
else:
243
 
244
ingredient_list = sorted(
245
ingredients_df[ingredient_column]
246
.dropna()
247
.astype(str)
248
.unique()
249
)
250
 
251
selected_ingredient = st.selectbox(
252
"Select Ingredient",
253
ingredient_list
254
)
255
 
256
result = ingredients_df[
257
ingredients_df[ingredient_column]
258
.astype(str)
259
== selected_ingredient
260
]
261
 
262
show_cols = []
263
 
264
for c in [
265
"Code",
266
"Brand",
267
"Vendor",
268
"$/lb"
269
]:
270
if c in result.columns:
271
show_cols.append(c)
272
 
273
st.dataframe(
274
result[show_cols],
275
use_container_width=True
276
)
277
 
278
if "$/lb" in result.columns:
279
 
280
prices = pd.to_numeric(
281
result["$/lb"],
282
errors="coerce"
283
)
284
 
285
valid_rows = result.loc[
286
prices.notna()
287
]
288
 
289
if not valid_rows.empty:
290
 
291
lowest_row = valid_rows.loc[
292
pd.to_numeric(
293
valid_rows["$/lb"]
294
).idxmin()
295
]
296
 
297
st.success(
298
f"Lowest Price: "
299
f"{lowest_row['Vendor']} "
300
f"(${float(lowest_row['$/lb']):.2f}/lb)"
301
)