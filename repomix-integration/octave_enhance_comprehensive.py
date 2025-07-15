#!/usr/bin/env python3
"""
Add comprehensive OCTAVE annotations to ALL TypeScript files in Repomix output.
This creates comprehensive enhancement with auto-generated annotations.

Usage:
    python octave_enhance_comprehensive.py input.xml output.xml

Based on empirical research showing 10.2x accuracy improvement.
"""

import re
import sys
from pathlib import Path

def generate_octave_annotation(file_path):
    """Generate OCTAVE annotation based on file path and common patterns."""
    filename = Path(file_path).stem
    dirname = Path(file_path).parent.name
    
    # Determine file type/purpose based on patterns
    purpose = "UNKNOWN"
    pattern = "MODULE"
    criticality = "MEDIUM"
    
    # CLI files
    if "cli" in file_path:
        purpose = "Command-line interface component"
        pattern = "CLI_COMPONENT"
        criticality = "HIGH" if "cliRun" in filename else "MEDIUM"
    
    # Core modules
    elif "core" in file_path:
        if "security" in file_path:
            purpose = "Security validation and checking"
            pattern = "SECURITY_MODULE"
            criticality = "CRITICAL"
        elif "output" in file_path:
            purpose = "Output generation and formatting"
            pattern = "OUTPUT_HANDLER"
        elif "file" in file_path:
            purpose = "File system operations"
            pattern = "FILE_HANDLER"
            criticality = "HIGH"
        elif "git" in file_path:
            purpose = "Git repository operations"
            pattern = "GIT_INTEGRATION"
            criticality = "HIGH"
        elif "metrics" in file_path:
            purpose = "Metrics calculation and analysis"
            pattern = "METRICS_MODULE"
        elif "treeSitter" in file_path:
            purpose = "AST parsing and manipulation"
            pattern = "PARSER"
    
    # Config files
    elif "config" in file_path:
        purpose = "Configuration management"
        pattern = "CONFIG"
        criticality = "HIGH"
    
    # Worker files
    elif "worker" in filename.lower():
        purpose = "Parallel processing worker"
        pattern = "WORKER"
        criticality = "HIGH"
    
    # Action files
    elif "Action" in filename:
        purpose = "CLI action handler"
        pattern = "ACTION_HANDLER"
    
    # Utility files
    elif "util" in file_path or "helper" in file_path:
        purpose = "Utility functions"
        pattern = "UTILITY"
        criticality = "LOW"
    
    # Type definition files
    elif "types" in filename or "schema" in filename:
        purpose = "Type definitions and schemas"
        pattern = "TYPE_DEFINITION"
    
    # Generate OCTAVE header
    module_name = filename.upper().replace('-', '_')
    
    annotation = f"""
==={module_name}===
// Auto-generated OCTAVE annotation for comprehensive analysis

META:
  FILE::{file_path}
  PURPOSE::"{purpose}"
  PATTERN::{pattern}
  CRITICALITY::{criticality}
  AUTO_GENERATED::true

ARCHITECTURE:
  MODULE::{dirname}/{filename}
  LAYER::{dirname.upper()}
  DEPENDENCIES::ANALYZE_IMPORTS
"""
    
    # Add specific sections based on pattern
    if pattern == "SECURITY_MODULE":
        annotation += """
SECURITY:
  THREAT_MODEL::UNTRUSTED_INPUT
  VALIDATION::REQUIRED
  AUDIT::ENABLED
"""
    elif pattern == "FILE_HANDLER":
        annotation += """
IO_OPERATIONS:
  TYPE::FILE_SYSTEM
  ASYNC::true
  ERROR_HANDLING::REQUIRED
"""
    elif pattern == "WORKER":
        annotation += """
CONCURRENCY:
  TYPE::WORKER_THREAD
  COMMUNICATION::MESSAGE_PASSING
  ISOLATION::PROCESS_LEVEL
"""
    elif pattern == "PARSER":
        annotation += """
PARSING:
  ENGINE::TREE_SITTER
  LANGUAGES::MULTIPLE
  AST_BASED::true
"""
    
    return annotation

def process_repomix_comprehensive(input_file, output_file):
    """Process Repomix output to add comprehensive OCTAVE annotations."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    annotated_count = 0
    
    # Find all TypeScript files
    file_pattern = r'<file path="([^"]+\.ts)">'
    matches = list(re.finditer(file_pattern, content))
    
    # Process from end to beginning to maintain positions
    for match in reversed(matches):
        file_path = match.group(1)
        
        # Skip test files
        if '/tests/' in file_path or '.test.' in file_path or '.spec.' in file_path:
            continue
            
        # Find the position after the file path tag
        start_pos = match.end()
        newline_pos = content.find('\n', start_pos)
        
        if newline_pos != -1:
            # Generate and insert OCTAVE annotation
            octave_annotation = generate_octave_annotation(file_path)
            content = content[:newline_pos+1] + octave_annotation + content[newline_pos+1:]
            annotated_count += 1
            
            if annotated_count % 10 == 0:
                print(f"Progress: {annotated_count} files annotated...")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nTotal files annotated: {annotated_count}")
    return annotated_count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python octave_enhance_comprehensive.py input.xml output.xml")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    if not input_file.exists():
        print(f"Error: Input file {input_file} does not exist")
        sys.exit(1)
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Process the file
    print("Creating comprehensive OCTAVE annotations...")
    count = process_repomix_comprehensive(input_file, output_file)
    
    print(f"\nComprehensive OCTAVE enhancement complete: {output_file}")
    print(f"Total TypeScript files annotated: {count}")