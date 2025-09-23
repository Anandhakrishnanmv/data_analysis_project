import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for better plots
plt.style.use('default')
sns.set_palette("husl")

# Load CSV file into a DataFrame
df = pd.read_csv('Sample_Superstore.csv', encoding='ISO-8859-1')

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print("=== REGIONAL SALES ANALYSIS ===")
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")
print()

# Basic sales statistics
total_sales = df['Sales'].sum()
total_orders = df['Order ID'].nunique()

print("=== BASIC SALES STATISTICS ===")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Orders: {total_orders:,}")
print()

# Sales by Region - Overview
print("=== SALES DISTRIBUTION BY REGION ===")
region_sales = df.groupby('Region').agg({
    'Sales': 'sum',
    'Quantity': 'sum',
    'Order ID': 'nunique',
    'Customer ID': 'nunique'
}).round(2)

region_sales['Avg_Order_Value'] = (region_sales['Sales'] / region_sales['Order ID']).round(2)
region_sales['Sales_Percentage'] = (region_sales['Sales'] / total_sales * 100).round(2)
region_sales['Customers_Percentage'] = (region_sales['Customer ID'] / region_sales['Customer ID'].sum() * 100).round(2)
region_sales = region_sales.sort_values('Sales', ascending=False)

print(region_sales)
print()

# Detailed Regional Analysis
print("=== DETAILED REGIONAL ANALYSIS ===")
regions = region_sales.index.tolist()

for region in regions:
    print(f"\n{'='*60}")
    print(f"REGION: {region.upper()}")
    print('='*60)

    # Filter data for this region
    region_data = df[df['Region'] == region]

    # Sales statistics for this region
    region_total_sales = region_data['Sales'].sum()
    region_orders = region_data['Order ID'].nunique()
    region_customers = region_data['Customer ID'].nunique()

    print("Region Overview:")
    print(f"   - Total Sales: ${region_total_sales:,.2f}")
    print(f"   - Total Orders: {region_orders:,}")
    print(f"   - Total Customers: {region_customers:,}")
    print(f"   - Avg Order Value: ${region_total_sales/region_orders:.2f}")
    print(f"   - % of Total Sales: {region_total_sales/total_sales*100:.1f}%")

    # Top categories in this region
    print("\nTop Categories:")
    region_categories = region_data.groupby('Category').agg({
        'Sales': 'sum',
        'Quantity': 'sum'
    }).round(2).sort_values('Sales', ascending=False)

    for idx, (category, data) in enumerate(region_categories.iterrows(), 1):
        print(f"   {idx}. {category}: ${data['Sales']:,.2f} ({data['Sales']/region_total_sales*100:.1f}% of region sales)")

    # Top sub-categories in this region
    print("\nTop Sub-Categories:")
    region_subcats = region_data.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Quantity': 'sum'
    }).round(2).sort_values('Sales', ascending=False).head(5)

    for idx, (subcat, data) in enumerate(region_subcats.iterrows(), 1):
        print(f"   {idx}. {subcat}: ${data['Sales']:,.2f} ({data['Sales']/region_total_sales*100:.1f}% of region sales)")

    # Top products in this region
    print("\nTop Products:")
    region_products = region_data.groupby('Product Name').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).round(2).sort_values('Sales', ascending=False).head(5)

    for idx, (product, data) in enumerate(region_products.iterrows(), 1):
        print(f"   {idx}. {product}: ${data['Sales']:,.2f} ({data['Quantity']:.0f} units, {data['Order ID']} orders)")

    # Top states in this region
    print("\nTop States:")
    region_states = region_data.groupby('State').agg({
        'Sales': 'sum'
    }).round(2).sort_values('Sales', ascending=False).head(3)

    for idx, (state, data) in enumerate(region_states.iterrows(), 1):
        print(f"   {idx}. {state}: ${data['Sales']:,.2f}")

    # Customer segments in this region
    print("\nCustomer Segments:")
    region_segments = region_data.groupby('Segment').agg({
        'Sales': 'sum'
    }).round(2).sort_values('Sales', ascending=False)

    for segment, data in region_segments.iterrows():
        print(f"   - {segment}: ${data['Sales']:,.2f} ({data['Sales']/region_total_sales*100:.1f}% of region sales)")

print(f"\n{'='*60}")
print("REGIONAL COMPARISON SUMMARY")
print('='*60)

# Regional preferences comparison
print("\nTop Category by Region:")
for region in regions:
    region_data = df[df['Region'] == region]
    top_category = region_data.groupby('Category')['Sales'].sum().idxmax()
    top_category_sales = region_data.groupby('Category')['Sales'].sum().max()
    print(f"   - {region}: {top_category}")

print("\nTop Sub-Category by Region:")
for region in regions:
    region_data = df[df['Region'] == region]
    top_subcat = region_data.groupby('Sub-Category')['Sales'].sum().idxmax()
    top_subcat_sales = region_data.groupby('Sub-Category')['Sales'].sum().max()
    print(f"   - {region}: {top_subcat}")

print("\nTop Product by Region:")
for region in regions:
    region_data = df[df['Region'] == region]
    top_product = region_data.groupby('Product Name')['Sales'].sum().idxmax()
    top_product_sales = region_data.groupby('Product Name')['Sales'].sum().max()
    print(f"   - {region}: {top_product}")

# Create visualizations
print("\n=== CREATING VISUALIZATIONS ===")

# Sales by Region
plt.figure(figsize=(10, 6))
region_sales['Sales'].plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Sales Distribution by Region')
plt.ylabel('')
plt.tight_layout()
plt.savefig('regional_sales_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: regional_sales_distribution.png")

# Regional comparison bar chart
plt.figure(figsize=(12, 6))
region_sales['Sales'].plot(kind='bar', color='skyblue')
plt.title('Sales by Region')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('regional_sales_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: regional_sales_comparison.png")

# Top categories by region
plt.figure(figsize=(14, 8))
regions_list = []
categories_list = []
sales_list = []

for region in regions:
    region_data = df[df['Region'] == region]
    top_cats = region_data.groupby('Category')['Sales'].sum().sort_values(ascending=False).head(3)
    for cat in top_cats.index:
        regions_list.append(region)
        categories_list.append(cat)
        sales_list.append(top_cats[cat])

regional_cats_df = pd.DataFrame({
    'Region': regions_list,
    'Category': categories_list,
    'Sales': sales_list
})

pivot_df = regional_cats_df.pivot(index='Region', columns='Category', values='Sales').fillna(0)

pivot_df.plot(kind='bar', figsize=(14, 8))
plt.title('Top Categories by Region')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('regional_category_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: regional_category_comparison.png")

# Top sub-categories by region
plt.figure(figsize=(16, 10))
regions_list = []
subcats_list = []
sales_list = []

for region in regions:
    region_data = df[df['Region'] == region]
    top_subcats = region_data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5)
    for subcat in top_subcats.index:
        regions_list.append(region)
        subcats_list.append(subcat)
        sales_list.append(top_subcats[subcat])

regional_subcats_df = pd.DataFrame({
    'Region': regions_list,
    'Sub_Category': subcats_list,
    'Sales': sales_list
})

# Create a grouped bar chart with regions on x-axis and sub-categories as legend
regional_subcats_pivot = regional_subcats_df.pivot_table(
    index='Region',
    columns='Sub_Category',
    values='Sales',
    aggfunc='sum'
).fillna(0)

regional_subcats_pivot.plot(kind='bar', figsize=(16, 10))
plt.title('Top Sub-Categories by Region')
plt.ylabel('Sales ($)')
plt.xlabel('Region')
plt.xticks(rotation=45)
plt.legend(title='Sub-Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('regional_subcategory_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: regional_subcategory_comparison.png")

print("\n=== ANALYSIS COMPLETE ===")
print("All visualizations have been saved as PNG files.")
print("Key files created:")
print("- regional_sales_distribution.png")
print("- regional_sales_comparison.png")
print("- regional_category_comparison.png")
print("- regional_subcategory_comparison.png")
