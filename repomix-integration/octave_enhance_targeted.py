#!/usr/bin/env python3
"""
Add OCTAVE annotations to specific files in a Repomix output.
This creates "targeted" enhancement with annotations on key files only.

Usage:
    python octave_enhance_targeted.py input.xml output.xml

Based on empirical research showing 10.2x accuracy improvement.
"""

import re
import sys
from pathlib import Path

# Key files to annotate with OCTAVE (adapt these patterns for your codebase)
KEY_FILES = [
    "src/core/packager.ts",
    "src/core/security/securityCheck.ts", 
    "src/core/metrics/TokenCounter.ts",
    "src/core/file/fileProcess.ts",
    "src/cli/cliRun.ts",
    "src/core/treeSitter/parseStrategies/TypeScriptParseStrategy.ts",
    "src/core/git/gitRemoteHandle.ts",
    "src/config/configSchema.ts",
    "src/core/output/outputGenerate.ts",
    "src/core/file/workers/fileProcessWorker.ts"
]

# OCTAVE annotations for each file
OCTAVE_ANNOTATIONS = {
    "src/core/packager.ts": """
===PACKAGER_MODULE===
// Core orchestration module for repomix packing process

META:
  PURPOSE::"Coordinate entire repository packing workflow"
  PATTERN::ORCHESTRATOR
  CRITICALITY::HIGH
  DEPENDENCIES::[fileCollect, fileProcess, securityCheck, outputGenerate]

ARCHITECTURE:
  ROLE::CENTRAL_COORDINATOR
  FLOW::COLLECT->PROCESS->VALIDATE->OUTPUT
  ERROR_STRATEGY::FAIL_FAST
  CONCURRENCY::WORKER_POOLS

PERFORMANCE:
  BOTTLENECKS::[FILE_IO, TOKEN_COUNTING]
  OPTIMIZATION::PARALLEL_PROCESSING
  MEMORY::STREAM_BASED
""",

    "src/core/security/securityCheck.ts": """
===SECURITY_MODULE===
// Security validation for suspicious file detection

META:
  PURPOSE::"Detect and flag potentially dangerous files"
  PATTERN::VALIDATOR
  CRITICALITY::CRITICAL
  THREAT_MODEL::UNTRUSTED_INPUT

SECURITY:
  STRATEGY::DEFENSE_IN_DEPTH
  CHECKS::[PATH_TRAVERSAL, EXEC_FILES, SENSITIVE_DATA]
  CONCURRENCY::WORKER_POOL[4]
  FALSE_POSITIVE_RATE::MINIMIZE
""",

    "src/core/metrics/TokenCounter.ts": """
===TOKEN_COUNTER===
// Performance-critical token counting implementation

META:
  PURPOSE::"Count tokens using tiktoken for LLM compatibility"
  PATTERN::UTILITY
  CRITICALITY::HIGH
  PERFORMANCE_SENSITIVE::true

ALGORITHM:
  METHOD::TIKTOKEN_ENCODING
  MODEL::CL100K_BASE
  FALLBACK::CHARACTER_ESTIMATE
  ERROR_HANDLING::GRACEFUL_DEGRADATION
""",

    "src/core/file/fileProcess.ts": """
===FILE_PROCESSOR===
// Complex file processing pipeline

META:
  PURPOSE::"Process files with comment removal and transformation"
  PATTERN::PIPELINE
  COMPLEXITY::HIGH
  WORKER_ENABLED::true

PIPELINE:
  STAGES::[read->PARSE->TRANSFORM->VALIDATE]
  PARALLELISM::FILE_LEVEL
  ERROR_RECOVERY::SKIP_FAILED
  SUPPORTED_TYPES::[TS, JS, PY, JAVA, CPP]
""",

    "src/cli/cliRun.ts": """
===CLI_INTERFACE===
// Command-line interface and user interaction

META:
  PURPOSE::"Parse commands and orchestrate execution"
  PATTERN::COMMAND_PARSER
  USER_FACING::true
  ERROR_HANDLING::USER_FRIENDLY

INTERFACE:
  COMMANDS::[pack, init, migrate]
  OPTIONS::EXTENSIVE
  VALIDATION::STRICT
  HELP::CONTEXTUAL
""",

    "src/core/treeSitter/parseStrategies/TypeScriptParseStrategy.ts": """
===TS_PARSER_STRATEGY===
// TypeScript-specific AST parsing implementation

META:
  PURPOSE::"Parse TypeScript using tree-sitter for comment removal"
  PATTERN::STRATEGY
  LANGUAGE::TYPESCRIPT
  COMPLEXITY::MEDIUM

PARSING:
  ENGINE::TREE_SITTER
  AST_TRAVERSAL::VISITOR_PATTERN
  COMMENT_TYPES::[LINE, BLOCK, JSDOC]
""",

    "src/core/git/gitRemoteHandle.ts": """
===GIT_REMOTE_HANDLER===
// Remote repository operations with security

META:
  PURPOSE::"Handle GitHub/GitLab remote repo downloads"
  PATTERN::ADAPTER
  SECURITY::HIGH_RISK
  EXTERNAL_DEPS::true

SECURITY:
  URL_VALIDATION::STRICT
  PROTOCOLS::[HTTPS_ONLY]
  ARCHIVE_VALIDATION::CHECKSUM
""",

    "src/config/configSchema.ts": """
===CONFIG_SCHEMA===
// Configuration structure and validation

META:
  PURPOSE::"Define and validate configuration options"
  PATTERN::SCHEMA
  VALIDATION::ZOD
  USER_CONFIGURABLE::true

SCHEMA:
  OUTPUT::FORMAT+OPTIONS
  INCLUDE::GLOB_PATTERNS
  SECURITY::ENABLE_CHECK
""",

    "src/core/output/outputGenerate.ts": """
===OUTPUT_GENERATOR===
// Multi-format output generation engine

META:
  PURPOSE::"Generate final output in various formats"
  PATTERN::TEMPLATE_ENGINE
  FORMATS::[XML, MARKDOWN, PLAIN]
  EXTENSIBLE::true

GENERATION:
  TEMPLATE_BASED::true
  STREAMING::LARGE_FILES
  FORMATTING::CONFIGURABLE
""",

    "src/core/file/workers/fileProcessWorker.ts": """
===FILE_WORKER===
// Worker thread for parallel file processing

META:
  PURPOSE::"Process files in isolated worker thread"
  PATTERN::WORKER
  CONCURRENCY::THREAD_POOL
  PERFORMANCE::CRITICAL

WORKER:
  COMMUNICATION::MESSAGE_PASSING
  ERROR_BOUNDARY::ISOLATED
  TIMEOUT::CONFIGURABLE
"""
}

def process_repomix_file(input_file, output_file):
    """Process Repomix output to add OCTAVE annotations."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    annotated_count = 0
    
    # Process each key file
    for file_path in KEY_FILES:
        # Find the file section - note the closing >
        pattern = f'<file path="{file_path}">'
        
        if pattern in content:
            # Find the position after the file path tag, including newline
            start_pos = content.find(pattern) + len(pattern)
            # Find the newline after the tag
            newline_pos = content.find('\n', start_pos)
            if newline_pos != -1:
                # Insert OCTAVE annotation after the newline
                octave_annotation = OCTAVE_ANNOTATIONS.get(file_path, '')
                if octave_annotation:
                    content = content[:newline_pos+1] + octave_annotation + content[newline_pos+1:]
                    annotated_count += 1
                    print(f"Annotated: {file_path}")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nTotal files annotated: {annotated_count}")
    return annotated_count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python octave_enhance_targeted.py input.xml output.xml")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    if not input_file.exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Process the file
    count = process_repomix_file(input_file, output_file)
    
    print(f"\nTargeted OCTAVE enhancement complete: {output_file}")
    print(f"Files annotated with OCTAVE: {count}/{len(KEY_FILES)}")