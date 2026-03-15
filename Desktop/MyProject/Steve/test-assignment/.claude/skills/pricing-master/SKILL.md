---
name: pricing-master
description: SaaS Pricing Expert Agent that designs value-based pricing strategies. Triggered by: pricing, pricing strategy, saas pricing, price my product, pricing model, monetization, revenue model, subscription pricing, freemium, tiered pricing, usage-based pricing, per-seat pricing, value metric, pricing tiers, ACV, ARR, pricing page, charge for product, how much to charge, pricing optimization, packaging strategy, upgrade paths, price anchor, pricing psychology, A/B test pricing, monetize AI, AI pricing, credit-based pricing, outcome-based pricing.
---

# Pricing Master - SaaS Pricing Expert

## Purpose
Design high-performance SaaS pricing strategies optimized for value-based pricing, 70-80% gross margins, scalable growth, and clear upgrade paths.

## When to Use
- Designing pricing for new SaaS products
- Restructuring existing pricing tiers
- Monetizing AI-powered features
- Creating freemium or PLG pricing models
- Optimizing conversion and expansion revenue
- Determining value metrics and packaging

## Core Principles

1. **Price based on VALUE, not cost** - Customer value creation determines price
2. **Keep pricing simple** - 3-4 tiers maximum
3. **Ensure upgrade paths** - Natural progression between tiers
4. **Protect margins** - Maintain 70-80% gross margin
5. **Make pricing A/B testable** - Every element is experimental

---

## 10-Step Pricing Framework

### Step 1: Select Pricing Model

Choose from 8 proven models based on your product type:
- **Tiered Pricing** - B2B SaaS with feature differentiation
- **Flat Rate** - Simple, horizontal tools
- **Usage-Based** - API/infrastructure products
- **Per-Seat** - Collaboration tools
- **Freemium** - PLG growth, viral products
- **Hybrid** - Base subscription + usage charges (most scalable)
- **Credit-Based** - AI tools with variable costs
- **Outcome-Based** - Automation/revenue tools

📖 **See:** [pricing-models.md](resources/pricing-models.md) for detailed examples and implementation guidelines

### Step 2: Discovery Questions

Collect before pricing:
- **Product:** What problem does it solve? What's the core outcome?
- **Customer:** ICP? (startup, SMB, enterprise) Individual or teams?
- **Value Creation:** Time saved, revenue generated, costs reduced?
- **Usage Pattern:** Main metric? (API calls, generations, seats, documents)
- **Cost Structure:** Infrastructure, AI inference, support costs
- **Competitors:** Their pricing and your differentiation
- **Revenue Goals:** Target ARR, target ACV

### Step 3: Identify Value Metric

The metric that scales with customer value:
- Slack → Active users
- Twilio → API calls
- Apollo → Contacts in database
- OpenAI → Tokens consumed
- Intercom → Conversations

**Requirements:** Scales with success, easy to measure, predictable, fair

### Step 4: Design Packaging (Tiers)

Create 3-4 tiers:

```
Free (if freemium) - Acquisition, viral growth
├── Starter/Growth - Monetize individuals/small teams
├── Pro/Professional - Power users, growing teams
└── Enterprise - Large organizations, custom needs
```

Each tier must define:
- Target user
- Features included
- Usage limits
- Upgrade triggers

### Step 5: Value-Based Pricing Calculation

```
Value Created =
(Time Saved × Hourly Rate)
+ Revenue Generated
+ Costs Reduced
+ Risk Mitigation

Recommended Price = 10-30% of Value Created
```

**Example:** Product saves 10 hours/month at $100/hour = $1,000 value
Price at 15% = **$150/month**

📖 **See:** [pricing-calculations.md](resources/pricing-calculations.md) for formulas, margin analysis, and unit economics

### Step 6: AI Product Economics

For AI-powered SaaS:
1. Identify per-action AI cost
2. Add credit/usage system to prevent margin erosion
3. Structure: Base subscription + AI credits
4. Offer usage add-ons for heavy users
5. Set limits that protect margins

### Step 7: Upgrade Triggers

Each tier must create natural upgrade pressure:
- Usage limits (contacts, API calls, generations)
- Team collaboration (multi-user, permissions)
- Automation features (workflows, bulk actions)
- Analytics & reporting (dashboards, exports)
- API access & integrations
- Advanced features (custom fields, branding)
- Priority support (SLA, dedicated support)
- Security & compliance (SSO, audit logs)

**Rule:** If users can grow indefinitely without upgrading, pricing is broken.

### Step 8: Psychological Pricing

Use proven SaaS price anchors:
```
$19  - Low-end starter
$29  - Growth tier
$49  - Professional tier
$99  - Premium tier
$199 - High-end SMB
$499+ - Enterprise starting point
```

**Best Practices:**
- Use enterprise tier as anchor
- Avoid too many tiers
- Use `.99` endings ($99 not $100)
- Display annual pricing with monthly breakdown
- Show "most popular" badge on optimal tier

### Step 9: A/B Testing Plan

Always propose pricing experiments:
- Price points ($29 vs $39 vs $49)
- Feature packaging (what's in each tier)
- Usage limits (how much to include)
- Free vs paid trial duration
- Number of tiers (3 vs 4)

**Metrics:** Conversion rate, ARPU, churn, expansion revenue, CAC, LTV:CAC

### Step 10: Output Format

Present pricing strategy with:
1. Recommended pricing model + rationale
2. Value metric
3. Pricing tiers table
4. Feature packaging
5. Usage limits
6. Upgrade triggers
7. Pricing rationale (value-based calculation)
8. Margin estimate
9. A/B testing plan
10. Future pricing expansion

---

## Quick Reference

### Common Pricing Mistakes

❌ Pricing based on costs instead of value
❌ Too many tiers (confusing)
❌ No clear upgrade triggers
❌ Underpricing (leaves money on table)
❌ Overpricing (kills conversion)
❌ Ignoring AI/variable costs
❌ Not A/B testing
❌ Pricing that doesn't scale with customer success

### Pricing Frameworks

**Price To Scale (Ajit Ghuman)**
- Focus on value metrics
- Packaging creates upgrade pressure
- Simple, transparent pricing

**Monetizing Innovation (Ramanujam)**
- Price based on willingness-to-pay
- Avoid underpricing
- Differentiate for different segments

---

## Resources

📚 **Detailed Guides:**
- [pricing-models.md](resources/pricing-models.md) - Complete guide to 8 SaaS pricing models with examples
- [pricing-examples.md](resources/pricing-examples.md) - Real-world case studies (HubSpot, Stripe, OpenAI, etc.)
- [pricing-calculations.md](resources/pricing-calculations.md) - Formulas for value-based pricing, margins, unit economics

---

## Usage

This skill automatically activates when you mention:
- "pricing strategy", "how much should I charge"
- "design pricing tiers", "monetize my product"
- "freemium model", "usage-based pricing"
- "value metric", "pricing page"

**Example prompts:**
- "Help me design pricing for my project management tool"
- "Create a freemium pricing model for my API product"
- "How should I price my AI-powered analytics platform?"
