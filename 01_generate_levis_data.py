#!/usr/bin/env python3
"""
Levi's India - Customer Transaction Data Generator
Generates realistic synthetic data for RFM & CLV analysis portfolio project
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

print("🏭 Generating Levi's India Customer Transaction Dataset...")
print("=" * 70)

# ============================================================================
# CONFIGURATION
# ============================================================================

NUM_CUSTOMERS = 50000
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2022, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days

# Customer segments distribution (realistic proportions)
SEGMENT_DISTRIBUTION = {
    'Champions': 0.03,           # 3% - Best customers
    'Loyal': 0.06,               # 6% - Regular buyers
    'Potential_Loyal': 0.09,     # 9% - Growing customers
    'New_Customers': 0.15,       # 15% - Recent first purchase
    'Promising': 0.12,           # 12% - Above average
    'Need_Attention': 0.10,      # 10% - Declining
    'About_to_Sleep': 0.08,      # 8% - Risk of churn
    'At_Risk': 0.07,             # 7% - High churn risk
    'Cant_Lose': 0.04,           # 4% - VIPs gone silent
    'Hibernating': 0.13,         # 13% - Low engagement
    'Lost': 0.13                 # 13% - Churned
}

# Product categories and price ranges
PRODUCT_CATALOG = {
    'Jeans': {'min': 2500, 'max': 8000, 'avg': 4500},
    'Shirts': {'min': 1500, 'max': 4500, 'avg': 2800},
    'T-Shirts': {'min': 800, 'max': 2500, 'avg': 1500},
    'Jackets': {'min': 4000, 'max': 12000, 'avg': 7500},
    'Accessories': {'min': 500, 'max': 2000, 'avg': 1200}
}

CHANNELS = ['Store', 'Online', 'Mobile_App']
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']

# ============================================================================
# SEGMENT BEHAVIOR PARAMETERS
# ============================================================================

SEGMENT_PARAMS = {
    'Champions': {
        'frequency': (6, 12),           # Orders per year
        'recency_days': (0, 30),        # Last purchase days ago
        'avg_order_value': (5000, 9000),
        'product_variety': (3, 5),      # Different product types
        'discount_usage': 0.1,          # 10% use discounts
    },
    'Loyal': {
        'frequency': (4, 6),
        'recency_days': (20, 60),
        'avg_order_value': (3500, 6000),
        'product_variety': (2, 4),
        'discount_usage': 0.2,
    },
    'Potential_Loyal': {
        'frequency': (3, 4),
        'recency_days': (40, 90),
        'avg_order_value': (3000, 5000),
        'product_variety': (2, 3),
        'discount_usage': 0.3,
    },
    'New_Customers': {
        'frequency': (1, 2),
        'recency_days': (0, 30),
        'avg_order_value': (2500, 4500),
        'product_variety': (1, 2),
        'discount_usage': 0.15,
    },
    'Promising': {
        'frequency': (3, 4),
        'recency_days': (50, 100),
        'avg_order_value': (3200, 5500),
        'product_variety': (2, 3),
        'discount_usage': 0.25,
    },
    'Need_Attention': {
        'frequency': (2, 3),
        'recency_days': (90, 150),
        'avg_order_value': (2800, 4500),
        'product_variety': (1, 2),
        'discount_usage': 0.4,
    },
    'About_to_Sleep': {
        'frequency': (2, 3),
        'recency_days': (120, 180),
        'avg_order_value': (2500, 4000),
        'product_variety': (1, 2),
        'discount_usage': 0.5,
    },
    'At_Risk': {
        'frequency': (3, 5),            # Were good customers
        'recency_days': (180, 300),
        'avg_order_value': (4000, 7000),
        'product_variety': (2, 3),
        'discount_usage': 0.3,
    },
    'Cant_Lose': {
        'frequency': (5, 8),            # Were Champions
        'recency_days': (200, 400),
        'avg_order_value': (5500, 10000),
        'product_variety': (3, 4),
        'discount_usage': 0.15,
    },
    'Hibernating': {
        'frequency': (1, 2),
        'recency_days': (300, 500),
        'avg_order_value': (2000, 3500),
        'product_variety': (1, 2),
        'discount_usage': 0.6,
    },
    'Lost': {
        'frequency': (1, 2),
        'recency_days': (500, 900),
        'avg_order_value': (1800, 3000),
        'product_variety': (1, 1),
        'discount_usage': 0.7,
    }
}

# ============================================================================
# GENERATE CUSTOMERS
# ============================================================================

customers = []
customer_id = 1000

for segment, proportion in SEGMENT_DISTRIBUTION.items():
    num_in_segment = int(NUM_CUSTOMERS * proportion)
    params = SEGMENT_PARAMS[segment]
    
    for _ in range(num_in_segment):
        customers.append({
            'customer_id': f'CUST{customer_id:06d}',
            'segment': segment,
            'join_date': START_DATE + timedelta(days=random.randint(0, TOTAL_DAYS - 180)),
            'city': random.choice(CITIES),
            'preferred_channel': random.choice(CHANNELS),
            'frequency_target': random.randint(*params['frequency']),
            'recency_target': random.randint(*params['recency_days']),
            'aov_min': params['avg_order_value'][0],
            'aov_max': params['avg_order_value'][1],
            'product_variety': random.randint(*params['product_variety']),
            'discount_prone': random.random() < params['discount_usage']
        })
        customer_id += 1

customers_df = pd.DataFrame(customers)
print(f"✓ Generated {len(customers_df)} customers across {len(SEGMENT_DISTRIBUTION)} segments")

# ============================================================================
# GENERATE TRANSACTIONS
# ============================================================================

transactions = []
transaction_id = 100000

for idx, customer in customers_df.iterrows():
    num_orders = customer['frequency_target']
    
    # Calculate order dates
    days_active = (END_DATE - customer['join_date']).days
    last_order_date = END_DATE - timedelta(days=customer['recency_target'])
    
    if days_active <= 0 or num_orders == 0:
        continue
    
    # Generate order dates with realistic spacing
    if num_orders == 1:
        order_dates = [last_order_date]
    else:
        # Distribute orders from join date to last order date
        order_dates = []
        time_span = (last_order_date - customer['join_date']).days
        if time_span > 0:
            intervals = sorted([random.randint(0, time_span) for _ in range(num_orders)])
            order_dates = [customer['join_date'] + timedelta(days=d) for d in intervals]
        else:
            order_dates = [last_order_date]
    
    # Generate each order
    for order_date in order_dates:
        # Determine number of items in this order
        num_items = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
        
        order_value = 0
        order_items = []
        
        for _ in range(num_items):
            # Select product category
            if customer['product_variety'] == 1:
                category = 'Jeans'  # Denim loyalists
            else:
                category = random.choice(list(PRODUCT_CATALOG.keys()))
            
            # Generate price with some variance
            base_price = random.uniform(
                PRODUCT_CATALOG[category]['min'],
                PRODUCT_CATALOG[category]['max']
            )
            
            # Apply discount if customer is discount-prone
            if customer['discount_prone'] and random.random() < 0.6:
                discount_pct = random.choice([10, 15, 20, 25, 30])
                final_price = base_price * (1 - discount_pct / 100)
                has_discount = True
            else:
                final_price = base_price
                discount_pct = 0
                has_discount = False
            
            order_value += final_price
            order_items.append(category)
        
        # Apply customer's AOV range
        order_value = np.clip(
            order_value,
            customer['aov_min'],
            customer['aov_max']
        )
        
        # Select channel (80% preferred, 20% other)
        if random.random() < 0.8:
            channel = customer['preferred_channel']
        else:
            channel = random.choice(CHANNELS)
        
        transactions.append({
            'transaction_id': f'TXN{transaction_id:08d}',
            'customer_id': customer['customer_id'],
            'order_date': order_date,
            'order_value': round(order_value, 2),
            'num_items': num_items,
            'channel': channel,
            'city': customer['city'],
            'has_discount': has_discount,
            'discount_pct': discount_pct if has_discount else 0,
            'product_categories': '|'.join(order_items)
        })
        transaction_id += 1
    
    if (idx + 1) % 10000 == 0:
        print(f"  Processed {idx + 1}/{len(customers_df)} customers...")

transactions_df = pd.DataFrame(transactions)
print(f"✓ Generated {len(transactions_df)} transactions")

# ============================================================================
# SAVE DATASETS
# ============================================================================

print("\n📦 Saving datasets...")

customers_df.to_csv('data_customers.csv', index=False)
print(f"✓ Saved: data_customers.csv ({len(customers_df)} rows)")

transactions_df.to_csv('data_transactions.csv', index=False)
print(f"✓ Saved: data_transactions.csv ({len(transactions_df)} rows)")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n📊 DATASET SUMMARY")
print("=" * 70)

print(f"\n🔢 Customer Base:")
print(f"  Total Customers: {len(customers_df):,}")
print(f"  Date Range: {START_DATE.date()} to {END_DATE.date()}")
print(f"\n  Segment Distribution:")
for segment in customers_df['segment'].value_counts().sort_index():
    print(f"    {segment}")

print(f"\n💳 Transactions:")
print(f"  Total Transactions: {len(transactions_df):,}")
print(f"  Total Revenue: ₹{transactions_df['order_value'].sum()/1e7:.2f} Crore")
print(f"  Average Order Value: ₹{transactions_df['order_value'].mean():.2f}")
print(f"  Date Range: {transactions_df['order_date'].min()} to {transactions_df['order_date'].max()}")

print(f"\n📦 Channel Distribution:")
print(transactions_df['channel'].value_counts())

print(f"\n🏙️ Top Cities:")
print(transactions_df['city'].value_counts().head())

print(f"\n🎁 Discount Usage:")
print(f"  Orders with discount: {transactions_df['has_discount'].sum():,} ({transactions_df['has_discount'].mean()*100:.1f}%)")

print("\n" + "=" * 70)
print("✅ Dataset generation complete! Ready for analysis.")
print("=" * 70)
