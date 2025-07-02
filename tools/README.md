'''
# OCTAVE Tools

This directory contains tools for working with the OCTAVE language.

## `octave_validator.py`

This is a Python-based validator for the OCTAVE v2.0 language specification.

**Important:** This script validates the current OCTAVE v2.0 syntax with ASCII operators (e.g., `::` assignments, `->` progressions, `+` synthesis, `_VERSUS_` tensions). It has the following features and limitations:

*   **Native Format:** Validates v2.0 operators and warns about deprecated Unicode operators from v1.0
*   **Operator Validation:** Checks proper usage of `+`, `_VERSUS_`, and `->` operators
*   **Structure Validation:** Validates document structure, indentation, and key formats
*   **JSON Format:** The JSON validation is currently a **placeholder** that only checks for basic JSON well-formedness

It is provided as a proof-of-concept and a starting point for developing more robust tooling.

### Usage

```bash
python octave_validator.py /path/to/your/document.oct.md
```
'''
