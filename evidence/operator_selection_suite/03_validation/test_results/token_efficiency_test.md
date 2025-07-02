# Token Efficiency Test Results

## Test Date: 2025-07-02

### Test Examples
All models tested with: `"AUTH_SERVICE[&]RATE_LIMITER[!]TIMEOUT[>]FAILURE_MODE"` and equivalents

### Token Count Results

| Representation | GPT-4.1 | Claude Opus 4 | Average |
|----------------|---------|---------------|---------|
| Square brackets `[&]` | 13 | 19 | 16 |
| Unicode `⊕⚡→` | 7 | 17 | 12 |
| ASCII Math `+*->` | 8 | 15 | 11.5 |
| ASCII Text `_AND_` | 1 | 21 | 11 |
| Natural Language | 7 | 17 | 12 |

### Key Findings

1. **Significant Tokenizer Differences**: GPT-4.1 and Claude Opus 4 show dramatically different token counts for the same strings
   - GPT-4.1 treats long snake_case as single tokens
   - Claude breaks down more granularly

2. **Square Brackets Performance**:
   - GPT-4.1: 13 tokens (worse than Unicode)
   - Claude: 19 tokens (worse than all except ASCII Text)
   - **Conclusion**: Square brackets are NOT the most token-efficient

3. **Most Efficient Overall**:
   - GPT-4.1: ASCII Text (1 token) - but misleading due to tokenizer behavior
   - Claude: ASCII Math (15 tokens)
   - **Real winner**: ASCII Math appears most consistently efficient

### Critical Discovery

⚠️ **The token efficiency claim for square brackets is FALSE**

Square brackets consistently rank among the LEAST efficient options across tokenizers. This contradicts the initial recommendation and suggests that token efficiency should NOT be a primary justification for square brackets.

### Revised Justification

If choosing square brackets, it must be for:
- Toolchain compatibility ✓
- Visual clarity ✓
- Unambiguity ✓
- NOT for token efficiency ✗