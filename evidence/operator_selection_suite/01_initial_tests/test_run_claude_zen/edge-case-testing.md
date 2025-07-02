# Edge Case and Ambiguity Testing

## Test Case 1: Mathematical Context Confusion

### Scenario: Algorithm Documentation
"The load balancer uses weighted round-robin: Server1 * 0.5 + Server2 * 0.3 + Server3 * 0.2"

| Approach | Expression | Ambiguity Level | Interpretation |
|----------|------------|-----------------|----------------|
| Unicode | `Server1 ⊕ Weight ⚡ 0.5 → Load` | Low | Clear: synthesis with tension |
| ASCII Math | `Server1 * 0.5 + Server2 * 0.3` | **CRITICAL** | Is this math or OCTAVE? |
| ASCII Text | `Server1 _AND_ Weight _VS_ 0.5` | Low | Clearly not math |
| Natural | `Server1 WITH Weight VERSUS 0.5` | Low | Clearly not math |

**Finding**: ASCII Math fails catastrophically in mathematical contexts

## Test Case 2: Boolean Logic Confusion

### Scenario: Access Control Rules
"Access granted if: (Admin + User) * Active"

| Approach | Expression | Ambiguity Level | Interpretation |
|----------|------------|-----------------|----------------|
| Unicode | `Admin ⊕ User ⚡ Active` | Low | System relationship |
| ASCII Math | `(Admin + User) * Active` | **HIGH** | Boolean? OCTAVE? Math? |
| ASCII Text | `Admin _AND_ User _VS_ Active` | Medium | Could be boolean AND |
| Natural | `Admin WITH User VERSUS Active` | Low | Not boolean |

**Finding**: ASCII Math and ASCII Text both problematic in logic contexts

## Test Case 3: Nested Relationships

### Scenario: Complex Service Orchestration
"((A ⊕ B) ⚡ C) ⊕ (D ⚡ E) → F"

| Approach | Readability | Parse Difficulty | Error Potential |
|----------|-------------|------------------|-----------------|
| Unicode | Medium | Medium | Low |
| ASCII Math | Low | High | **Very High** |
| ASCII Text | Very Low | Low | Low |
| Natural | Unreadable | Very Low | Low |

**Finding**: Unicode handles nesting best; Natural language becomes unwieldy

## Test Case 4: Undefined Operator Sequences

### What if someone writes invalid sequences?

| Invalid Pattern | Unicode | ASCII Math | ASCII Text | Natural |
|-----------------|---------|------------|------------|---------|
| Double synthesis | `A ⊕ ⊕ B` | `A + + B` | `A _AND_ _AND_ B` | `A WITH WITH B` |
| Missing progress | `A ⊕ B ⚡ C` | `A + B * C` | `A _AND_ B _VS_ C` | `A WITH B VERSUS C` |
| Wrong order | `A → B ⊕ C` | `A -> B + C` | `A _TO_ B _AND_ C` | `A LEADS_TO B WITH C` |

**Finding**: ASCII Math most likely to create valid-looking but semantically wrong expressions

## Test Case 5: Domain-Specific Conflicts

### Database Query Context
```sql
SELECT * FROM orders WHERE user_id = 123 AND status = 'active'
-- Document flow: Query + Cache * Timeout -> Result
```

| Approach | Conflict Level | Disambiguation |
|----------|----------------|----------------|
| Unicode | None | Clear separation |
| ASCII Math | **SEVERE** | Conflicts with SQL math |
| ASCII Text | Medium | _AND_ conflicts with SQL AND |
| Natural | Low | Verbose but clear |

## Test Case 6: Parser/Tool Compatibility

### YAML Configuration
```yaml
flow_rules:
  - pattern: Service + Auth * RateLimit -> Result
  - pattern: Service ⊕ Auth ⚡ RateLimit → Result  
```

| Approach | YAML Safe | JSON Safe | XML Safe | Regex Safe |
|----------|-----------|-----------|----------|------------|
| Unicode | No | No | Sometimes | No |
| ASCII Math | Yes | Yes | Yes | No (meta chars) |
| ASCII Text | Yes | Yes | Yes | Yes |
| Natural | Yes | Yes | Yes | Yes |

## Test Case 7: Internationalization

### Non-English Documentation
```
服务A ⊕ 服务B ⚡ 速率限制 → 结果
Service A + Service B * Limite de Taux -> Résultat
```

| Approach | i18n Compatible | Direction Issues | Font Support |
|----------|-----------------|------------------|--------------|
| Unicode | Partial | RTL problems | Often missing |
| ASCII Math | Yes | None | Universal |
| ASCII Text | English-only | None | Universal |
| Natural | English-only | None | Universal |

## Test Case 8: Version Migration

### If we need to change operators later:
```
# Old: A ⊕ B ⚡ C → D
# New: A ⨁ B ⚦ C ⟹ D
```

| Approach | Migration Difficulty | Tooling Support | Regex Replace |
|----------|---------------------|-----------------|---------------|
| Unicode | High | Poor | Difficult |
| ASCII Math | Low | Excellent | Simple |
| ASCII Text | Very Low | Excellent | Trivial |
| Natural | Low | Excellent | Simple |

## Critical Ambiguity Summary

### Fatal Flaws Found:
1. **ASCII Math**: Unusable in mathematical/logical contexts
2. **ASCII Text**: AND operator conflicts with boolean logic
3. **Natural Language**: Becomes unreadable with nesting
4. **Unicode**: Poor tool support and internationalization

### Ambiguity Scores (Lower is Better)
1. Unicode: 3/10 (clear when it works)
2. ASCII Text: 5/10 (some boolean confusion)
3. Natural: 5/10 (verbose but clear)
4. ASCII Math: 9/10 (severe context conflicts)

## Recommendation Based on Edge Cases

**CRITICAL FINDING**: ASCII Math, despite good readability scores, has fatal ambiguity in common contexts (math, boolean logic, SQL).

### Revised Recommendation:
1. **ASCII Text** with modified operators to avoid AND conflict
2. **Unicode** for specialized contexts with controlled environment
3. **Natural Language** only for non-technical docs
4. **ASCII Math** - NOT RECOMMENDED due to critical ambiguity