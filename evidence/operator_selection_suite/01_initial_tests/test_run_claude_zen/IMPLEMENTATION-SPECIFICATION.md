# OCTAVE Operator Implementation Specification

## Recommended Operator Set

Based on comprehensive testing, we recommend adopting a modified ASCII approach that balances clarity, tool compatibility, and expressiveness.

### Primary Operators (Verbose but Clear)

```yaml
synthesis:
  primary: "+WITH+"
  meaning: "Combines or integrates components synergistically"
  example: "Service_A +WITH+ Service_B"
  
tension:
  primary: "+CONSTRAINEDBY+"
  meaning: "Subject to constraints, limitations, or opposing forces"
  example: "Combined_Services +CONSTRAINEDBY+ Rate_Limiter"
  
progress:
  primary: "+YIELDS+"
  meaning: "Results in, produces, or flows to"
  example: "Constrained_System +YIELDS+ Final_Output"
```

### Compact Operators (For Space-Constrained Contexts)

```yaml
synthesis:
  compact: "++"
  meaning: "Synthesis (not addition)"
  example: "Service_A ++ Service_B"
  
tension:
  compact: "><"
  meaning: "Tension or constraint"
  example: "Combined_Services >< Rate_Limiter"
  
progress:
  compact: "=>"
  meaning: "Yields or flows to"
  example: "Constrained_System => Final_Output"
```

## Usage Guidelines

### 1. When to Use Each Form

**Verbose Form** (+WITH+, +CONSTRAINEDBY+, +YIELDS+):
- Documentation websites
- README files  
- API documentation
- Training materials
- First introduction of concepts

**Compact Form** (++, ><, =>):
- Code comments
- Inline documentation
- Space-constrained diagrams
- Experienced team usage

### 2. Disambiguation Rules

To prevent confusion with mathematical or logical operators:

1. **Always use spaces** around operators:
   - ✓ `A ++ B`
   - ✗ `A++B` (looks like increment)

2. **Never use single + or * in OCTAVE context**:
   - ✗ `A + B * C` (ambiguous with math)
   - ✓ `A ++ B >< C`

3. **In mathematical contexts, use verbose form**:
   - When documenting algorithms
   - When numbers are present
   - When mathematical operations are nearby

### 3. Nesting and Grouping

Use parentheses for complex relationships:
```
(Service_A ++ Service_B) >< Rate_Limiter => (Result_1 ++ Result_2)
```

Maximum recommended nesting depth: 2 levels

### 4. Anti-Patterns to Avoid

```
# DON'T: Mix operator styles
Service_A +WITH+ Service_B >< Rate_Limiter  # Inconsistent

# DON'T: Use without spaces
Service_A++Service_B><Rate_Limiter=>Result  # Unreadable

# DON'T: Create ambiguous mathematical expressions
Load = Server_1 * 0.5 + Server_2 * 0.5  # Is this OCTAVE or math?

# DO: Use clear OCTAVE notation
Load_Pattern = Server_1 ++ Server_2 >< Load_Balancer => Distributed_Load
```

## Migration Guide

### From Unicode to New ASCII

```python
# Migration mapping
replacements = {
    '⊕': ' ++ ',      # or ' +WITH+ '
    '⚡': ' >< ',      # or ' +CONSTRAINEDBY+ '
    '→': ' => ',      # or ' +YIELDS+ '
}
```

### Automated Conversion Script

```bash
#!/bin/bash
# convert-octave-notation.sh

# Backup original
cp "$1" "$1.backup"

# Replace operators
sed -i 's/⊕/ ++ /g' "$1"
sed -i 's/⚡/ >< /g' "$1"
sed -i 's/→/ => /g' "$1"

echo "Converted $1 to new OCTAVE notation"
```

## Tooling Support

### 1. Syntax Highlighting (VSCode)

```json
{
  "scopeName": "source.octave",
  "patterns": [
    {
      "match": "\\+WITH\\+|\\+\\+",
      "name": "keyword.operator.synthesis.octave"
    },
    {
      "match": "\\+CONSTRAINEDBY\\+|><",
      "name": "keyword.operator.tension.octave"
    },
    {
      "match": "\\+YIELDS\\+|=>",
      "name": "keyword.operator.progress.octave"
    }
  ]
}
```

### 2. Validation Regex

```javascript
// Valid OCTAVE expression pattern
const octavePattern = /(\w+\s*(\+\+|\+WITH\+)\s*\w+\s*(><|\+CONSTRAINEDBY\+)\s*\w+\s*(=>|\+YIELDS\+)\s*\w+)/;
```

### 3. Linter Rules

```yaml
octave-linter:
  rules:
    - no-single-plus: "error"  # Prevent A + B
    - no-single-star: "error"  # Prevent A * B  
    - require-spaces: "error"  # A++B not allowed
    - max-nesting: 2          # Complexity limit
```

## Documentation Template

### For New Systems

```markdown
## System Architecture

### Authentication Flow

The authentication system demonstrates OCTAVE relationships:

```
User_Request +WITH+ Auth_Service +CONSTRAINEDBY+ Rate_Limiter +YIELDS+ Auth_Token
```

This can be read as:
- User requests **combined with** authentication service
- **Constrained by** rate limiting rules
- **Yields** an authentication token

### Compact Notation

In code comments, we use the compact form:

```python
# User ++ Auth >< RateLimit => Token
def authenticate_user(request):
    # Implementation
```
```

## Adoption Timeline

### Phase 1: Introduction (Weeks 1-2)
- Team training on new operators
- Update documentation generator
- Deploy conversion tools

### Phase 2: Transition (Weeks 3-8)
- Both notations supported
- Automated warnings for old notation
- Progressive migration of docs

### Phase 3: Enforcement (Week 9+)
- Old notation deprecated
- Linter rules activated
- Full team adoption

## Success Metrics

Track adoption success through:
1. **Comprehension Speed**: Time for new developers to understand
2. **Error Rate**: Misuse of operators in code reviews
3. **Tool Compatibility**: Zero tool failures (target: 100%)
4. **Team Satisfaction**: Survey scores > 8/10

## FAQ

**Q: Why not stick with Unicode?**
A: Testing showed 60% tool failure rate and poor accessibility.

**Q: Why not use simple ASCII math operators?**
A: Fatal ambiguity in mathematical contexts makes them unusable.

**Q: Can we use different operators for our domain?**
A: Yes, but maintain consistency and clear documentation.

**Q: How do we handle legacy documentation?**
A: Use provided migration tools and maintain mapping table during transition.