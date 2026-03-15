# TDD Workflow Patterns and Examples

## Real-World TDD Examples

### Example 1: Building a Semantic Search Feature

#### Step 1: User Journey
```
As a user, I want to search for markets using natural language,
so that I can find relevant markets even without exact keywords.

Acceptance Criteria:
- Returns markets ranked by semantic similarity
- Handles typos and related concepts
- Falls back to substring search if Redis is unavailable
- Returns empty array for empty queries
```

#### Step 2: Write Tests First

**File: `apps/api/src/__tests__/search.test.ts`**

```typescript
import { searchMarkets } from '../search'
import { searchMarketsByVector } from '@/lib/redis'
import { supabase } from '@/lib/supabase'

// Mock external dependencies
jest.mock('@/lib/redis')
jest.mock('@/lib/supabase')

describe('searchMarkets', () => {
  const mockMarkets = [
    { slug: 'us-election-2024', name: 'US Presidential Election 2024' },
    { slug: 'midterm-elections', name: 'Midterm Elections' },
    { slug: 'bitcoin-price', name: 'Bitcoin Price' }
  ]

  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('when Redis is available', () => {
    it('returns markets ranked by similarity score', async () => {
      // Arrange
      const query = 'president'
      ;(searchMarketsByVector as jest.Mock).mockResolvedValue([
        { slug: 'us-election-2024', similarity_score: 0.95 },
        { slug: 'midterm-elections', similarity_score: 0.82 }
      ])
      ;(supabase.from).mockReturnValue({
        select: jest.fn().mockReturnValue({
          in: jest.fn().mockResolvedValue({
            data: mockMarkets,
            error: null
          })
        })
      } as any)

      // Act
      const results = await searchMarkets(query)

      // Assert
      expect(results).toHaveLength(2)
      expect(results[0].slug).toBe('us-election-2024')
      expect(results[0].similarity).toBeCloseTo(0.95)
      expect(searchMarketsByVector).toHaveBeenCalledWith(query)
    })

    it('returns empty array for empty query', async () => {
      const results = await searchMarkets('')
      expect(results).toEqual([])
      expect(searchMarketsByVector).not.toHaveBeenCalled()
    })

    it('handles null query gracefully', async () => {
      const results = await searchMarkets(null as any)
      expect(results).toEqual([])
    })
  })

  describe('when Redis is unavailable', () => {
    it('falls back to substring search', async () => {
      const query = 'election'
      ;(searchMarketsByVector as jest.Mock).mockRejectedValue(
        new Error('Redis connection failed')
      )
      ;(supabase.from).mockReturnValue({
        select: jest.fn().mockReturnValue({
          ilike: jest.fn().mockResolvedValue({
            data: [
              mockMarkets[0],
              mockMarkets[1]
            ],
            error: null
          })
        })
      } as any)

      const results = await searchMarkets(query)

      expect(results).toHaveLength(2)
      expect(results[0].slug).toBe('us-election-2024')
      expect(results[1].slug).toBe('midterm-elections')
    })

    it('returns empty array when fallback also fails', async () => {
      ;(searchMarketsByVector as jest.Mock).mockRejectedValue(
        new Error('Redis failed')
      )
      ;(supabase.from).mockReturnValue({
        select: jest.fn().mockReturnValue({
          ilike: jest.fn().mockRejectedValue(new Error('DB failed'))
        })
      } as any)

      const results = await searchMarkets('test')

      expect(results).toEqual([])
    })
  })

  describe('edge cases', () => {
    it('handles special characters in query', async () => {
      const query = 'test & query!'
      ;(searchMarketsByVector as jest.Mock).mockResolvedValue([])
      ;(supabase.from).mockReturnValue({
        select: jest.fn().mockReturnValue({
          ilike: jest.fn().mockResolvedValue({
            data: [],
            error: null
          })
        })
      } as any)

      await expect(searchMarkets(query)).resolves.toEqual([])
    })

    it('handles very long queries', async () => {
      const longQuery = 'a'.repeat(1000)
      ;(searchMarketsByVector as jest.Mock).mockResolvedValue([])
      ;(supabase.from).mockReturnValue({
        select: jest.fn().mockReturnValue({
          ilike: jest.fn().mockResolvedValue({
            data: [],
            error: null
          })
        })
      } as any)

      await expect(searchMarkets(longQuery)).resolves.toEqual([])
    })

    it('handles unicode characters', async () => {
      const query = '选举' // Chinese for 'election'
      ;(searchMarketsByVector as jest.Mock).mockResolvedValue([])
      ;(supabase.from).mockReturnValue({
        select: jest.fn().mockReturnValue({
          ilike: jest.fn().mockResolvedValue({
            data: [],
            error: null
          })
        })
      } as any)

      await expect(searchMarkets(query)).resolves.toEqual([])
    })
  })
})
```

#### Step 3: Run Tests (Should Fail)
```bash
npm test search.test.ts
# FAIL: searchMarkets is not defined
```

#### Step 4: Implement Code

**File: `apps/api/src/search.ts`**

```typescript
import { searchMarketsByVector } from '@/lib/redis'
import { supabase } from '@/lib/supabase'

export interface SearchResult {
  slug: string
  name: string
  similarity?: number
}

export async function searchMarkets(query: string): Promise<SearchResult[]> {
  // Guard clause for empty/null queries
  if (!query || query.trim().length === 0) {
    return []
  }

  try {
    // Try semantic search via Redis
    const results = await searchMarketsByVector(query)

    if (results.length > 0) {
      // Fetch full market details
      const slugs = results.map(r => r.slug)
      const { data } = await supabase
        .from('markets')
        .select('slug, name')
        .in('slug', slugs)

      if (data) {
        // Merge results with similarity scores
        return data.map(market => ({
          slug: market.slug,
          name: market.name,
          similarity: results.find(r => r.slug === market.slug)?.similarity_score
        }))
      }
    }

    return []
  } catch (redisError) {
    // Fallback to substring search if Redis fails
    try {
      const { data } = await supabase
        .from('markets')
        .select('slug, name')
        .ilike('name', `%${query}%`)

      return data || []
    } catch (dbError) {
      // Both Redis and DB failed
      console.error('Search failed:', { redisError, dbError })
      return []
    }
  }
}
```

#### Step 5: Run Tests Again
```bash
npm test search.test.ts
# PASS: All tests green
```

#### Step 6: Verify Coverage
```bash
npm run test:coverage -- search.test.ts
# Coverage: 95% (all branches covered)
```

---

### Example 2: Building a React Component with TDD

#### Step 1: User Journey
```
As a user, I want to see market cards with status indicators,
so that I can quickly identify which markets are open/closed.

Acceptance Criteria:
- Shows market name and description
- Shows status badge (Active/Closed)
- Shows end date
- Clickable card navigates to market page
- Shows loading skeleton while loading
```

#### Step 2: Write Tests First

**File: `apps/web/components/MarketCard/MarketCard.test.tsx`**

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { MarketCard } from './MarketCard'

describe('MarketCard', () => {
  const mockMarket = {
    slug: 'test-market',
    name: 'Test Market',
    description: 'A test market for TDD',
    status: 'active',
    end_date: '2025-12-31'
  }

  it('renders market name and description', () => {
    render(<MarketCard market={mockMarket} />)

    expect(screen.getByText('Test Market')).toBeInTheDocument()
    expect(screen.getByText('A test market for TDD')).toBeInTheDocument()
  })

  it('shows active status badge', () => {
    render(<MarketCard market={mockMarket} />)

    const badge = screen.getByText('Active')
    expect(badge).toBeInTheDocument()
    expect(badge).toHaveClass('bg-green-100')
  })

  it('shows closed status badge', () => {
    const closedMarket = { ...mockMarket, status: 'closed' }
    render(<MarketCard market={closedMarket} />)

    const badge = screen.getByText('Closed')
    expect(badge).toBeInTheDocument()
    expect(badge).toHaveClass('bg-gray-100')
  })

  it('shows formatted end date', () => {
    render(<MarketCard market={mockMarket} />)

    expect(screen.getByText(/Dec 31, 2025/)).toBeInTheDocument()
  })

  it('navigates to market page when clicked', () => {
    const mockPush = jest.fn()
    jest.mock('next/navigation', () => ({
      useRouter: () => ({ push: mockPush })
    }))

    render(<MarketCard market={mockMarket} />)

    const card = screen.getByTestId('market-card')
    fireEvent.click(card)

    expect(mockPush).toHaveBeenCalledWith('/markets/test-market')
  })

  it('shows loading skeleton when loading', () => {
    render(<MarketCard market={null} loading />)

    expect(screen.getByTestId('skeleton')).toBeInTheDocument()
  })

  it('handles missing description gracefully', () => {
    const marketWithoutDesc = { ...mockMarket, description: null }
    render(<MarketCard market={marketWithoutDesc} />)

    // Should not crash, just not show description
    expect(screen.getByText('Test Market')).toBeInTheDocument()
  })

  it('truncates long descriptions', () => {
    const longDescMarket = {
      ...mockMarket,
      description: 'A'.repeat(200) // Very long description
    }
    render(<MarketCard market={longDescMarket} />)

    const description = screen.getByText((content) => {
      return content && content.length < 150
    })
    expect(description).toBeInTheDocument()
  })
})
```

#### Step 3: Implement Component

**File: `apps/web/components/MarketCard/MarketCard.tsx`**

```typescript
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface Market {
  slug: string
  name: string
  description: string | null
  status: 'active' | 'closed'
  end_date: string
}

interface MarketCardProps {
  market: Market | null
  loading?: boolean
}

export function MarketCard({ market, loading }: MarketCardProps) {
  const router = useRouter()

  if (loading || !market) {
    return (
      <div data-testid="skeleton" className="animate-pulse bg-gray-200 h-48 rounded-lg" />
    )
  }

  const truncatedDescription = market.description
    ? market.description.slice(0, 150) + (market.description.length > 150 ? '...' : '')
    : 'No description available'

  const statusColor = market.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'

  const endDate = new Date(market.end_date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })

  return (
    <Link
      href={`/markets/${market.slug}`}
      data-testid="market-card"
      className="block p-6 border rounded-lg hover:shadow-lg transition-shadow cursor-pointer"
      onClick={(e) => {
        e.preventDefault()
        router.push(`/markets/${market.slug}`)
      }}
    >
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold">{market.name}</h3>
        <span className={`px-2 py-1 text-xs font-medium rounded ${statusColor}`}>
          {market.status === 'active' ? 'Active' : 'Closed'}
        </span>
      </div>

      <p className="text-gray-600 text-sm mb-4 line-clamp-3">
        {truncatedDescription}
      </p>

      <div className="text-xs text-gray-500">
        Ends: {endDate}
      </div>
    </Link>
  )
}
```

#### Step 4: Run Tests
```bash
npm test MarketCard.test.tsx
# PASS: All tests green
```

---

### Example 3: API Route with Full Test Coverage

#### Step 1: User Journey
```
As a user, I want to create a new market,
so that I can start a prediction market.

Acceptance Criteria:
- Validates required fields (name, description, end_date)
- Returns created market on success
- Returns 400 for validation errors
- Returns 401 for unauthenticated users
- Returns 500 for database errors
```

#### Step 2: Write Tests First

**File: `apps/web/app/api/markets/route.test.ts`**

```typescript
import { POST } from './route'
import { NextRequest } from 'next/server'
import { supabase } from '@/lib/supabase'
import { getSession } from '@/lib/auth'

jest.mock('@/lib/supabase')
jest.mock('@/lib/auth')

describe('POST /api/markets', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('authentication', () => {
    it('returns 401 when user is not authenticated', async () => {
      ;(getSession as jest.Mock).mockResolvedValue(null)

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({ name: 'Test' })
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(401)
      expect(data.error).toBe('Unauthorized')
    })

    it('returns 401 when session is invalid', async () => {
      ;(getSession as jest.Mock).mockResolvedValue({ user: null })

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({ name: 'Test' })
      })

      const response = await POST(request)

      expect(response.status).toBe(401)
    })
  })

  describe('validation', () => {
    beforeEach(() => {
      ;(getSession as jest.Mock).mockResolvedValue({
        user: { id: 'user-123' }
      })
    })

    it('returns 400 when name is missing', async () => {
      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({ description: 'Test' })
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(400)
      expect(data.error).toBe('Name is required')
    })

    it('returns 400 when name is too short', async () => {
      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({ name: 'ab' })
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(400)
      expect(data.error).toBe('Name must be at least 3 characters')
    })

    it('returns 400 when end_date is in the past', async () => {
      const pastDate = new Date(2020, 0, 1).toISOString()

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({
          name: 'Test Market',
          end_date: pastDate
        })
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(400)
      expect(data.error).toBe('End date must be in the future')
    })

    it('returns 400 when description is too long', async () => {
      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({
          name: 'Test',
          description: 'a'.repeat(1001)
        })
      })

      const response = await POST(request)

      expect(response.status).toBe(400)
    })
  })

  describe('success cases', () => {
    beforeEach(() => {
      ;(getSession as jest.Mock).mockResolvedValue({
        user: { id: 'user-123' }
      })
    })

    it('creates market and returns 201', async () => {
      const newMarket = {
        slug: 'test-market',
        name: 'Test Market',
        description: 'A test market',
        end_date: '2025-12-31'
      }

      ;(supabase.from as any).mockReturnValue({
        insert: jest.fn().mockReturnValue({
          select: jest.fn().mockReturnValue({
            single: jest.fn().mockResolvedValue({
              data: { ...newMarket, id: 1, creator_id: 'user-123' },
              error: null
            })
          })
        })
      })

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify(newMarket)
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(201)
      expect(data.success).toBe(true)
      expect(data.data.name).toBe('Test Market')
    })

    it('generates slug from name', async () => {
      ;(supabase.from as any).mockReturnValue({
        insert: jest.fn().mockReturnValue({
          select: jest.fn().mockReturnValue({
            single: jest.fn().mockResolvedValue({
              data: {
                slug: 'my-test-market',
                name: 'My Test Market'
              },
              error: null
            })
          })
        })
      })

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({
          name: 'My Test Market'
        })
      })

      const response = await POST(request)
      const data = await response.json()

      expect(response.status).toBe(201)
      expect(data.data.slug).toBe('my-test-market')
    })
  })

  describe('database errors', () => {
    beforeEach(() => {
      ;(getSession as jest.Mock).mockResolvedValue({
        user: { id: 'user-123' }
      })
    })

    it('returns 500 when database insert fails', async () => {
      ;(supabase.from as any).mockReturnValue({
        insert: jest.fn().mockReturnValue({
          select: jest.fn().mockReturnValue({
            single: jest.fn().mockResolvedValue({
              data: null,
              error: { message: 'Database connection failed' }
            })
          })
        })
      })

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({ name: 'Test' })
      })

      const response = await POST(request)

      expect(response.status).toBe(500)
    })

    it('returns 500 for unexpected errors', async () => {
      ;(supabase.from as any).mockImplementation(() => {
        throw new Error('Unexpected error')
      })

      const request = new NextRequest('http://localhost/api/markets', {
        method: 'POST',
        body: JSON.stringify({ name: 'Test' })
      })

      const response = await POST(request)

      expect(response.status).toBe(500)
    })
  })
})
```

#### Step 3: Implement Route Handler

**File: `apps/web/app/api/markets/route.ts`**

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { supabase } from '@/lib/supabase'
import { getSession } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getSession()
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    // Parse request body
    const body = await request.json()
    const { name, description, end_date } = body

    // Validation
    if (!name || name.trim().length < 3) {
      return NextResponse.json(
        { error: name?.length < 3 ? 'Name must be at least 3 characters' : 'Name is required' },
        { status: 400 }
      )
    }

    if (description && description.length > 1000) {
      return NextResponse.json(
        { error: 'Description must be less than 1000 characters' },
        { status: 400 }
      )
    }

    if (end_date) {
      const endDate = new Date(end_date)
      if (endDate <= new Date()) {
        return NextResponse.json(
          { error: 'End date must be in the future' },
          { status: 400 }
        )
      }
    }

    // Generate slug from name
    const slug = name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '')

    // Insert market
    const { data, error } = await supabase
      .from('markets')
      .insert({
        slug,
        name: name.trim(),
        description: description?.trim() || null,
        end_date: end_date || null,
        creator_id: session.user.id
      })
      .select()
      .single()

    if (error) {
      return NextResponse.json(
        { error: error.message },
        { status: 500 }
      )
    }

    return NextResponse.json({
      success: true,
      data
    }, { status: 201 })

  } catch (error) {
    console.error('Error creating market:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

#### Step 4: Run Tests
```bash
npm test route.test.ts
# PASS: All tests green, 100% coverage
```

---

## E2E Test Examples

### Example: Complete User Journey

**File: `e2e/trading-flow.spec.ts`**

```typescript
import { test, expect } from '@playwright/test'

test.describe('Trading Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/')
  })

  test('complete trading workflow', async ({ page }) => {
    // 1. Navigate to markets
    await page.click('a[href="/markets"]')
    await expect(page).toHaveURL(/\/markets/)

    // 2. Search for a market
    await page.fill('input[placeholder="Search markets"]', 'bitcoin')
    await page.waitForTimeout(500) // Wait for debounce

    // 3. Click on a market
    await page.click('[data-testid="market-card"]:first-child')
    await expect(page).toHaveURL(/\/markets\/bitcoin-/)

    // 4. Place a buy order
    await page.click('button:has-text("Buy Yes")')
    await page.fill('input[type="number"]', '10')
    await page.click('button:has-text("Confirm Order")')

    // 5. Verify success message
    await expect(page.locator('text=Order placed successfully')).toBeVisible()

    // 6. Check order in portfolio
    await page.click('a[href="/portfolio"]')
    await expect(page.locator('text=Bitcoin')).toBeVisible()
    await expect(page.locator('text=10 shares')).toBeVisible()
  })

  test('handles insufficient balance', async ({ page }) => {
    await page.goto('/markets/bitcoin-price')
    await page.click('button:has-text("Buy Yes")')

    // Try to buy more than balance allows
    await page.fill('input[type="number"]', '999999')
    await page.click('button:has-text("Confirm Order")')

    // Verify error message
    await expect(page.locator('text=Insufficient balance')).toBeVisible()
  })

  test('validates order input', async ({ page }) => {
    await page.goto('/markets/bitcoin-price')
    await page.click('button:has-text("Buy Yes")')

    // Test negative number
    await page.fill('input[type="number"]', '-5')
    await page.click('button:has-text("Confirm Order")')

    await expect(page.locator('text=Invalid amount')).toBeVisible()

    // Test zero
    await page.fill('input[type="number"]', '0')
    await page.click('button:has-text("Confirm Order")')

    await expect(page.locator('text=Amount must be greater than 0')).toBeVisible()
  })

  test('cancels order correctly', async ({ page }) => {
    await page.goto('/markets/bitcoin-price')
    await page.click('button:has-text("Buy Yes")')
    await page.fill('input[type="number"]', '10')
    await page.click('button:has-text("Cancel")')

    // Verify modal is closed and no order placed
    await expect(page.locator('text=Order placed')).not.toBeVisible()
  })
})
```

---

## Test Utilities and Helpers

### Factory Functions for Test Data

```typescript
// tests/factories.ts
export function createMockMarket(overrides = {}) {
  return {
    slug: 'test-market',
    name: 'Test Market',
    description: 'A test market',
    status: 'active',
    end_date: '2025-12-31',
    creator_id: 'user-123',
    created_at: new Date().toISOString(),
    ...overrides
  }
}

export function createMockUser(overrides = {}) {
  return {
    id: 'user-123',
    email: 'test@example.com',
    name: 'Test User',
    balance: 1000,
    ...overrides
  }
}

export function createMockOrder(overrides = {}) {
  return {
    id: 'order-123',
    user_id: 'user-123',
    market_slug: 'test-market',
    type: 'buy',
    shares: 10,
    price: 0.50,
    status: 'filled',
    ...overrides
  }
}
```

### Custom Test Matchers

```typescript
// tests/setup.ts
import { expect } from '@jest/globals'

customMatchers.ts

expect.extend({
  toBeValidISODate(received: string) {
    const pass = !isNaN(Date.parse(received))
    return {
      pass,
      message: () => pass
        ? `Expected ${received} not to be a valid ISO date`
        : `Expected ${received} to be a valid ISO date`
    }
  },

  toHaveStatusCode(received: Response, expected: number) {
    const pass = received.status === expected
    return {
      pass,
      message: () => pass
        ? `Expected response not to have status ${expected}`
        : `Expected response to have status ${expected}, got ${received.status}`
    }
  }
})
```

### Test Database Utilities

```typescript
// tests/db.ts
import { supabase } from '@/lib/supabase'

export async function truncateTable(tableName: string) {
  await supabase.from(tableName).delete().neq('id', 0)
}

export async function seedMarket(market: any) {
  const { data, error } = await supabase
    .from('markets')
    .insert(market)
    .select()
    .single()

  if (error) throw error
  return data
}

export async function cleanupTest() {
  await truncateTable('orders')
  await truncateTable('markets')
  await truncateTable('users')
}
```

---

## CI/CD Configuration Examples

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run unit tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload E2E test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .husky/pre-commit

echo "Running tests..."
npm test -- --passWithNoTests

if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi

echo "Running linter..."
npm run lint:fix

echo "Pre-commit checks passed!"
```

---

This patterns file provides real-world TDD examples for frontend components, backend routes, and E2E flows, along with testing utilities and CI/CD setup.
