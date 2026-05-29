import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv('data.csv', encoding="latin-1")
print('-------basic information----------')
print("rows, columns:", df.shape)
print(df.head())
print('\n')
df.info()
print('\n')
print(df.describe())
print('\n')
print(df.isnull().sum())
print('\n')

print('-------Data Cleaning----------')
# Use non-null data to create corresponding relationship
code_to_name = df.dropna(subset=["Description"]).set_index("StockCode")["Description"].to_dict()

# Step 2: Fill empty Description by matching StockCode
df["Description"] = df.apply(
    lambda row: code_to_name.get(row["StockCode"], row["Description"]),
    axis=1
)

# Remove rows that still have empty Description (cannot be filled)
df = df.dropna(subset=["Description"])

print('\n-------Check for missing values after filling----------')
print(df.isnull().sum())

# Step 3: Filter out invalid data (negative quantity / unit price)
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Step 4: Convert string date to datetime type
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Step 5: Calculate total price per item
df['total_price'] = df['Quantity'] * df['UnitPrice']

# Step 6: Create customer dataset (only keep rows with valid CustomerID)
df_customer = df.dropna(subset=["CustomerID"])

# ===================== Overall Key Metrics =====================
print('\n-------Final cleaned data info----------')
print("Main dataset shape (rows, columns):", df.shape)
print(df.isnull().sum())
print("\nCustomer dataset shape (rows, columns):", df_customer.shape)
print(df_customer.isnull().sum())


print("="*50)
print("                Overall Business Metrics")
print("="*50)

# Overall indicators of the entire site (including anonymous orders)
total_sales = df['total_price'].sum()
total_quantity = df['Quantity'].sum()
total_orders = df['InvoiceNo'].nunique()
avg_sales_per_order = total_sales / total_orders
# Customer-related indicators (for real-name customers only)
total_customers = df_customer['CustomerID'].nunique()
avg_order_value = df_customer.groupby('InvoiceNo')['total_price'].sum().mean()

print(f"Total Sales Amount: {total_sales:.2f}")
print(f"Total Goods Quantity: {total_quantity:,}")
print(f"Total Unique Orders: {total_orders:,}")
print(f"Average sales per order: {avg_sales_per_order:.2f}")
print(f"Total Unique Customers: {total_customers:,}")
print(f"Average Order Value: {avg_order_value:.2f}")

# ===================== Overall Key Metrics =====================
print("="*50)
print("                Overall Business Metrics")
print("="*50)

df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['total_price'].sum()
monthly_orders = df.groupby('YearMonth')['InvoiceNo'].nunique()

print("Monthly Sales Amount:")
print(monthly_sales)
print("\nMonthly Order Count:")
print(monthly_orders)


# ===================== Top 10 Products by Sales =====================
print("\n" + "="*50)
print("                Top 10 Best-selling Products")
print("="*50)

product_top10 = df.groupby(['StockCode', 'Description'])['total_price'].sum().sort_values(ascending=False).head(10)
print(product_top10)

# ===================== Sales by Country =====================
print("\n" + "="*50)
print("                Sales by Country")
print("="*50)

sales_by_area = df.groupby('Country')['total_price'].sum().sort_values(ascending=False)
print(sales_by_area)

# ===================== Customer Consumption Analysis =====================
print("\n" + "="*50)
print("                Customer Behavior Analysis")
print("="*50)

customer_spend = df_customer.groupby('CustomerID')['total_price'].sum()
customer_order_count = df_customer.groupby('CustomerID')['InvoiceNo'].nunique()
top_cust_id_spend = customer_spend.idxmax()
bottom_cust_id_spend = customer_spend.idxmin()
top_cust_id_order = customer_order_count.idxmax()

print(f"Customer with highest consumption: ID = {top_cust_id_spend:.0f}")
print(f"Max consumption per customer: {customer_spend.max():.2f}")
print(f"Customer with lowest consumption: ID = {bottom_cust_id_spend:.0f}")
print(f"Min consumption per customer: {customer_spend.min():.2f}")
print(f"Average consumption per customer: {customer_spend.mean():.2f}")

print(f"\nCustomer with most orders: ID = {top_cust_id_order:.0f}")
print(f"Max order count per customer: {customer_order_count.max()}")
print(f"Min order count per customer: {customer_order_count.min()}")
print(f"Average order count per customer: {customer_order_count.mean():.2f}")

# ===================== Data Visualization =====================
print("\n" + "="*50)
print("                Data Visualization")
print("="*50)
# Global plot settings
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.unicode_minus'] = False

# ---------------- 1. Monthly Sales Line Chart ----------------
plt.figure()
ax1 = monthly_sales.plot(kind='line', marker='o', color='#1f77b4')

plt.title('Monthly Total Sales Trend', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Sales Amount (£)')

ax1.ticklabel_format(style='plain', axis='y')
formatter = ticker.StrMethodFormatter('£{x:,.0f}')
ax1.yaxis.set_major_formatter(formatter)

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print('picture 1 succeed!')

# ---------------- 2. Top 10 Countries Bar Chart ----------------
plt.figure()
ax2 = sales_by_area.head(10).plot(kind='bar', color='#2ca02c')

plt.title('Top 10 Countries by Sales', fontsize=14)
plt.xlabel('Country')
plt.ylabel('Sales Amount (£)')

ax2.ticklabel_format(style='plain', axis='y')
ax2.yaxis.set_major_formatter(formatter)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print('picture 2 succeed!')

# Calculate total consumption for each customer
customer_spend = df_customer.groupby('CustomerID')['total_price'].sum()

# Calculate tertiles to set classification thresholds
q1 = customer_spend.quantile(1/3)   # Lower tertile
q2 = customer_spend.quantile(2/3)   # Upper tertile

print("="*50)
print("          Customer Value Stratification")
print("="*50)
print(f"Threshold 1 (Low / Middle): £{q1:.0f}")
print(f"Threshold 2 (Middle / High): £{q2:.0f}")

# Define function to label customer value level
def label_level(amount):
    if amount <= q1:
        return "Low Value"
    elif amount <= q2:
        return "Middle Value"
    else:
        return "High Value"

# Convert Series to DataFrame and add level label for each customer
cust_df = customer_spend.reset_index()
cust_df.columns = ["CustomerID", "TotalSpend"]
cust_df["Level"] = cust_df["TotalSpend"].apply(label_level)

# Count customers of each level
level_count = cust_df["Level"].value_counts()
# Calculate total consumption of each level
level_spend = cust_df.groupby("Level")["TotalSpend"].sum()
# Calculate consumption percentage of each level
level_ratio = (level_spend / customer_spend.sum() * 100).round(2)

print("\n----- Number of Customers per Level -----")
print(level_count)

print("\n----- Total Spend & Proportion per Level -----")
stat_df = pd.DataFrame({
    "TotalSpend(£)": level_spend.round(0),
    "SpendRatio(%)": level_ratio
})
print(stat_df)

# Visualization 1: Bar chart for customer quantity distribution
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.unicode_minus'] = False

plt.figure()
level_count.plot(kind='bar', color=["#90EE90", "#87CEFA", "#FFB6C1"])
plt.title("Customer Distribution by Value Level", fontsize=14)
plt.xlabel("Customer Level")
plt.ylabel("Customer Count")
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Visualization 2: Pie chart for sales proportion of each level
plt.figure()
level_spend.plot(kind='pie', autopct='%1.1f%%', startangle=90,
                 labels=level_spend.index,
                 colors=["#90EE90", "#87CEFA", "#FFB6C1"])
plt.title("Sales Proportion by Customer Level", fontsize=14)
plt.ylabel("")
plt.tight_layout()
plt.show()