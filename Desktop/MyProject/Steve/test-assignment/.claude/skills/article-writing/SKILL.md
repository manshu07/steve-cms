---
name: article-writing
description: Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph, especially when voice consistency, structure, and credibility matter.
origin: ECC
---

# Article Writing Skill

Write long-form content that sounds like a real person or brand, not generic AI output.

## Purpose
Transform rough ideas, notes, research, or transcripts into polished articles, guides, blog posts, tutorials, and newsletters with authentic voice and concrete credibility.

## When to Use This Skill

**Auto-activates when:**
- Drafting blog posts, essays, launch posts, guides, tutorials, or newsletter issues
- Turning notes, transcripts, or research into polished articles
- Matching an existing founder, operator, or brand voice from examples
- Tightening structure, pacing, and evidence in already-written long-form copy
- Writing long-form content (more than a paragraph)

**Keywords that trigger:**
- blog post, article, guide, tutorial, newsletter, essay, write, writing, content, draft, publish
- voice, tone, style, brand voice
- long-form, content marketing

---

## Core Rules (The Anti-Generic-AI Checklist)

### ✅ DO These Things

1. **Lead with the concrete thing** - Example, output, anecdote, number, screenshot description, or code block
2. **Explain after the example, not before** - Show, then tell
3. **Prefer short, direct sentences** over padded ones
4. **Use specific numbers** when available and sourced
5. **One idea per paragraph** - Keep it focused

### ❌ NEVER Do These Things

1. **Generic openings** - "In today's rapidly evolving landscape"
2. **Filler transitions** - "Moreover", "Furthermore", "Additionally"
3. **Hype phrases** - "game-changer", "cutting-edge", "revolutionary", "groundbreaking"
4. **Vague claims** without evidence
5. **Invented facts** - Never make up biographical details, company metrics, or customer quotes
6. **Corporate speak** - "leverage", "synergy", "paradigm shift", "thought leadership"

---

## Default Voice: Operator-Style

When no voice references are provided, use this voice:

**Characteristics:**
- Concrete and practical
- Low on hype
- Direct sentences
- Specific examples
- Numbers over adjectives
- Industry jargon is okay if explained

**Example:**
```
❌ BAD: "In today's competitive landscape, leveraging cutting-edge
AI solutions can be a game-changer for forward-thinking companies."

✅ GOOD: "We cut our customer support tickets by 40% with a simple
AI triage bot. Here's how we built it."
```

---

## Voice Capture Workflow

When the user wants a specific voice, collect and analyze:

### What to Collect
- Published articles
- Newsletters
- X / LinkedIn posts
- Docs or memos
- Short style guide
- Product descriptions
- Launch announcements

### What to Extract

**1. Sentence Length and Rhythm**
```
Short punchy? "Sales are up. Way up."
Long flowing? "When we consider the cumulative impact of..."
Mixed? Varies for effect (like this example shows)
```

**2. Formality Level**
- Formal: "One must consider..."
- Conversational: "You gotta think about..."
- Sharp/Blunt: "This is wrong. Here's why."

**3. Rhetorical Devices**
- Parentheses (for asides)
- Em-dashes — for emphasis
- Fragment sentences. Like this.
- Questions? Rhetorical ones?
- Lists (like you're reading now)

**4. Formatting Habits**
- Headers: ## vs ### vs bold
- Bullets: • vs - vs *
- Code blocks: when and how
- Pull quotes: how they're marked
- Links: inline vs footnotes

**5. Personality Markers**
- Humor: Punny? Dry? None?
- Opinion: Strong takes? Measured?
- Contrarian: Loves to disagree?
- Self-deprecation: Okay to be wrong?

---

## Writing Process

### Step 1: Clarify Audience and Purpose

Ask yourself:
- Who is reading? (Developers? Founders? General audience?)
- What do they want? (Learn? Be entertained? Make a decision?)
- What's the win? (What do they get by reading this?)

### Step 2: Build Skeleton Outline

One purpose per section:
```
## Title (the promise)
## The Hook (why this matters)
## Example 1 (concrete proof)
## How It Works (the meat)
## Example 2 (another proof)
## What You Should Do (actionable)
## Resources (if applicable)
```

### Step 3: Write Each Section

**Start with evidence, example, or scene:**
```
✅ GOOD: "By month 3, we had lost 40% of our trial users. The data
showed they all dropped off at the same point: the onboarding video."

❌ BAD: "Before we dive into the solution, it's important to understand
the problem that many SaaS companies face when it comes to user
retention and onboarding strategies."
```

### Step 4: Expand Only Where Earned

Every sentence must earn its place. Ask:
- Does this add new info?
- Is it concrete?
- Would the reader miss it if deleted?

If no → cut it.

### Step 5: Remove Templated Language

Delete anything that sounds like:
- "In this article, we'll explore..."
- "It's important to note that..."
- "It goes without saying..."
- "Key takeaways include..."

Replace with direct statements:
- "Here's the fix."
- "This matters because..."
- "The data shows..."

---

## Structure Guidance by Content Type

### Technical Guides

**Goal:** Reader learns how to do something

**Structure:**
```
## Title (Verb + What + Benefit)
## What You'll Get (the promise)
## The Problem (why this isn't obvious)
## Solution with Code (concrete steps)
## Example Output (proof it works)
## Common Mistakes (what to avoid)
## Quick Reference (cheat sheet)
```

**Example:**
```markdown
## How to Build a JWT Auth System in 15 Minutes

**What you'll get:** A working authentication system with refresh
tokens, cookie security, and role-based access control.

**The hard part:** JWTs are simple. Security isn't. Most tutorials
skip the stuff that actually gets you hacked.

**The fix:**

\`\`\`typescript
// Generate tokens with short expiry
const accessToken = jwt.sign({ userId }, SECRET, {
    expiresIn: '15m'  // Short-lived
});

const refreshToken = jwt.sign({ userId }, REFRESH_SECRET, {
    expiresIn: '7d'  // Longer-lived, separate secret
});
\`\`\`

**Why this works:** If an access token leaks (and it will), it's
useless in 15 minutes. The refresh token can only be used from
your domain, thanks to httpOnly cookies.
```

---

### Essays / Opinion Pieces

**Goal:** Persuade reader of a viewpoint

**Structure:**
```
## Title (Clear stance)
## The Hook (tension or contradiction)
## Evidence 1 (data, story, or example)
## Evidence 2 (different angle)
## Counterargument (and why it's wrong)
## The Point (why this matters)
## What to Do (if applicable)
```

**Example:**
```markdown
## Most SaaS Companies Die From Success, Not Failure

**The trap:** You land a big customer. You build custom features for
them. Your team is stretched thin but ARR is up.

Then they churn. And you're stuck maintaining custom features nobody
else wants.

**The data:** Of the 127 YC SaaS companies we studied, 43% that hit
$1M ARR still failed. The #1 cause? Feature bloat from "strategic"
customers.

**The math:**
- Custom feature takes 2 weeks to build
- One customer wants it, pays $50k/year
- Maintenance cost = $30k/year forever
- You need 3 more customers just to break even

**Better approach:** Say no to custom features. Build for the market,
not the customer. If one company needs it, others probably do too.
```

---

### Newsletters

**Goal:** Keep readers subscribed and informed

**Structure:**
```
## Above the Fold (strong, skimmable)
## One Big Insight (the main value)
## Quick Updates (bullet points)
## One Cool Thing (interesting find)
## Ask or Call to Action
```

**Example:**
```markdown
**WEEKLY #47**

We cut AWS costs by 60% last week. Not by negotiating—by counting.

### The Expensive Mistake

Our dev team spun up 47 EC2 instances for a batch job. Left them
running. For 3 months.

Cost: $12,400.

The fix? A simple cron job:
\`\`\`bash
# Run at 6pm, kill orphaned instances
*/5 18 * * * aws ec2 terminate-instances --filters ...
\`\`\`

**This week:**
- 🚀 Launched the new dashboard (finally)
- 🐛 Fixed the login timeout bug
- 📊 Released our open-source Redis client

**One cool thing:** [link]

Just shipped something cool? Hit reply—I'd love to see it.
```

---

### Launch Posts

**Goal:** Announce something and get people to care

**Structure:**
```
## The Hook (what changed)
## Before (the problem)
## After (the solution)
## How It Works (details)
## Early Access / Get Started
```

**Example:**
```markdown
## We Made Passwords Optional. Here's Why.

**The problem:** Passwords are terrible. People reuse them. Forget
them. Hate creating them.

**The data:** 34% of our signups dropped off at the password step.
We were losing thousands of users because of a security "best
practice."

**The solution:** Magic links + passkeys. Click a button, you're in.
No password. No reset flow.

**How it works:**
1. Enter email
2. Click link in email (magic link)
3. Or use Face ID / Touch ID (passkey)
4. Done

**Try it:** [link to signup]

The best part? Support tickets for "I forgot my password" dropped
to zero. Not one. Zero.
```

---

## Quality Gate

Before delivering any article, verify:

### Factual Claims
- [ ] Every statistic is sourced or provided by user
- [ ] No invented metrics, revenue numbers, or growth figures
- [ ] No fake customer quotes or testimonials
- [ ] No made-up biographical details

### Voice Consistency
- [ ] Sentence length matches examples
- [ ] Formality level matches examples
- [ ] Rhetorical devices match examples
- [ ] Formatting matches examples

### Anti-Generic Check
- [ ] No "In today's world" openings
- [ ] No "Moreover", "Furthermore", "Additionally"
- [ ] No "game-changer", "cutting-edge", "revolutionary"
- [ ] No corporate buzzwords
- [ ] No templated transitions

### Structure Check
- [ ] Every section adds new information
- [ ] Each paragraph has one clear idea
- [ ] Examples precede explanations
- [ ] Concrete specifics over vague abstractions
- [ ] No wasted words or filler

### Read-Aloud Test
- [ ] Read the full article aloud
- [ ] Does it sound human or robotic?
- [ ] Does it flow or stumble?
- [ ] Would you share this with friends?

---

## Quick Reference: Common Fixes

| Generic AI Output | Fix With This |
|------------------|---------------|
| "In today's rapidly evolving landscape..." | Delete. Start with the thing. |
| "Moreover, Furthermore, Additionally" | Delete or make a new section. |
| "cutting-edge, revolutionary, game-changer" | Use specific numbers or examples. |
| "It's important to note that..." | Say the thing directly. |
| "Leverage our innovative solution..." | "We use X to do Y." |
| "Key takeaways include..." | Delete or use "One more thing:" |
| "In conclusion, therefore, thus" | Delete or make final point. |

---

## Examples Gallery

### Paul Graham Style
```
Short sentences. Conversational but sharp. Contrarian opinions.
Concrete examples. No padding.

Example: "Most startups fail. Not because the idea is bad, but
because they give up. The ones that succeed are the ones who
don't stop."
```

### Stripe Blog Style
```
Technical depth. Clear headers. Code examples. Screenshots.
Very practical. Developer-focused.

Example: "Implementing webhooks is hard. Let's walk through how
we handle idempotency, retry logic, and signature verification."
```

### HN/Show HN Style
```
Direct. Technical. Show the code early. Explain the tradeoffs.
Community-focused.

Example: "Built a real-time collab editor in 300 lines. CRDTs
are overrated for most use cases. Here's what I learned."
```

### Newsletter Style (General)
```
Personal voice. Quick hits. One deep dive per issue. Ask for
replies.

Example: "This week I learned that most people don't read the
docs. They just copy-paste from StackOverflow. So we made the
docs copy-paste friendly. Conversion tripled."
```

---

## Related Skills

- **pm-guidelines** - Product narrative and positioning
- **documentation-architect** - Technical docs and API references
- **cto-guidelines** - Technical blog posts and architecture essays

---

## Origin

This skill is based on the "Article Writing" skill from ECC (Exa
Computer Corp), adapted for Claude Code's extensibility system.
