# Levi's India - RFM Analysis & Customer Segmentation

**Portfolio Project**: Complete end-to-end customer analytics demonstrating RFM methodology, segmentation, and actionable business insights.

---

## 📋 Project Overview

This project analyzes **50,000 Levi's India customers** and **140,000+ transactions** to:
- Segment customers using **RFM (Recency, Frequency, Monetary)** analysis
- Identify high-value segments and at-risk customers
- Provide data-driven marketing campaign recommendations
- Demonstrate real-world analytics skills applicable to e-commerce and retail

**Business Impact**: Analysis reveals that **top 40% of customers drive 82% of revenue**, enabling targeted retention strategies that could protect ₹54+ Crore in annual revenue.

---

## 🎯 Key Findings

### Champion Segment Analysis
- **16.8%** of customers (8,421 Champions)
- Generate **33%** of total revenue (₹21.9 Cr)
- **10x more valuable** than average customer
- **Recommendation**: VIP program with early access, free alterations → Expected ROI: 6-8x

### At-Risk Customer Recovery
- **1,050 high-value customers** at risk of churn
- **₹1.9 Cr** in historical value at stake
- Average **590 days** since last purchase
- **Recommendation**: Urgent win-back campaign (30% off + urgency) → Could recover ₹0.7 Cr

### New Customer Conversion
- **3,739 new customers** with only 1 order
- **Massive conversion opportunity** (3-4x LTV increase potential)
- **Recommendation**: 2nd purchase incentive (15% off within 30 days) → Expected ROI: 5-7x

---

## 📊 Methodology

### 1. RFM Calculation
```python
# Recency: Days since last purchase
# Frequency: Total number of orders
# Monetary: Total revenue contributed

rfm = transactions.groupby('customer_id').agg({
    'order_date': lambda x: (analysis_date - x.max()).days,
    'transaction_id': 'count',
    'order_value': 'sum'
})
```

### 2. Quintile Scoring (1-5 Scale)
- **Recency**: Lower days = Higher score (5 = recent, 1 = long ago)
- **Frequency**: More orders = Higher score
- **Monetary**: Higher spend = Higher score

### 3. Customer Segmentation
11 distinct segments identified based on RFM patterns:
- **Champions** (555, 554, 544): Best customers
- **Loyal Customers** (543, 444): Regular buyers
- **At Risk** (144, 244): Were good, now fading
- **New Customers** (511, 512): Recent first purchase
- And 7 more...

---

## 📁 Project Structure

```
levis_rfm_analysis/
│
├── 01_generate_levis_data.py      # Synthetic data generator
├── 02_rfm_analysis.py              # Main RFM analysis script
├── README.md                       # This file
│
├── data_customers.csv              # Customer master data (50K records)
├── data_transactions.csv           # Transaction history (140K records)
│
├── output_rfm_analysis.csv         # RFM scores + segments for all customers
├── output_segment_summary.csv      # Segment-level metrics
│
└── output_figures/
    ├── 01_segment_distribution.png      # Pie chart
    ├── 02_revenue_by_segment.png        # Bar chart
    ├── 03_rfm_score_distribution.png    # Score distributions
    ├── 04_segment_metrics.png           # Multi-metric comparison
    └── 05_rfm_scatter.png               # Customer distribution
```

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn
```

### Step 1: Generate Dataset
```bash
python 01_generate_levis_data.py
```
**Output**: `data_customers.csv` (50K customers), `data_transactions.csv` (140K transactions)

### Step 2: Run RFM Analysis
```bash
python 02_rfm_analysis.py
```
**Output**: 
- `output_rfm_analysis.csv` - Customer-level RFM scores
- `output_segment_summary.csv` - Segment metrics
- `output_figures/` - 5 visualization files

### Step 3: Review Results
- Check **Executive Summary** in console output
- View **visualizations** in `output_figures/`
- Explore **CSV files** for detailed data

---

## 📈 Visualizations Included

### 1. Segment Distribution (Pie Chart)
Shows proportion of customer base in each segment.

### 2. Revenue by Segment (Bar Chart)
Compares revenue contribution across segments. **Key insight**: Top 3 segments = 82% of revenue.

### 3. RFM Score Distributions
Histograms showing how customers score on Recency, Frequency, and Monetary dimensions.

### 4. Segment Performance Metrics
4-panel comparison:
- Average recency by segment
- Average frequency by segment
- Average monetary value by segment
- Customer count by segment

### 5. Customer Distribution Scatter
2D scatter plot (Recency vs Monetary) with Frequency as color gradient.

---

## 💡 Business Recommendations

### 🎯 Campaign 1: "Levi's Black" VIP Program
- **Target**: Champions (8,421 customers)
- **Offer**: Early access + free alterations + 25% birthday discount
- **Goal**: Retention & LTV maximization
- **Expected ROI**: 6-8x

### 🎯 Campaign 2: "Complete Your Look"
- **Target**: New Customers (3,739 customers)
- **Offer**: 15% off 2nd purchase within 30 days
- **Goal**: Convert one-timers to repeat buyers
- **Expected ROI**: 5-7x

### 🎯 Campaign 3: "Win-Back Special"
- **Target**: At-Risk + Can't Lose Them (1,050 customers)
- **Offer**: 30-40% off with urgency (7-day expiry)
- **Goal**: Reactivate before permanent churn
- **Expected ROI**: 7-12x

### 🎯 Campaign 4: Suppress Lost Segment
- **Target**: Lost + Hibernating (8,930 customers)
- **Action**: Remove from expensive email/SMS campaigns
- **Goal**: Cost savings
- **Impact**: Save ₹2-3 Cr annually

---

## 🔧 Technical Skills Demonstrated

- **Python**: pandas, numpy, matplotlib, seaborn
- **Data Analysis**: Aggregation, segmentation, statistical profiling
- **Business Metrics**: RFM scoring, CLV concepts, cohort behavior
- **Visualization**: Multi-panel charts, distribution plots, business dashboards
- **Synthetic Data**: Realistic dataset generation with segment-specific behaviors

---

## 📊 Dataset Statistics

### Customers (50,000 records)
- **Segments**: 11 distinct behavioral segments
- **Cities**: 8 major Indian metros
- **Date Range**: Jan 2020 - Dec 2022
- **Channels**: Store, Online, Mobile App

### Transactions (140,786 records)
- **Total Revenue**: ₹66.43 Crore
- **Average Order Value**: ₹4,718
- **Product Categories**: Jeans, Shirts, T-Shirts, Jackets, Accessories
- **Discount Usage**: 18.2% of orders

---

## 🎓 Key Learnings

### 1. Pareto Principle in Action
**16.8% of customers (Champions) = 33% of revenue**. Focus retention efforts here for maximum ROI.

### 2. Early Intervention Beats Recovery
**New Customers** with 1 order are easier to convert than winning back **Lost** customers. Prioritize onboarding.

### 3. Segment-Specific Strategies
One-size-fits-all marketing wastes budget. **At-Risk** needs urgency; **Champions** need exclusivity.

### 4. Data-Driven Resource Allocation
Suppress marketing to **Lost** segment (9.7% of base) → Saves ₹2-3 Cr without losing meaningful revenue.

---

## 📝 Interview Talking Points

**"Tell me about this project"**
> "I built an end-to-end RFM analysis for a hypothetical Levi's India dataset with 50K customers. I segmented the base into 11 behavioral groups and found that 40% of customers drive 82% of revenue. I designed segment-specific campaigns—VIP programs for Champions, conversion incentives for New Customers, and urgent win-backs for At-Risk. The analysis shows potential to protect ₹22 Cr in Champion revenue and recover ₹0.7 Cr from churning VIPs."

**"What tools did you use?"**
> "Python for the entire pipeline—pandas for data manipulation, numpy for calculations, matplotlib & seaborn for visualization. I generated synthetic data that mirrors real-world customer behavior patterns, calculated RFM using quintile scoring, and created 5 business-ready charts."

**"What was the business impact?"**
> "The segmentation revealed that we were wasting marketing budget on the 'Lost' segment (10% of customers, <4% of revenue). Reallocating that spend to high-ROI segments like Champions and At-Risk could improve marketing efficiency by 200-300% while protecting ₹54 Crore in annual revenue from the top 3 segments."

---

## 🔗 Related Concepts

- **Customer Lifetime Value (CLV)**: Predictive extension of this RFM work
- **Churn Prediction**: Machine learning to forecast which customers will leave
- **Cohort Analysis**: Tracking retention over time for different customer cohorts
- **A/B Testing**: Measuring campaign effectiveness experimentally

---

## 📧 Contact

**Project by**: [Your Name]  
**LinkedIn**: [Your LinkedIn]  
**GitHub**: [Your GitHub]  
**Email**: [Your Email]

---

## 📄 License

This is a portfolio project using synthetic data. Feel free to use as reference for your own analytics projects.

---

**⭐ If you found this project helpful, please star the repository!**
