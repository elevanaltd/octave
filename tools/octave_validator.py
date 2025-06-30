#!/usr/bin/env python3
"""
OCTAVE Validator - Simple Implementation

This validator checks OCTAVE-formatted documents for structure and syntax compliance.

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
    """Validator for OCTAVE structured documents, updated for the current spec."""

    def __init__(self, version: str = "1.0.0"):
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

            # Validate operator usage
            if '→' in stripped_line:
                if not (stripped_line.startswith('[') and stripped_line.endswith(']')):
                     self.errors.append(f"Line {line_num}: Progression operator '→' can only be used inside lists (e.g., [A→B→C]).")
            
            if '⊕' in stripped_line:
                if stripped_line.count('⊕') > 1:
                    self.errors.append(f"Line {line_num}: Synthesis operator '⊕' cannot be chained. Use nested structures for complex synthesis.")
            
            if '⚡' in stripped_line:
                if stripped_line.count('⚡') > 1:
                    self.errors.append(f"Line {line_num}: Tension operator '⚡' cannot be chained.")

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


def validate_octave_document(octave_text: str, version: str = "1.0.0") -> str:
    """Validates an OCTAVE document for structure and format."""
    validator = OctaveValidator(version)
    is_valid, messages = validator.validate_octave_document(octave_text)
    return validator.format_results(is_valid, messages)

def validate_octave_file(file_path: str, version: str = "1.0.0") -> str:
    """Validates an OCTAVE document file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            octave_text = f.read()
        return validate_octave_document(octave_text, version)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def main() -> None:
    """Command-line interface for OCTAVE validator."""
    parser = argparse.ArgumentParser(description='Validate OCTAVE documents against the v1.0 specification.')
    parser.add_argument('file', help='Path to OCTAVE document file')
    parser.add_argument('--version', '-v', default='1.0.0', help='OCTAVE version to validate against (currently ignored).')
    
    args = parser.parse_args()
    result = validate_octave_file(args.file, args.version)
    print(result)


if __name__ == "__main__":
    main()