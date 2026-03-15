# Article Examples Collection

Real-world examples of different article types and voices to use as reference when capturing voice and writing long-form content.

---

## Table of Contents

- [Operator/Founder Voice](#operatorfounder-voice)
- [Technical Deep Dive](#technical-deep-dive)
- [Newsletter Style](#newsletter-style)
- [Launch Announcement](#launch-announcement)
- [Opinion Essay](#opinion-essay)
- [How-To Guide](#how-to-guide)

---

## Operator/Founder Voice

**Characteristics:** Short sentences. Direct. Numbers over adjectives. Anti-hype.

### Example 1: HN Comment Style

```
We hit $10k MRR last month. Here's what worked:

1. Cold emailed 500 founders. Got 12 replies. 2 converted.
2. Wrote one blog post per week. The one about "pricing mistakes"
   still brings in 2-3 leads/week.
3. Killed the free tier. Conversion went up, not down.

The counterintuitive part: People who pay, pay attention.

We're now at $23k MRR. 80% from inbound.

Happy to answer questions about pricing or cold outreach.
```

### Example 2: Twitter/X Thread Style

```
Bad advice I followed for 2 years:

"Build an audience first, then launch"

Reality: nobody cares until you ship something useful.

Better approach:
1. Build something
2. Get 10 users
3. Talk to them
4. Make it better
5. Repeat

The audience comes after the product, not before.

This took me 2 years and $40k to learn. Save yourself the time.
```

---

## Technical Deep Dive

**Characteristics:** Code-heavy. Screenshots. Step-by-step. Technical depth.

### Example: Stripe Blog Style

```
# Building Webhooks That Don't Fail

Webhooks seem simple. POST a request, done. But in production:
- Networks fail
- Servers restart
- Events arrive out of order
- Retries create duplicates

Here's how we handle all of that.

## The Problem

You receive a webhook. Your server processes it. Then crashes.
The webhook sender retries. Now you've processed the same event twice.

## The Solution

### 1. Idempotency Keys

Every webhook gets a unique ID. Store it.

```typescript
async function handleWebhook(event: WebhookEvent) {
    // Check if already processed
    const existing = await db.webhooks.findUnique({
        where: { id: event.id }
    });

    if (existing) {
        return { status: 'already_processed' };
    }

    // Process the event
    await processEvent(event);

    // Store the ID
    await db.webhooks.create({
        data: { id: event.id, processedAt: new Date() }
    });
}
```

### 2. Exactly-Once Processing

Wrap everything in a transaction:

```typescript
await db.$transaction(async (tx) => {
    // 1. Mark as processing
    // 2. Process event
    // 3. Mark as complete
});
```

If anything fails, the transaction rolls back. The webhook sender
can retry safely.

## The Results

Since implementing this:
- Dropped from 0.3% duplicate processing to <0.001%
- Can safely retry any webhook
- Audit trail for every event

Full implementation: [github.com/your-repo/webhooks]
```

---

## Newsletter Style

**Characteristics:** Personal. One deep dive per issue. Quick hits. Ask for replies.

### Example: Product Hunt Newsletter Style

```
PRODUCT DAILY #47

**The 3-click rule that increased conversions by 40%**

Our signup form had 7 fields. Email, password, confirm password,
company, role, team size, use case.

Most people dropped off at step 3.

**The fix:**

1. Email only (we'll send a magic link)
2. Set password later (on first login)
3. Ask the rest after they're hooked

**Result:** Signup completion went from 34% to 62%.

The insight: Friction kills. Ask for commitment after they've
seen value, not before.

---

**Quick hits:**

🚀 Launched the new dashboard (finally)
🐛 Fixed the export bug that everyone hated
📊 Added 3 new templates

**One cool thing:** [link to competitor's feature we like]

Working on something cool? Hit reply—I'd love to see it.
```

---

## Launch Announcement

**Characteristics:** Clear value proposition. Before/after. Specific benefit. Call to action.

### Example: Product Launch Style

```
# Introducing: NovaSales AI

We built the sales agent we wished we had.

**The problem:**

Sales teams spend 4 hours/day on:
- Qualifying leads (manual research)
- Writing emails (copy-paste templates)
- Following up (spreadsheets and reminders)
- Updating CRM (data entry nobody likes)

**The solution:**

NovaSales AI automates the whole thing:
1. Researches prospects (LinkedIn, company site, news)
2. Writes personalized emails (actually personalized, not templates)
3. Sends at optimal times (AI learns when they open emails)
4. Updates your CRM automatically
5. Handles replies and schedules meetings

**The results:**

Early users are seeing:
- 3.2x more meetings booked
- 67% less time on prospecting
- 28% reply rate (vs 8% industry average)

**Try it free:** [novasales.ai]

No credit card required. 14-day trial. Cancel anytime.

---

**One more thing:**

We built this because we lived it. Our founders did 500+ cold calls
and sent 10,000+ emails. NovaSales AI is what we wished we had.

Now you don't have to suffer through what we did.
```

---

## Opinion Essay

**Characteristics:** Clear stance. Evidence-based. One argument per section. Contrarian if possible.

### Example: Paul Graham Style

```
# Most Startup Advice Is Wrong

Here's the pattern:

1. Successful founder gives interview
2. Attributes success to specific thing
3. Others copy that thing
4. They fail because it wasn't the real reason

**The problem:**

Founders are bad at knowing why they succeeded.

Airbnb thinks it was "design-first culture." Actually it was timing
(2008 recession) and relentless door-to-door selling.

Stripe thinks it was "developer-first." Actually it was starting
when payments were a nightmare and incumbents were asleep.

**The truth:**

Success is usually:
1. Right market (timing + demand)
2. Good enough product
3. Relentless execution
4. Luck

Everything else is noise.

**What to do instead:**

Ignore advice about:
- "Must-have" features
- "Proven" strategies
- "Best" practices

Focus on:
- Talking to users
- Building what they actually want
- Shipping fast
- Staying alive long enough to get lucky

**The uncomfortable truth:**

Most success is survival + luck. The rest is just storytelling
after the fact.

If you're lucky enough to succeed, you'll make up a reason too.
```

---

## How-To Guide

**Characteristics:** Actionable steps. Code examples. Common mistakes. Quick reference.

### Example: Tutorial Style

```
# How to Add JWT Auth to Your API in 15 Minutes

**What you'll get:**
- JWT access tokens (15min expiry)
- Refresh tokens (7 day expiry)
- Secure cookie storage
- Role-based access control

**Before we start:**

This guide uses Node.js + Express. If you're using something else,
the concepts are the same but code will differ.

## Step 1: Install Dependencies

```bash
npm install jsonwebtoken cookie-parser
npm install --save-dev @types/jsonwebtoken @types/cookie-parser
```

## Step 2: Generate Tokens

```typescript
import jwt from 'jsonwebtoken';

const ACCESS_SECRET = process.env.JWT_ACCESS_SECRET;
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;

function generateTokens(userId: string) {
    const accessToken = jwt.sign({ userId }, ACCESS_SECRET, {
        expiresIn: '15m'
    });

    const refreshToken = jwt.sign({ userId }, REFRESH_SECRET, {
        expiresIn: '7d'
    });

    return { accessToken, refreshToken };
}
```

**Why two secrets?**
If the access token leaks (it will), it's useless in 15 minutes.
The refresh token lives longer but only works from your domain.

## Step 3: Set Cookies

```typescript
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const user = authenticateUser(email, password);

    const tokens = generateTokens(user.id);

    // Access token in memory (httpOnly not needed)
    res.cookie('accessToken', tokens.accessToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 15 * 60 * 1000 // 15 minutes
    });

    // Refresh token for long-term sessions
    res.cookie('refreshToken', tokens.refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
    });

    res.json({ user });
});
```

## Common Mistakes

**❌ Storing tokens in localStorage**
→ XSS can steal them

**❌ Long-lived access tokens**
→ If stolen, attacker has days/weeks of access

**❌ Same secret for access + refresh**
 defeating the purpose

**❌ Not rotating refresh tokens**
→ One stolen token = forever access

## Quick Reference

| Token | Expiry | Storage | Secret |
|-------|--------|---------|--------|
| Access | 15min | Cookie (httpOnly) | SECRET_A |
| Refresh | 7 days | Cookie (httpOnly) | SECRET_B |

**What's next?**
- Add role-based access control
- Implement token rotation
- Add rate limiting on auth endpoints
```

---

## Voice Capture Examples

### Extracting Voice Patterns

**Paul Graham Analysis:**
```
Sentence length: Short (3-10 words)
Tone: Conversational but authoritative
Rhetorical devices: Fragments. Questions. Contrarian takes.
Formatting: Short paragraphs. Sometimes one sentence.
Humor: Dry, understated
Opinion: Strong, unapologetic

Key markers:
- "Here's the thing"
- "The problem is"
- "What most people don't get"
```

**Stripe Blog Analysis:**
```
Sentence length: Medium (10-20 words)
Tone: Professional but approachable
Rhetorical devices: Code examples, before/after comparisons
Formatting: Clear headers, code blocks, bullet lists
Humor: None. Very serious.
Opinion: Measured, evidence-backed

Key markers:
- "Here's how we handle X"
- "The problem"
- "The solution"
- "The results"
```

**Newsletter Analysis (Product Hunt):**
```
Sentence length: Mixed. Short for impact, longer for explanation.
Tone: Enthusiastic, personal
Rhetorical devices: Emojis, quick hits, one cool thing
Formatting: Sections with emoji headers
Humor: Light, occasional
Opinion: Opinionated but friendly

Key markers:
- "Quick hits:"
- "One cool thing:"
- "Working on something cool?"
```

---

## Banned Phrase Transformations

| Generic | Fix With This |
|---------|---------------|
| "In today's rapidly evolving landscape..." | DELETE. Start with the thing. |
| "Moreover, Furthermore, Additionally" | DELETE. Start a new section. |
| "cutting-edge, revolutionary, game-changer" | Use numbers: "3x faster", "40% increase" |
| "It's important to note that..." | Say it directly. |
| "Leverage our innovative solution..." | "We use X to do Y." |
| "Key takeaways include..." | "One more thing:" or DELETE |
| "In conclusion, therefore, thus" | Make final point or DELETE |
| "synergy, paradigm shift, thought leadership" | DELETE ALL |

---

## Voice Matching Checklist

When capturing a voice, identify:

**Structure:**
- [ ] Sentence length (short/medium/mixed)
- [ ] Paragraph length (one-liners/multi-sentence)
- [ ] Header usage (### vs bold vs none)

**Personality:**
- [ ] Formality (0-10 scale)
- [ ] Humor (none/dry/punny/frequent)
- [ ] Opinion level (measured/strong/contrarian)
- [ ] Self-reference (I/we, third person, none)

**Rhetorical devices:**
- [ ] Parentheses (for asides)
- [ ] Em dashes — for emphasis
- [ ] Fragment sentences.
- [ ] Questions? Even rhetorical?
- [ ] Lists (bullets, numbers)

**Formatting:**
- [ ] Code blocks (how often, when)
- [ ] Links (inline, footnotes, none)
- [ ] Emojis (yes/no, how many)
- [ ] Pull quotes (yes/no, how marked)

---

## Testing Voice Match

**Before writing full article, test with 3 paragraphs:**

1. **Opening paragraph** - Does it sound like them?
2. **Technical paragraph** - Does it match their depth?
3. **Closing paragraph** - Does it have their sign-off?

**If all three pass, proceed. If not, adjust and retry.**
