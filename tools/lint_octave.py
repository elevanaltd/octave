#!/usr/bin/env python3
"""
Minimal OCTAVE v2.0 validator - 30 lines of essential checks
Returns "OCTAVE_INVALID: <reason>" or "OCTAVE_VALID"
Handles .oct.md, .octave, and .oct files
"""

import re
import sys

def lint_octave(content):
    lines = content.strip().split('\n')
    
    # Check document markers
    if not lines[0].startswith('===') or not lines[-1] == '===END===':
        return "OCTAVE_INVALID: Missing document markers (===NAME=== and ===END===)"
    
    # Check basic syntax
    errors = []
    indent_stack = [0]
    
    for i, line in enumerate(lines[1:-1], 1):
        if not line.strip() or line.strip().startswith('//'):
            continue
            
        # Check indentation (must be 2-space multiples)
        indent = len(line) - len(line.lstrip())
        if indent % 2 != 0:
            errors.append(f"Line {i}: Invalid indent (must be 2-space multiples)")
        
        # Check assignment operator
        if '::' in line and not re.match(r'^\s*[A-Za-z_]\w*::', line):
            errors.append(f"Line {i}: Invalid assignment syntax")
        
        # Check list brackets
        if line.count('[') != line.count(']'):
            errors.append(f"Line {i}: Unbalanced brackets")
        
        # Check for trailing comma in lists
        if re.search(r',\s*\]', line):
            errors.append(f"Line {i}: Trailing comma in list")
    
    return f"OCTAVE_INVALID: {'; '.join(errors)}" if errors else "OCTAVE_VALID"

if __name__ == "__main__":
    content = sys.stdin.read() if not sys.argv[1:] else open(sys.argv[1]).read()
    print(lint_octave(content))