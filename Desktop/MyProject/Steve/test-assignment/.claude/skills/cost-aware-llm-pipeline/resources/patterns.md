# Cost-Aware LLM Pipeline Patterns

## Model Cost Structure

### Pricing Reference (2025)

```
Claude Models (per million tokens):
├─ Haiku:   $0.25 (input) | $1.25 (output)
├─ Sonnet:  $3.00 (input) | $15.00 (output)
└─ Opus:   $15.00 (input) | $75.00 (output)

Cost Multipliers:
Haiku:  1x  (baseline)
Sonnet: 12x (input) | 12x (output)
Opus:   60x (input) | 60x (output)
```

### Cost Calculation Examples

```python
def calculate_cost(model, input_tokens, output_tokens):
    """
    Calculate API call cost
    """
    pricing = {
        'haiku': {'input': 0.25, 'output': 1.25},
        'sonnet': {'input': 3.0, 'output': 15.0},
        'opus': {'input': 15.0, 'output': 75.0}
    }

    rates = pricing[model]
    input_cost = (input_tokens / 1_000_000) * rates['input']
    output_cost = (output_tokens / 1_000_000) * rates['output']
    return input_cost + output_cost

# Examples
calculate_cost('haiku', 1000, 500)   # $0.000875
calculate_cost('sonnet', 1000, 500)  # $0.0105
calculate_cost('opus', 1000, 500)    # $0.0525

# Opus is 60x more expensive than Haiku
```

## Model Routing Strategy

### Task Complexity Classification

```python
class TaskClassifier:
    """
    Classify tasks to route to appropriate model
    """

    def classify(self, task):
        """
        Determine task complexity
        """
        # Level 1: Simple tasks → Haiku
        if self.is_simple_task(task):
            return 'haiku'

        # Level 2: Medium complexity → Sonnet
        if self.is_medium_task(task):
            return 'sonnet'

        # Level 3: High complexity → Opus
        return 'opus'

    def is_simple_task(self, task):
        """
        Quick/High-volume tasks suitable for Haiku
        """
        simple_indicators = [
            task.get('token_count', 0) < 1000,  # Short context
            task.get('type') in ['summarization', 'extraction'],  # Structured
            not task.get('requires_reasoning'),  # No complex reasoning
            task.get('confidence_required', 0) < 0.7,  # Lower accuracy needed
            task.get('batch_mode', False)  # Batch processing
        ]
        return sum(simple_indicators) >= 3

    def is_medium_task(self, task):
        """
        Standard tasks suitable for Sonnet
        """
        medium_indicators = [
            1000 <= task.get('token_count', 0) < 10000,  # Medium context
            task.get('type') in ['analysis', 'coding', 'writing'],  # Standard complexity
            task.get('requires_reasoning'),  # Some reasoning needed
            0.7 <= task.get('confidence_required', 0) < 0.9,  # Medium accuracy
        ]
        return sum(medium_indicators) >= 2
```

### Routing Decision Tree

```
Task received
│
├─ Is it a batch operation?
│  └─ Yes → Use Haiku (high volume, low cost)
│
├─ Token count > 100K?
│  └─ Yes → Use Haiku (cost concerns)
│
├─ Requires deep reasoning/analysis?
│  ├─ Yes → Confidence required?
│  │   ├─ >0.95 → Use Opus (highest quality)
│  │   └─ 0.7-0.95 → Use Sonnet (balance)
│  │
│   └─ No → Use Haiku (fast/cheap)
│
└─ Is cost the primary concern?
   └─ Yes → Start with Haiku, upgrade if quality insufficient
```

## Budget Management

### Budget Tracking

```python
class BudgetManager:
    """
    Track and manage LLM API spend
    """

    def __init__(self, daily_budget, monthly_budget):
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget
        self.daily_spend = 0
        self.monthly_spend = 0

    def can_execute(self, estimated_cost):
        """
        Check if task fits budget
        """
        # Check daily budget
        if self.daily_spend + estimated_cost > self.daily_budget:
            return False, 'Daily budget exceeded'

        # Check monthly budget
        if self.monthly_spend + estimated_cost > self.monthly_budget:
            return False, 'Monthly budget exceeded'

        return True, 'OK'

    def record_spend(self, cost):
        """
        Record actual spend
        """
        self.daily_spend += cost
        self.monthly_spend += cost

    def get_spend_summary(self):
        """
        Get current spend status
        """
        return {
            'daily': {
                'spent': self.daily_spend,
                'budget': self.daily_budget,
                'remaining': self.daily_budget - self.daily_spend,
                'percentage': (self.daily_spend / self.daily_budget) * 100
            },
            'monthly': {
                'spent': self.monthly_spend,
                'budget': self.monthly_budget,
                'remaining': self.monthly_budget - self.monthly_spend,
                'percentage': (self.monthly_spend / self.monthly_budget) * 100
            }
        }
```

### Budget Allocation Strategy

```python
def allocate_budget(task_queue, total_budget):
    """
    Allocate budget across tasks optimally
    """
    allocation = {}

    # Priority 1: Critical tasks → Opus budget
    critical_tasks = [t for t in task_queue if t['priority'] == 'critical']
    opus_budget = total_budget * 0.4  # 40% to Opus
    allocation['opus'] = opus_budget

    # Priority 2: Standard tasks → Sonnet budget
    standard_tasks = [t for t in task_queue if t['priority'] == 'standard']
    sonnet_budget = total_budget * 0.4  # 40% to Sonnet
    allocation['sonnet'] = sonnet_budget

    # Priority 3: Batch tasks → Haiku budget
    batch_tasks = [t for t in task_queue if t['priority'] == 'batch']
    haiku_budget = total_budget * 0.2  # 20% to Haiku
    allocation['haiku'] = haiku_budget

    return allocation
```

## Prompt Caching

### Cacheable Patterns

```python
class PromptCache:
    """
    Cache prompts to reduce token usage
    """

    def __init__(self):
        self.cache = {}

    def get_cache_key(self, prompt):
        """
        Generate cache key from prompt
        """
        # Remove dynamic values
        sanitized = re.sub(r'\d{4}-\d{2}-\d{2}', '[DATE]', prompt)
        sanitized = re.sub(r'\$\{?\w+\}?', '[VAR]', sanitized)
        return hashlib.md5(sanitized.encode()).hexdigest()

    def should_cache(self, prompt):
        """
        Determine if prompt should be cached
        """
        cacheable_indicators = [
            len(prompt) > 1000,  # Long prompts
            'system prompt' in prompt.lower(),  # System prompts
            'template' in prompt.lower(),  # Templates
            prompt.count('```') > 2,  # Code-heavy prompts
        ]
        return any(cacheable_indicators)

    def get_cached_response(self, prompt):
        """
        Retrieve cached response if available
        """
        key = self.get_cache_key(prompt)
        return self.cache.get(key)

    def cache_response(self, prompt, response):
        """
        Cache response for future use
        """
        if self.should_cache(prompt):
            key = self.get_cache_key(prompt)
            self.cache[key] = {
                'response': response,
                'timestamp': datetime.now(),
                'hits': 0
            }
```

### Caching Strategy

```
Cache Decision Flow:
│
├─ Is prompt > 1000 tokens?
│  └─ Yes → Cache it
│
├─ Is it a system prompt?
│  └─ Yes → Cache it (reuse across sessions)
│
├─ Does it contain code/templates?
│  └─ Yes → Cache structure, cache variables separately
│
└─ Is it one-time prompt?
   └─ No → Don't cache (save memory)
```

## Retry Logic

### Cost-Optimized Retry

```python
class RetryStrategy:
    """
    Retry failures with cost optimization
    """

    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.retry_costs = {
            'haiku': [1.0, 1.0, 1.0],    # Always retry with Haiku
            'sonnet': [1.0, 1.0, 1.2],   # Retry with Sonnet, then upgrade
            'opus': [1.0, 1.5, 2.0]      # Retry with Opus (expensive)
        }

    def should_retry(self, attempt, error_type, model):
        """
        Determine if should retry and with which model
        """
        if attempt >= self.max_retries:
            return False, None

        # Rate limiting → Retry with same model
        if error_type == 'rate_limit':
            return True, model

        # Timeout → Retry with same model
        if error_type == 'timeout':
            return True, model

        # Quality error → Upgrade model
        if error_type == 'quality':
            if model == 'haiku':
                return True, 'sonnet'
            elif model == 'sonnet':
                return True, 'opus'

        # Server error → Retry with same model
        if error_type == 'server_error':
            return True, model

        return False, None

    def calculate_retry_cost(self, model, attempt):
        """
        Calculate cumulative retry cost
        """
        return sum(self.retry_costs[model][:attempt+1])
```

### Retry with Model Upgrade

```python
async def execute_with_retry(task, initial_model='haiku'):
    """
    Execute task with intelligent retry
    """
    model = initial_model
    max_retries = 3

    for attempt in range(max_retries):
        try:
            # Execute with current model
            result = await execute(task, model)

            # Quality check
            if check_quality(result):
                return result
            else:
                # Quality insufficient, upgrade model
                if model == 'haiku':
                    model = 'sonnet'
                elif model == 'sonnet':
                    model = 'opus'
                else:
                    return result  # Already at Opus, return as-is

        except RateLimitError:
            # Wait and retry with same model
            await asyncio.sleep(2 ** attempt)
            continue

        except TimeoutError:
            # Retry with same model
            continue

    return None
```

## Prompt Optimization

### Token Reduction Techniques

```python
def optimize_prompt(prompt):
    """
    Reduce token count while maintaining quality
    """
    # Technique 1: Remove redundant phrases
    prompt = re.sub(r'please\s+', '', prompt)
    prompt = re.sub(r'i\s+would\s+like\s+you\s+to\s+', '', prompt)

    # Technique 2: Use concise language
    prompt = re.sub(r'in\s+order\s+to', 'to', prompt)
    prompt = re.sub(r'as\s+well\s+as', 'and', prompt)

    # Technique 3: Remove filler words
    filler_words = ['basically', 'actually', 'literally', 'just']
    for word in filler_words:
        prompt = re.sub(r'\b' + word + r'\b', '', prompt)

    # Technique 4: Use code for structured data
    if '<json>' in prompt and '</json>' in prompt:
        # Keep JSON format (efficient)
        pass

    return prompt.strip()

# Example
original = "I would like you to please analyze the following data in order to find patterns"
optimized = "Analyze data to find patterns"
# Savings: ~50% tokens
```

### Structured Prompt Template

```python
def create_structured_prompt(task):
    """
    Create efficient structured prompt
    """
    template = """
Task: {task_type}

Context:
{context}

Requirements:
{requirements}

Output Format:
{format}

Input:
{input}
"""

    return template.format(
        task_type=task['type'],
        context=format_context(task['context']),
        requirements=format_requirements(task['requirements']),
        format=task.get('format', 'json'),
        input=task['input']
    )
```

## Usage Patterns

### Batch Processing

```python
async def process_batch(tasks, budget_limit):
    """
    Process batch of tasks within budget
    """
    results = []
    total_cost = 0

    # Sort by priority
    tasks.sort(key=lambda t: t['priority'], reverse=True)

    for task in tasks:
        # Estimate cost
        estimated_cost = estimate_cost(task)

        # Check budget
        if total_cost + estimated_cost > budget_limit:
            print(f"Budget limit reached, skipping {task['id']}")
            break

        # Route to appropriate model
        model = route_task(task)

        # Execute
        result = await execute(task, model)
        results.append(result)

        # Track cost
        actual_cost = calculate_cost(model, result['input_tokens'], result['output_tokens'])
        total_cost += actual_cost

    return results, total_cost
```

### Streaming for Long Outputs

```python
async def execute_streaming(prompt, model):
    """
    Execute with streaming to monitor cost
    """
    max_tokens = 4000  # Set limit
    current_tokens = 0
    output = []

    async for chunk in stream_completion(prompt, model):
        output.append(chunk)
        current_tokens += len(chunk.split())

        # Check if approaching limit
        if current_tokens > max_tokens * 0.9:
            print(f"Warning: Approaching token limit ({current_tokens}/{max_tokens})")

        # Stop if limit reached
        if current_tokens >= max_tokens:
            print(f"Token limit reached, truncating output")
            break

    return ''.join(output)
```

## Monitoring

### Cost Tracking Dashboard

```python
class CostDashboard:
    """
    Real-time cost monitoring
    """

    def __init__(self):
        self.metrics = {
            'total_cost': 0,
            'total_tokens': 0,
            'calls_by_model': {
                'haiku': 0,
                'sonnet': 0,
                'opus': 0
            },
            'cost_by_model': {
                'haiku': 0,
                'sonnet': 0,
                'opus': 0
            }
        }

    def log_call(self, model, input_tokens, output_tokens, cost):
        """
        Log API call
        """
        self.metrics['total_cost'] += cost
        self.metrics['total_tokens'] += input_tokens + output_tokens
        self.metrics['calls_by_model'][model] += 1
        self.metrics['cost_by_model'][model] += cost

    def get_summary(self):
        """
        Get cost summary
        """
        return {
            'total_cost': self.metrics['total_cost'],
            'total_tokens': self.metrics['total_tokens'],
            'avg_cost_per_1k_tokens': (self.metrics['total_cost'] / self.metrics['total_tokens']) * 1000,
            'model_distribution': {
                model: {
                    'calls': self.metrics['calls_by_model'][model],
                    'cost': self.metrics['cost_by_model'][model],
                    'percentage': (self.metrics['cost_by_model'][model] / self.metrics['total_cost']) * 100
                }
                for model in ['haiku', 'sonnet', 'opus']
            }
        }
```

### Cost Optimization Checklist

- [ ] Use Haiku for simple, high-volume tasks
- [ ] Use Sonnet for standard operations
- [ ] Reserve Opus for complex, critical tasks
- [ ] Implement prompt caching for repeated prompts
- [ ] Set budget limits to prevent overspend
- [ ] Monitor costs in real-time
- [ ] Optimize prompts to reduce token count
- [ ] Use streaming for long outputs
- [ ] Implement retry with model upgrade
- [ ] Track costs per task/project

---

This resources file provides comprehensive patterns for cost-aware LLM usage with model routing, budget tracking, and optimization strategies.
