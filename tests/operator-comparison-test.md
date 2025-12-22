# OCTAVE Operator Comparison Test

## Objective
Test which operator representations produce better LLM outputs for agent prompts.

## Test Matrix

### Tension Operators
```
TEST_T1: SPEED _VERSUS_ QUALITY
TEST_T2: SPEED vs QUALITY
TEST_T3: SPEED ⚡ QUALITY
TEST_T4: SPEED # QUALITY
TEST_T5: SPEED × QUALITY
```

### Synthesis Operators
```
TEST_S1: APOLLO + HERMES
TEST_S2: APOLLO ⊕ HERMES
TEST_S3: APOLLO & HERMES
TEST_S4: APOLLO ∧ HERMES
TEST_S5: APOLLO ♪ HERMES
```

### Combined Context Test
```
# Base agent definition (change only operators)
COGNITION::LOGOS
ROLE::SECURITY_ARCHITECT
ARCHETYPES::ATHENA [OPERATOR] PROMETHEUS
MISSION::PREVENT→CHAOS
BALANCE::SPEED [TENSION_OP] QUALITY
```

## Quick Manual Test

```bash
# Test with zen-chat
mcp zen chat --model o3-mini --prompt "
COGNITION::LOGOS
ROLE::ARCHITECT
BALANCE::SPEED _VERSUS_ QUALITY
[rest of prompt]
"

# vs

mcp zen chat --model o3-mini --prompt "
COGNITION::LOGOS
ROLE::ARCHITECT
BALANCE::SPEED ⚡ QUALITY
[rest of prompt]
"
```

## Measurement Criteria
1. Does operator choice affect comprehension?
2. Does visual impact improve semantic activation?
3. Do abbreviated forms (vs) work as well as verbose (_VERSUS_)?
4. Do Unicode symbols cause issues or enhance understanding?

## Expected Outcomes
- Visual operators (⚡, ♪) may enhance semantic priming
- Natural abbreviations (vs, &) may work as well as verbose
- Context matters - security agents may respond better to conflict symbols
- ASCII fallbacks important for compatibility
