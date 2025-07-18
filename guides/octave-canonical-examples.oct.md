===OCTAVE_CANONICAL_EXAMPLES===
// Two gold-standard snippets for model learning

META:
  NAME::"OCTAVE Canonical Examples"
  VERSION::"1.0"
  PURPOSE::"Concrete patterns that models generalize from"

DIAGNOSTIC_EXAMPLE:
  SYSTEM_STATUS:
    STATE::[NORMAL->WARNING->DEGRADED]
    PATTERN::RESOURCE_BOTTLENECK
    ROOT_CAUSE::DB_INDEX_REBUILD
  
  COMPONENTS:
    DATABASE:
      STATUS::DEGRADED
      CONNECTIONS::2047  // saturated
      QUERY_TIME::1250ms
    SERVER:
      STATUS::WARNING
      CPU::[45, 68, 94]  // progression
      MEMORY::82

  CAUSALITY::[DB_LOCK->QUERY_BACKUP->CPU_SPIKE->USER_TIMEOUT]

STRATEGY_EXAMPLE:
  CHALLENGE::SCALING_CRISIS
  TENSION::PERFORMANCE _VERSUS_ CONSISTENCY
  FORCES:
    CHRONOS::DEADLINE_PRESSURE
    HUBRIS::OVERCONFIDENT_ARCHITECTURE
  
  STRATEGY::ATHENA+GORDIAN
  APPROACH::[ANALYZE->SIMPLIFY->EXECUTE]
  SUCCESS_CRITERIA:
    LATENCY::"<100ms"
    AVAILABILITY::"99.9%"
    COST_INCREASE::"<20%"

===END===