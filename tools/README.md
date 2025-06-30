'''
# OCTAVE Tools

This directory contains tools for working with the OCTAVE language.

## `octave_validator.py`

This is a Python-based validator for the OCTAVE language.

**Important:** This script has been updated to check for the current native OCTAVE v1.0 syntax (e.g., `::` assignments, `→` in lists). However, it still has limitations:

*   **Native Format:** The checks are not exhaustive and focus on common errors. They do not represent a complete, formal validation.
*   **JSON Format:** The JSON validation logic is currently a **placeholder**. It only checks for basic JSON well-formedness, not for compliance with the actual [OCTAVE JSON Schema](../json/JSON_SCHEMA.md).

It is provided as a proof-of-concept and a starting point for developing more robust tooling.

### Usage

```bash
python octave_validator.py /path/to/your/document.oct.md
```
'''
