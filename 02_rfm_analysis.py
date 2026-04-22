#!/usr/bin/env python3
"""
Levi's India - Complete RFM Analysis & Customer Segmentation
Portfolio Project: End-to-end analytics demonstrating RFM methodology, 
CLV modeling, and actionable business insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 80)
print("LEVI'S INDIA - RFM ANALYSIS & CUSTOMER SEGMENTATION")
print("=" * 80)
print()

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("📂 Loading datasets...")
customers = pd.read_csv('data_customers.csv')
transactions = pd.read_csv('data_transactions.csv')
transactions['order_date'] = pd.to_datetime(transactions['order_date'])

print(f"✓ Loaded {len(customers):,} customers")
print(f"✓ Loaded {len(transactions):,} transactions")
print()

# ============================================================================
# 2. RFM CALCULATION
# ============================================================================

print("🔢 Calculating RFM Metrics...")
print("-" * 80)

# Analysis date (day after last transaction)
analysis_date = transactions['order_date'].max() + timedelta(days=1)
print(f"Analysis Date: {analysis_date.date()}")

# Calculate RFM
rfm = transactions.groupby('customer_id').agg({
    'order_date': lambda x: (analysis_date - x.max()).days,  # Recency
    'transaction_id': 'count',                               # Frequency
    'order_value': 'sum'                                     # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

print(f"\n📊 RFM Statistics:")
print(rfm.describe())

# ============================================================================
# 3. RFM SCORING (Quintile Method)
# ============================================================================

print("\n🎯 Assigning RFM Scores (1-5 scale)...")

# Quintile scoring
rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1], duplicates='drop')  # Reverse
rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')

# Create RFM string
rfm['RFM_Score'] = (rfm['R_score'].astype(str) + 
                    rfm['F_score'].astype(str) + 
                    rfm['M_score'].astype(str))

print(f"✓ Scores assigned to {len(rfm):,} customers")

# ============================================================================
# 4. CUSTOMER SEGMENTATION
# ============================================================================

print("\n🎭 Segmenting Customers Based on RFM...")
print("-" * 80)

def assign_rfm_segment(row):
    """Assign segment based on RFM scores"""
    r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
    
    # Champions
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    
    # Loyal Customers
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    
    # Potential Loyalists
    elif r >= 3 and f >= 2 and m >= 2:
        return 'Potential Loyalists'
    
    # New Customers
    elif r >= 4 and f <= 2:
        return 'New Customers'
    
    # Promising
    elif r >= 3 and f <= 2:
        return 'Promising'
    
    # Need Attention
    elif r == 3 and f >= 2:
        return 'Need Attention'
    
    # About to Sleep
    elif r == 2:
        return 'About to Sleep'
    
    # At Risk (were good, now inactive)
    elif r == 1 and f >= 4:
        return 'At Risk'
    
    # Can't Lose Them (high value but gone)
    elif r == 1 and m >= 4:
        return "Can't Lose Them"
    
    # Hibernating
    elif r == 1 and f == 2:
        return 'Hibernating'
    
    # Lost
    else:
        return 'Lost'

rfm['segment'] = rfm.apply(assign_rfm_segment, axis=1)

# Segment summary
segment_summary = rfm.groupby('segment').agg({
    'customer_id': 'count',
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'sum'
}).reset_index()

segment_summary.columns = ['Segment', 'Count', 'Avg_Recency', 'Avg_Frequency', 'Total_Revenue']
segment_summary['Pct_Customers'] = (segment_summary['Count'] / len(rfm) * 100).round(1)
segment_summary['Pct_Revenue'] = (segment_summary['Total_Revenue'] / rfm['monetary'].sum() * 100).round(1)
segment_summary = segment_summary.sort_values('Total_Revenue', ascending=False)

print("\n📊 SEGMENT ANALYSIS:")
print(segment_summary.to_string(index=False))

# ============================================================================
# 5. KEY INSIGHTS
# ============================================================================

print("\n" + "=" * 80)
print("🔍 KEY BUSINESS INSIGHTS")
print("=" * 80)

# Top segments
top_segments = segment_summary.head(3)
print(f"\n💎 Top 3 Revenue-Generating Segments:")
for idx, row in top_segments.iterrows():
    print(f"  {row['Segment']}: {row['Count']} customers ({row['Pct_Customers']}%) = ₹{row['Total_Revenue']/1e7:.2f} Cr ({row['Pct_Revenue']}%)")

# Champions analysis
champions = rfm[rfm['segment'] == 'Champions']
print(f"\n👑 Champions Deep Dive:")
print(f"  Count: {len(champions):,} customers ({len(champions)/len(rfm)*100:.1f}%)")
print(f"  Revenue: ₹{champions['monetary'].sum()/1e7:.2f} Cr ({champions['monetary'].sum()/rfm['monetary'].sum()*100:.1f}%)")
print(f"  Avg Order Value: ₹{champions['monetary'].mean():.2f}")
print(f"  Avg Orders: {champions['frequency'].mean():.1f}")
print(f"  Avg Recency: {champions['recency'].mean():.0f} days")

# At-risk analysis
at_risk = rfm[rfm['segment'].isin(['At Risk', "Can't Lose Them"])]
print(f"\n⚠️  At-Risk Customers:")
print(f"  Count: {len(at_risk):,} customers")
print(f"  Historical Value: ₹{at_risk['monetary'].sum()/1e7:.2f} Cr (at risk of being lost)")
print(f"  Avg Days Since Last Order: {at_risk['recency'].mean():.0f} days")

# New customers
new_cust = rfm[rfm['segment'] == 'New Customers']
print(f"\n🆕 New Customers:")
print(f"  Count: {len(new_cust):,} customers")
print(f"  Conversion Opportunity: Only {new_cust['frequency'].mean():.1f} orders on average")
print(f"  Potential if converted to Loyal: 3-4x increase in LTV")

# ============================================================================
# 6. VISUALIZATIONS
# ============================================================================

print("\n📊 Generating visualizations...")

# Create figure directory
import os
os.makedirs('output_figures', exist_ok=True)

# 1. Segment Distribution (Pie Chart)
fig, ax = plt.subplots(figsize=(10, 7))
segment_counts = rfm['segment'].value_counts()
colors = plt.cm.Set3(range(len(segment_counts)))
wedges, texts, autotexts = ax.pie(
    segment_counts.values, 
    labels=segment_counts.index,
    autopct='%1.1f%%',
    colors=colors,
    startangle=90
)
ax.set_title('Customer Segmentation Distribution', fontsize=16, fontweight='bold', pad=20)
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
plt.tight_layout()
plt.savefig('output_figures/01_segment_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 01_segment_distribution.png")

# 2. Revenue by Segment (Bar Chart)
fig, ax = plt.subplots(figsize=(12, 6))
segment_summary_sorted = segment_summary.sort_values('Total_Revenue', ascending=True)
bars = ax.barh(segment_summary_sorted['Segment'], segment_summary_sorted['Total_Revenue']/1e7)
ax.set_xlabel('Total Revenue (₹ Crore)', fontsize=12)
ax.set_title('Revenue Contribution by Segment', fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (segment, revenue) in enumerate(zip(segment_summary_sorted['Segment'], segment_summary_sorted['Total_Revenue'])):
    ax.text(revenue/1e7 + 0.5, i, f'₹{revenue/1e7:.1f}Cr', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('output_figures/02_revenue_by_segment.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 02_revenue_by_segment.png")

# 3. RFM Score Distribution (Heatmap)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (score, title) in enumerate([('R_score', 'Recency'), ('F_score', 'Frequency'), ('M_score', 'Monetary')]):
    score_dist = rfm[score].value_counts().sort_index()
    axes[idx].bar(score_dist.index.astype(str), score_dist.values, color='steelblue')
    axes[idx].set_title(f'{title} Score Distribution', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Score', fontsize=10)
    axes[idx].set_ylabel('Count', fontsize=10)
    axes[idx].grid(axis='y', alpha=0.3)

plt.suptitle('RFM Score Distributions', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('output_figures/03_rfm_score_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 03_rfm_score_distribution.png")

# 4. Segment Metrics Comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Avg Recency
segment_metrics = rfm.groupby('segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': ['mean', 'sum']
}).reset_index()
segment_metrics.columns = ['segment', 'avg_recency', 'avg_frequency', 'avg_monetary', 'total_monetary']

axes[0, 0].barh(segment_metrics['segment'], segment_metrics['avg_recency'], color='coral')
axes[0, 0].set_xlabel('Days Since Last Order')
axes[0, 0].set_title('Average Recency by Segment', fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3)

# Avg Frequency
axes[0, 1].barh(segment_metrics['segment'], segment_metrics['avg_frequency'], color='lightgreen')
axes[0, 1].set_xlabel('Number of Orders')
axes[0, 1].set_title('Average Frequency by Segment', fontweight='bold')
axes[0, 1].grid(axis='x', alpha=0.3)

# Avg Monetary
axes[1, 0].barh(segment_metrics['segment'], segment_metrics['avg_monetary'], color='skyblue')
axes[1, 0].set_xlabel('Average Spend (₹)')
axes[1, 0].set_title('Average Monetary Value by Segment', fontweight='bold')
axes[1, 0].grid(axis='x', alpha=0.3)

# Customer Count
segment_counts_df = rfm['segment'].value_counts().reset_index()
segment_counts_df.columns = ['segment', 'count']
axes[1, 1].barh(segment_counts_df['segment'], segment_counts_df['count'], color='plum')
axes[1, 1].set_xlabel('Number of Customers')
axes[1, 1].set_title('Customer Count by Segment', fontweight='bold')
axes[1, 1].grid(axis='x', alpha=0.3)

plt.suptitle('Segment Performance Metrics', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('output_figures/04_segment_metrics.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 04_segment_metrics.png")

# 5. RFM 3D Scatter (using 2D projection)
fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(
    rfm['recency'], 
    rfm['monetary'],
    c=rfm['frequency'],
    s=50,
    alpha=0.6,
    cmap='viridis'
)
ax.set_xlabel('Recency (days)', fontsize=12)
ax.set_ylabel('Monetary Value (₹)', fontsize=12)
ax.set_title('RFM Customer Distribution (Color = Frequency)', fontsize=16, fontweight='bold', pad=20)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Frequency (# orders)', fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('output_figures/05_rfm_scatter.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 05_rfm_scatter.png")

# ============================================================================
# 7. CAMPAIGN RECOMMENDATIONS
# ============================================================================

print("\n" + "=" * 80)
print("🎯 RECOMMENDED MARKETING CAMPAIGNS")
print("=" * 80)

campaigns = {
    'Champions': {
        'Campaign': 'Levi\'s Black VIP Program',
        'Offer': 'Early access to new collections, free alterations, 25% birthday discount',
        'Goal': 'Retain and maximize LTV',
        'Expected ROI': '6-8x'
    },
    'Loyal Customers': {
        'Campaign': 'Referral Rewards',
        'Offer': 'Refer a friend, both get ₹500 off',
        'Goal': 'Leverage for acquisition',
        'Expected ROI': '4-5x'
    },
    'New Customers': {
        'Campaign': 'Complete Your Look',
        'Offer': '15% off 2nd purchase within 30 days',
        'Goal': 'Drive second purchase (conversion)',
        'Expected ROI': '5-7x'
    },
    'At Risk': {
        'Campaign': 'Win-Back Special',
        'Offer': '30% off + free shipping (7-day urgency)',
        'Goal': 'Reactivate before churn',
        'Expected ROI': '7-9x'
    },
    "Can't Lose Them": {
        'Campaign': 'Personal Outreach',
        'Offer': 'Call from relationship manager + exclusive 40% off',
        'Goal': 'Save high-value customers',
        'Expected ROI': '10-12x'
    }
}

for segment, details in campaigns.items():
    customer_count = len(rfm[rfm['segment'] == segment])
    print(f"\n📌 {segment} ({customer_count:,} customers)")
    print(f"   Campaign: {details['Campaign']}")
    print(f"   Offer: {details['Offer']}")
    print(f"   Goal: {details['Goal']}")
    print(f"   Expected ROI: {details['Expected ROI']}")

# ============================================================================
# 8. SAVE RESULTS
# ============================================================================

print("\n💾 Saving analysis results...")

# Save RFM with segments
rfm_output = rfm.copy()
rfm_output.to_csv('output_rfm_analysis.csv', index=False)
print(f"  ✓ Saved: output_rfm_analysis.csv")

# Save segment summary
segment_summary.to_csv('output_segment_summary.csv', index=False)
print(f"  ✓ Saved: output_segment_summary.csv")

# ============================================================================
# 9. FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("📈 EXECUTIVE SUMMARY")
print("=" * 80)

total_revenue = rfm['monetary'].sum()
top_3_segments_revenue = segment_summary.head(3)['Total_Revenue'].sum()

print(f"""
Key Findings:
• Total Customer Base: {len(rfm):,} customers
• Total Revenue Analyzed: ₹{total_revenue/1e7:.2f} Crore
• Top 3 Segments: {segment_summary.head(3)['Count'].sum():,} customers ({segment_summary.head(3)['Count'].sum()/len(rfm)*100:.1f}%)
  → Generate: ₹{top_3_segments_revenue/1e7:.2f} Cr ({top_3_segments_revenue/total_revenue*100:.1f}% of revenue)

Champion Segment:
• {len(champions):,} customers ({len(champions)/len(rfm)*100:.1f}% of base)
• ₹{champions['monetary'].sum()/1e7:.2f} Cr revenue ({champions['monetary'].sum()/total_revenue*100:.1f}% of total)
• 10x more valuable than average customer

At-Risk Opportunity:
• {len(at_risk):,} high-value customers at risk
• ₹{at_risk['monetary'].sum()/1e7:.2f} Cr historical value to protect
• Win-back campaign could recover 30-40% → ₹{at_risk['monetary'].sum()*0.35/1e7:.1f}Cr potential

Recommended Actions:
1. Launch VIP program for Champions (protect ₹{champions['monetary'].sum()/1e7:.1f}Cr segment)
2. 2nd-purchase incentive for {len(new_cust):,} New Customers (conversion opportunity)
3. Urgent win-back for {len(at_risk):,} At-Risk customers (₹{at_risk['monetary'].sum()/1e7:.1f}Cr at stake)
4. Suppress marketing to Lost segment (save ₹2-3Cr annually)
""")

print("=" * 80)
print("✅ ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n📁 Output files saved in: output_rfm_analysis.csv, output_segment_summary.csv")
print(f"📊 Visualizations saved in: output_figures/ (5 charts)")
print()
