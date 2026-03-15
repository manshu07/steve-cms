# Continuous Agent Loop Patterns

## Canonical Loop Structure

### v1.8 Standard Loop

```python
class ContinuousAgentLoop:
    """
    Core loop for autonomous agents with quality gates and recovery
    """

    def __init__(self, agent_config):
        self.config = agent_config
        self.state = {
            'iterations': 0,
            'errors': [],
            'evaluations': []
        }

    async def run(self, task):
        """
        Main execution loop
        """
        while not self.is_complete():
            # 1. Planning
            plan = await self.plan(task)

            # 2. Execution
            result = await self.execute(plan)

            # 3. Quality Gate
            passed = await self.quality_gate(result)

            # 4. Evaluation
            score = await self.evaluate(result)

            # 5. Recovery (if failed)
            if not passed:
                result = await self.recover(result)

            # 6. Update state
            self.update_state(result)

        return result
```

## Quality Gates

### Gate Types

```python
class QualityGate:
    """
    Define quality thresholds for agent outputs
    """

    async def check_completion(self, result):
        """
        Gate 1: Completion Check
        - Is task complete?
        - Are all requirements met?
        """
        return {
            'passed': bool(result.get('output')),
            'reason': 'No output generated' if not result.get('output') else None
        }

    async def check_quality(self, result):
        """
        Gate 2: Quality Check
        - Output meets quality standards?
        - No errors or warnings?
        """
        return {
            'passed': result.get('errors', 0) == 0,
            'reason': f"{result.get('errors')} errors found"
        }

    async def check_safety(self, result):
        """
        Gate 3: Safety Check
        - No harmful output?
        - Within constraints?
        """
        return {
            'passed': self.is_safe(result),
            'reason': 'Safety check failed' if not self.is_safe(result) else None
        }
```

## Evaluation Patterns

### Evaluator Template

```python
class AgentEvaluator:
    """
    Evaluate agent outputs with scoring
    """

    def __init__(self, criteria):
        self.criteria = criteria

    async def evaluate(self, result):
        """
        Score output against criteria
        """
        scores = {}

        for criterion, spec in self.criteria.items():
            score = await self.score_criterion(result, criterion, spec)
            scores[criterion] = score

        return {
            'overall_score': sum(scores.values()) / len(scores),
            'individual_scores': scores,
            'passed': all(s > 0.7 for s in scores.values())
        }
```

## Recovery Controls

### Error Recovery

```python
class RecoverySystem:
    """
    Recover from agent errors with fallback strategies
    """

    async def recover(self, error, context):
        """
        Attempt recovery from error
        """
        # Strategy 1: Retry with different model
        if error.type == 'model_error':
            return await self.retry_with_model(error, context)

        # Strategy 2: Simplify task
        if error.type == 'complexity_error':
            return await self.simplify_task(error, context)

        # Strategy 3: Request clarification
        if error.type == 'ambiguity_error':
            return await self.request_clarification(error, context)

        # Strategy 4: Fail gracefully
        return await self.fail_gracefully(error, context)
```

## Loop Patterns

### Pattern 1: Exploratory Loop

```python
class ExploratoryLoop:
    """
    For tasks with uncertain solution path
    """
    async def run(self, task):
        max_iterations = 10

        for i in range(max_iterations):
            # Explore
            action = await self.decide_action(task)
            result = await self.execute(action)

            # Evaluate
            progress = await self.evaluate_progress(result)

            # Update strategy
            if progress > 0.8:
                task = await self.refine_task(task, result)
            elif progress < 0.2:
                task = await self.pivot_task(task, result)

            # Check completion
            if await self.is_complete(task):
                return result
```

### Pattern 2: Optimization Loop

```python
class OptimizationLoop:
    """
    For improving outputs iteratively
    """
    async def run(self, task):
        best_result = None
        best_score = 0
        max_iterations = 5

        for i in range(max_iterations):
            # Generate variant
            variant = await self.generate_variant(task)
            result = await self.execute(variant)

            # Evaluate
            score = await self.evaluate(result)

            # Keep best
            if score > best_score:
                best_result = result
                best_score = score

            # Check convergence
            if self.converged(i, best_score):
                break

        return best_result
```

### Pattern 3: Verification Loop

```python
class VerificationLoop:
    """
    For validating outputs against requirements
    """
    async def run(self, task, requirements):
        output = await self.initial_generation(task)

        while not self.satisfied(requirements, output):
            # Identify gap
            gaps = await self.find_gaps(requirements, output)

            # Fill gaps
            output = await self.fill_gaps(gaps, output)

            # Verify
            if await self.verify(requirements, output):
                return output

        return output
```

## Anti-Patterns

### ❌ Infinite Loops

```python
# BAD: No termination condition
while True:
    result = await self.process(task)
    if not result.success:
        continue  # Will retry forever!

# GOOD: Max iterations
for i in range(max_iterations):
    result = await self.process(task)
    if result.success:
        break
```

### ❌ No Recovery

```python
# BAD: No error handling
result = await self.execute(task)
return result  # Will fail if error

# GOOD: With recovery
try:
    result = await self.execute(task)
except Error as e:
    result = await self.recover(e, task)
return result
```

### ❌ No Evaluation

```python
# BAD: No quality check
result = await self.execute(task)
return result  # May be low quality

# GOOD: With quality gate
result = await self.execute(task)
if await self.quality_gate(result):
    return result
else:
    return await self.improve(result)
```

## Configuration

### Agent Config

```json
{
  "agent_name": "code_review_agent",
  "max_iterations": 10,
  "quality_gates": ["completion", "quality", "safety"],
  "evaluators": ["code_quality", "best_practices", "security"],
  "recovery_strategies": ["retry", "fallback", "clarify"],
  "evaluation_threshold": 0.7,
  "convergence_threshold": 0.9
}
```

## Monitoring

### Metrics to Track

```python
class LoopMetrics:
    """
    Track loop performance
    """

    def __init__(self):
        self.metrics = {
            'iterations': 0,
            'errors': 0,
            'recoveries': 0,
            'evaluations': [],
            'avg_score': 0,
            'completion_time': 0
        }

    def log_iteration(self, result):
        """
        Log iteration metrics
        """
        self.metrics['iterations'] += 1
        if result.get('error'):
            self.metrics['errors'] += 1
        if result.get('recovered'):
            self.metrics['recoveries'] += 1
        self.metrics['evaluations'].append(result.get('score', 0))
```

---

This resources file provides comprehensive patterns for continuous autonomous agent loops.
