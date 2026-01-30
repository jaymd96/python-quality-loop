# Annotation Patterns Reference

Detailed patterns for high-quality literate annotations.

## Pattern: Algorithm Explanation

```python
#> **Levenshtein Distance via Dynamic Programming**
#  We build an (m+1) × (n+1) matrix where cell [i,j] represents
#  the minimum edits to transform the first i characters of `source`
#  into the first j characters of `target`. This bottom-up approach
#  avoids the exponential blowup of naive recursion.
def levenshtein(source: str, target: str) -> int:
    m, n = len(source), len(target)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    #> Base cases: transforming empty string requires i insertions
    #  or j deletions respectively.
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i-1] == target[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # deletion
                    dp[i][j-1],      # insertion
                    dp[i-1][j-1]     # substitution
                )
    return dp[m][n]
```

## Pattern: Business Logic Context

```python
#> **Pricing Tier Calculation**
#  Enterprise customers (>100 seats) receive volume discounts per
#  the 2024 pricing matrix. The 15% threshold was negotiated with
#  Sales as the maximum sustainable discount while maintaining
#  target margins. See PRICING-2024-Q1 for full breakdown.
def calculate_tier_price(seats: int, base_price: float) -> float:
    if seats > 100:
        discount = min(0.15, seats * 0.001)
        return base_price * (1 - discount)
    return base_price
```

## Pattern: Performance Rationale

```python
#> Using `__slots__` reduces memory footprint by ~40% for these
#  high-volume event objects. Profiling showed 2M+ instances
#  in memory during peak load; the dict overhead was significant.
class Event:
    __slots__ = ('timestamp', 'event_type', 'payload')
    
    def __init__(self, timestamp, event_type, payload):
        self.timestamp = timestamp
        self.event_type = event_type
        self.payload = payload
```

## Pattern: Edge Case Documentation

```python
def parse_date(date_str: str) -> datetime:
    #> Legacy systems send dates in inconsistent formats. The order
    #  of parsing attempts reflects frequency in production logs:
    #  ISO 8601 (78%), US format (15%), European format (7%).
    formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    #> Fallback: dateutil handles exotic formats but is 10x slower,
    #  so we only use it for the ~0.1% of unparseable dates.
    return dateutil.parser.parse(date_str)
```

## Pattern: Security Considerations

```python
#> **Rate Limiting Implementation**
#  Uses token bucket algorithm with per-IP tracking. The 100 req/min
#  limit was chosen based on legitimate usage patterns from analytics.
#  Attackers attempting credential stuffing typically exceed this
#  within seconds.
#  
#  **Security note**: IP-based limiting can be bypassed with proxies;
#  this is defense-in-depth alongside CAPTCHA and account lockout.
@rate_limit(requests=100, window=60)
def authenticate(username: str, password: str) -> AuthResult:
    ...
```

## Pattern: Mathematical Foundation

```python
#> **Newton-Raphson Root Finding**
#  Given f(x) and its derivative f'(x), we iteratively refine
#  our estimate: x_{n+1} = x_n - f(x_n)/f'(x_n)
#  
#  Convergence is quadratic near the root, but the method can
#  diverge if the initial guess is poor or f'(x) ≈ 0.
def newton_raphson(f, df, x0, tolerance=1e-10, max_iter=100):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tolerance:
            return x
        x = x - fx / df(x)
    raise ConvergenceError(f"Failed to converge after {max_iter} iterations")
```

## Anti-Patterns to Avoid

### Restating the Obvious

```python
# BAD
#> Create a dictionary mapping user IDs to user objects
users_by_id = {u.id: u for u in users}

# GOOD (if annotation needed at all)
#> Index enables O(1) lookups during the join phase, avoiding
#  the O(n²) scan that caused the 2023-Q4 performance incident.
users_by_id = {u.id: u for u in users}
```

### Explaining Language Features

```python
# BAD
#> Use a context manager to ensure the file is closed
with open(path) as f:
    data = f.read()

# GOOD (only if there's domain context)
#> Config files are read at startup and cached; we don't hold
#  file handles open because containerized deployments may
#  remount volumes during rolling updates.
with open(path) as f:
    data = f.read()
```

### Narrative Padding

```python
# BAD
#> Now we need to process the data. First, we'll filter it,
#  then we'll transform it, and finally we'll aggregate it.
#  This is an important step in our pipeline.

# GOOD
#> Filter→Transform→Aggregate pipeline. Each stage is lazy
#  (generator-based) to handle datasets larger than RAM.
```

## Annotation Density Guidelines

- **High-level modules**: More annotations explaining architecture
- **Utility functions**: Minimal annotations unless non-obvious
- **Business logic**: Annotate rules, thresholds, edge cases
- **Algorithms**: Annotate approach, complexity, tradeoffs
- **Integrations**: Annotate API quirks, retry logic, timeouts

## Markdown Features in Annotations

```python
#> **Bold** for emphasis, *italic* for terms, `code` for identifiers.
#  
#  Links work: see [RFC 7231](https://tools.ietf.org/html/rfc7231)
#  for HTTP semantics.
#  
#  Code blocks in annotations:
#  ```
#  Expected format: {"status": "ok", "data": [...]}
#  ```
```
