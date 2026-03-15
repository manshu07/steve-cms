# Pricing Calculations & Formulas

Mathematical framework for calculating value-based pricing, margins, and unit economics for SaaS products.

## Table of Contents
- [Value-Based Pricing Calculation](#value-based-pricing-calculation)
- [Margin & Cost Analysis](#margin--cost-analysis)
- [Unit Economics](#unit-economics)
- [Pricing Psychology Formulas](#pricing-psychology-formulas)
- [A/B Testing Calculations](#ab-testing-calculations)

---

## Value-Based Pricing Calculation

### Core Formula

```
Value Created =
(Time Saved × Hourly Rate)
+ Revenue Generated
+ Costs Reduced
+ Risk Mitigation Value
```

### Recommended Price Range

```
Recommended Price = 10-30% of Value Created
```

**Why 10-30%?**
- Below 10%: Leaving money on table
- 10-20%: Competitive pricing, high volume
- 20-30%: Premium pricing, strong differentiation
- Above 30%: Requires exceptional value or lack of competition

---

### Detailed Calculation Example

#### Scenario: Project Management SaaS

**Product Saves Time:**
- Team of 10 people
- Saves 2 hours/week per person
- Average hourly rate: $75
- Weeks per month: 4

**Calculation:**
```
Time Value = 10 people × 2 hours/week × $75/hour × 4 weeks
Time Value = $6,000/month in saved time

Additional Value:
- Reduced overtime costs: $1,000/month
- Improved project delivery: $2,000/month (revenue protection)
------------------------------------------
Total Value Created: $9,000/month

Price at 15% (competitive market):
$9,000 × 0.15 = $1,350/month

Recommended Pricing:
$997/month or $99/user/month (for 10 users)
```

---

### Revenue Generation Value

For products that directly generate revenue:

```
Revenue Value = (Revenue Increase × Conversion Rate) + (Average Deal Size × Additional Deals)
```

**Example: Email Marketing Tool**
- Sends 100,000 emails/month
- Improves open rate by 5% (5,000 more opens)
- 2% conversion to sales
- Average deal size: $100

```
Additional Sales = 5,000 opens × 2% × $100
Additional Sales = 100 sales × $100 = $10,000/month

Price at 20% (high ROI tool):
$10,000 × 0.20 = $2,000/month
```

---

### Cost Reduction Value

For products that reduce operational costs:

```
Cost Reduction = (Old Cost - New Cost) + (Reduced Labor Costs)
```

**Example: Cloud Cost Optimization Tool**
- Current cloud spend: $50,000/month
- Tool saves: 20% reduction
- Implementation cost: $500/month (tool subscription)

```
Monthly Savings = $50,000 × 20%
Monthly Savings = $10,000

Price at 25% (direct ROI tool):
$10,000 × 0.25 = $2,500/month
```

---

## Margin & Cost Analysis

### Gross Margin Formula

```
Gross Margin = (Revenue - COGS) / Revenue

COGS (Cost of Goods Sold) for SaaS:
- Hosting/Infrastructure costs
- AI/ML inference costs
- Third-party API costs
- Payment processing fees
- Customer support (allocated)
```

### Target SaaS Margins

| Tier | Target Gross Margin | Why |
|------|-------------------|-----|
| **Early-stage** | 60-70% | Scale and learn |
| **Growth-stage** | 70-80% | Standard SaaS benchmark |
| **Mature** | 80-85% | Optimized operations |
| **Rule of 50** | 50%+ growth + 50%+ margin | Balanced growth |

### Reverse Engineering Price from Margin

```
Price = Cost / (1 - Target Margin)
```

**Example: AI-Powered Tool**
- Infrastructure cost: $5/user/month
- AI inference cost: $3/user/month
- Support cost: $2/user/month
- Total Cost: $10/user/month
- Target margin: 75%

```
Price = $10 / (1 - 0.75)
Price = $10 / 0.25
Price = $40/user/month

Verification:
Revenue: $40
Cost: $10
Margin: ($40 - $10) / $40 = 75% ✓
```

---

### AI Product Cost Modeling

#### Per-Request Cost Calculation

```
Cost per Request =
(Model Input Cost × Input Tokens)
+ (Model Output Cost × Output Tokens)
+ (Infrastructure Overhead)
```

**Example: GPT-4 Integration**
- Input tokens: 1,000 (user prompt)
- Output tokens: 500 (AI response)
- GPT-4o input: $2.50 per 1M tokens
- GPT-4o output: $10.00 per 1M tokens
- Infrastructure overhead: 20%

```
Input Cost = (1,000 / 1,000,000) × $2.50 = $0.0025
Output Cost = (500 / 1,000,000) × $10.00 = $0.0050
Base Cost = $0.0075
With Overhead = $0.0075 × 1.20 = $0.009 per request

Pricing for 75% margin:
Price = $0.009 / (1 - 0.75) = $0.036 per request
Round to: $0.04 per request
```

#### Credit System Design

```
Credits Included = (Target Price - Fixed Costs) / (Price per Credit × Margin)

Where:
- Target Price: What customer pays monthly
- Fixed Costs: Base platform costs
- Price per Credit: Cost of one credit unit
- Margin: Target gross margin
```

**Example: AI Writing Assistant**
- Target price: $49/month
- Fixed platform cost: $10/month
- Cost per credit: $0.01
- Target margin: 80%

```
Available for Credits = $49 - ($10 / 0.80)
Available for Credits = $49 - $12.50 = $36.50

Credits Included = $36.50 / ($0.01 / 0.80)
Credits Included = $36.50 / $0.0125
Credits Included = 2,920 credits

Round to: 3,000 credits/month
```

---

## Unit Economics

### Customer Acquisition Cost (CAC)

```
CAC = Total Sales & Marketing Costs / New Customers Acquired

Include:
- Marketing spend (ads, content, events)
- Sales team salaries & commissions
- Marketing tools & software
- Lead generation costs
```

**Example:**
- Monthly marketing spend: $50,000
- Sales team cost: $30,000
- New customers: 80

```
CAC = ($50,000 + $30,000) / 80
CAC = $80,000 / 80
CAC = $1,000 per customer
```

### CAC Payback Period

```
CAC Payback = CAC / (ARPA × Gross Margin)

Where ARPA = Average Revenue Per Account
```

**Example:**
- CAC: $1,000
- ARPA: $100/month
- Gross Margin: 80%

```
Contribution Margin = $100 × 0.80 = $80/month
Payback Period = $1,000 / $80 = 12.5 months
```

**Benchmark:** <12 months is excellent, <18 months is healthy

### Lifetime Value (LTV)

```
LTV = ARPA × Gross Margin × Customer Lifetime (months)

Customer Lifetime = 1 / Churn Rate
```

**Example:**
- ARPA: $100/month
- Gross Margin: 80%
- Monthly churn: 2%

```
Customer Lifetime = 1 / 0.02 = 50 months
LTV = $100 × 0.80 × 50 = $4,000
```

### LTV:CAC Ratio

```
LTV:CAC Ratio = LTV / CAC
```

**Example:**
- LTV: $4,000
- CAC: $1,000

```
LTV:CAC = $4,000 / $1,000 = 4:1
```

**Benchmarks:**
- 3:1 or higher: Healthy
- 5:1 or higher: Excellent
- Below 3:1: Need to improve retention or reduce CAC

---

## Pricing Psychology Formulas

### The Power of 9

```
Price with 9 = Round down to nearest .99

Example:
$100 → $99
$50 → $49
$20 → $19
```

**Impact:** Studies show ~2-3% increase in purchases vs rounded prices

### Anchor Effect Calculation

```
Perceived Savings = (Anchor Price - Actual Price) / Anchor Price

For maximum effect:
- Anchor price should be 2-3x actual price
- Show anchor price first
- Cross out anchor price visually
```

**Example:**
- Anchor price: $199
- Actual price: $99
- Perceived savings: ($199 - $99) / $199 = 50%

### Tier Pricing Optimization

```
Price Ratio = Higher Tier Price / Lower Tier Price

Optimal ratios:
- Adjacent tiers: 1.5x - 3x price difference
- Top tier to bottom tier: 5x - 10x difference
```

**Example Structure:**
```
Starter: $29
Pro: $79 (2.7x Starter)
Enterprise: $299 (3.8x Pro)

Total spread: 299 / 29 = 10.3x ✓
```

### Volume Discount Formula

```
Volume Price = Base Price × (1 - Discount Rate)

Common discount schedules:
- 10-20% off for annual payment
- 15-30% off for 100+ units
- 30-50% off for enterprise contracts
```

---

## A/B Testing Calculations

### Statistical Significance

```
Z-Score = (Conversion Rate A - Conversion Rate B) / √[(p(1-p)/nA) + (p(1-p)/nB)]

Where:
- p = Combined conversion rate
- nA, nB = Sample sizes
- Z-Score > 1.96 = 95% confidence
```

**Simplified Rule of Thumb:**
- Need at least 1,000 visitors per variant
- Run for minimum 2 full business cycles (14 days)
- Look for >10% difference in conversion rate

### Revenue Impact Calculation

```
Revenue Impact = Traffic × Conversion Rate × (ARPU_test - ARPU_control)
```

**Example:**
- Monthly traffic: 50,000 visitors
- Control conversion: 3% at $49 = 1,500 customers
- Test conversion: 3.3% at $59 = 1,650 customers

```
Control Revenue = 1,500 × $49 = $73,500
Test Revenue = 1,650 × $59 = $97,350
Monthly Increase = $97,350 - $73,500 = $23,850 (+32%)
```

### Minimum Detectable Effect (MDE)

```
MDE = (Z-score × √[p(1-p) × (2/n)])

Where:
- Z-score = 1.96 for 95% confidence
- p = baseline conversion rate
- n = sample size per variant
```

**Quick Reference:**

| Sample Size | Baseline CR | MDE |
|-------------|-------------|-----|
| 1,000 | 5% | ±2.1% |
| 1,000 | 10% | ±2.7% |
| 5,000 | 5% | ±0.9% |
| 5,000 | 10% | ±1.2% |

---

## Pricing Strategy ROI Calculator

### Scenario: Tier Restructure

**Current State:**
- 3 tiers at $29, $79, $199
- Conversion: 60% Starter, 30% Pro, 10% Enterprise
- Monthly new customers: 1,000
- ARPU: $58.70/month

**Proposed State:**
- New tiers at $39, $99, $249
- Expected conversion shift: 50%, 35%, 15%
- Same traffic: 1,000 customers
- ARPU: $91.40/month

**Revenue Impact:**
```
Current Monthly Revenue = 1,000 × $58.70 = $58,700
Proposed Monthly Revenue = 1,000 × $91.40 = $91,400
Monthly Increase = $32,700 (+55.7%)
Annual Impact = $392,400
```

**Churn Risk Adjustment:**
- If churn increases by 2% due to higher prices
- Net impact still positive if increase >15%

---

## Quick Reference Formulas

### Value-Based Pricing
```
Price = (Time Value + Revenue Value + Cost Savings) × 10-30%
```

### Margin-Based Pricing
```
Price = Cost / (1 - Target Margin)
```

### Break-Even Analysis
```
Break-Even Customers = Fixed Costs / (Price - Variable Costs)
```

### Maximum Willingness to Pay
```
Max Price = (Value Created × 30%) - Competitor Price Differential
```

### Optimal Price Testing
```
Test Price 1 = Current Price
Test Price 2 = Current Price × 1.2
Test Price 3 = Current Price × 1.5
```

---

## Common Mistakes in Calculations

❌ **Cost-Plus Pricing**
```
Wrong: Price = Cost + 20% markup
Right: Price = Value Created × 15-30%
```

❌ **Ignoring Margins**
```
Wrong: Price = $50 without checking costs
Right: Verify $50 maintains 75%+ margin
```

❌ **Averaging Wrongly**
```
Wrong: Average price = ($29 + $99) / 2 = $64
Right: Weighted average by conversion rate
```

❌ **Churn Impact on LTV**
```
Wrong: LTV = ARPA × 12 (for 1 year)
Right: LTV = ARPA × (1 / churn rate)
```

---

## Summary Checklist

Before finalizing any price:

✅ Calculate value created for customer
✅ Verify 70-80% gross margin
✅ Check LTV:CAC > 3:1
✅ Ensure CAC payback < 12 months
✅ Test pricing with A/B experiments
✅ Benchmark against competitors
✅ Leave room for annual discounts (10-20%)
✅ Create upgrade paths between tiers
✅ Protect against heavy users (usage limits or overages)
✅ Plan for enterprise negotiations (20-30% discounts)
