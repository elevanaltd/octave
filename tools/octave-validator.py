#!/usr/bin/env python3
"""
OCTAVE Validator - v2.0 Implementation

This validator checks OCTAVE v2.0 formatted documents for structure and syntax compliance.

Usage:
    python octave_validator.py <file_path>
    # or
    import octave_validator
    result = octave_validator.validate_octave_document(octave_text)
"""

import re
import json
import argparse
from typing import List, Tuple

class OctaveValidator:
    """Validator for OCTAVE v2.0 structured documents."""

    def __init__(self, version: str = "2.0.0"):
        self.version = version
        self.errors = []
        self.warnings = []

    def validate_octave_document(self, document: str) -> Tuple[bool, List[str]]:
        """Validate an OCTAVE document against the specification."""
        self.errors = []
        self.warnings = []

        if document.strip().startswith("{"):
            return self._validate_json_octave(document)
        else:
            return self._validate_native_octave(document)

    def _validate_json_octave(self, document: str) -> Tuple[bool, List[str]]:
        """Placeholder for JSON validation. Full validation requires a JSON Schema validator."""
        try:
            json.loads(document)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON format: {e}")
            return False, self.errors

        self.warnings.append("JSON validation is a stub. For full validation, use a JSON Schema validator against json/JSON_SCHEMA.md.")
        return True, self.warnings

    def _validate_native_octave(self, document: str) -> Tuple[bool, List[str]]:
        """Validate a native-formatted OCTAVE document."""
        lines = document.strip().split('\n')
        in_list = False

        if not lines[0].startswith("===") or not lines[-1].startswith("==="):
            self.errors.append("Document must begin and end with ===DOCUMENT_NAME=== markers.")

        for i, line in enumerate(lines):
            line_num = i + 1
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith("//"):
                continue

            # Check for incorrect assignment operators
            if " = " in line or ": " in line or " :" in line:
                self.errors.append(f"Line {line_num}: Invalid assignment operator. Use '::' with no surrounding spaces.")

            # Validate v2.0 operator usage
            
            # Check for progression operator -> (only allowed in lists)
            if '->' in stripped_line:
                # Check if it's inside a list structure
                if not re.search(r'\[.*->.*\]', stripped_line):
                    self.errors.append(f"Line {line_num}: Progression operator '->' can only be used inside lists (e.g., [A->B->C]).")
            
            # Check for synthesis operator + (cannot be chained)
            if '+' in stripped_line and '::' in stripped_line:
                # Extract the value part after ::
                value_part = stripped_line.split('::', 1)[1] if '::' in stripped_line else stripped_line
                # Count + signs not inside quotes
                plus_count = len(re.findall(r'(?<!")(?<!\w)\+(?!\w)(?!")', value_part))
                if plus_count > 1:
                    self.errors.append(f"Line {line_num}: Synthesis operator '+' cannot be chained. Use nested structures for complex synthesis.")
            
            # Check for tension operator _VERSUS_ (cannot be chained)
            if '_VERSUS_' in stripped_line:
                versus_count = stripped_line.count('_VERSUS_')
                if versus_count > 1:
                    self.errors.append(f"Line {line_num}: Tension operator '_VERSUS_' cannot be chained.")
            
            # Warn about old operators
            if '→' in stripped_line:
                self.warnings.append(f"Line {line_num}: Found old Unicode operator '→'. Use '->' for v2.0.")
            if '⊕' in stripped_line:
                self.warnings.append(f"Line {line_num}: Found old Unicode operator '⊕'. Use '+' for v2.0.")
            if '⚡' in stripped_line:
                self.warnings.append(f"Line {line_num}: Found old Unicode operator '⚡'. Use '_VERSUS_' for v2.0.")

            # Check for incorrect indentation (must be multiple of 2)
            indentation = len(line) - len(line.lstrip(' '))
            if indentation % 2 != 0:
                self.warnings.append(f"Line {line_num}: Indentation is not a multiple of 2 spaces.")

            # Check for tabs
            if '\t' in line:
                self.errors.append(f"Line {line_num}: Tab characters are not allowed. Use spaces for indentation.")

            # Basic key format validation
            if "::" in stripped_line:
                key = stripped_line.split("::")[0]
                if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
                    self.warnings.append(f"Line {line_num}: Key '{key}' may not follow best practices (alphanumeric and underscores, starting with a letter or underscore).")

        return len(self.errors) == 0, self.errors + self.warnings

    def format_results(self, is_valid: bool, messages: List[str]) -> str:
        """Format validation results into a readable string."""
        if is_valid and not self.warnings:
            return "✅ OCTAVE document appears to be valid."
        elif is_valid:
            warning_count = len(self.warnings)
            return f"✅ OCTAVE document is valid but has {warning_count} suggestion{'s' if warning_count > 1 else ''}:\n" + "\n".join([f"  - {w}" for w in self.warnings])
        else:
            error_count = len(self.errors)
            return f"❌ OCTAVE document is invalid with {error_count} error{'s' if error_count > 1 else ''}:\n" + "\n".join([f"  - {e}" for e in self.errors])


def validate_octave_document(octave_text: str, version: str = "2.0.0") -> str:
    """Validates an OCTAVE v2.0 document for structure and format."""
    validator = OctaveValidator(version)
    is_valid, messages = validator.validate_octave_document(octave_text)
    return validator.format_results(is_valid, messages)

def validate_octave_file(file_path: str, version: str = "2.0.0") -> str:
    """Validates an OCTAVE v2.0 document file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            octave_text = f.read()
        return validate_octave_document(octave_text, version)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def main() -> None:
    """Command-line interface for OCTAVE validator."""
    parser = argparse.ArgumentParser(description='Validate OCTAVE documents against the v2.0 specification.')
    parser.add_argument('file', help='Path to OCTAVE document file')
    parser.add_argument('--version', '-v', default='2.0.0', help='OCTAVE version to validate against (default: 2.0.0)')
    
    args = parser.parse_args()
    result = validate_octave_file(args.file, args.version)
    print(result)


if __name__ == "__main__":
    main()