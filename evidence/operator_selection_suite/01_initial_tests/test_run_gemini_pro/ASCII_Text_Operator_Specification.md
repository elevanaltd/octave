# ASCII Text Operator Specification

This document provides the official specification for the ASCII Text Operators in the OCTAVE system.

## Core Operators

*   **Synthesis: `_AND_`**
    *   **Meaning:** Represents a combination or synthesis of two or more elements. It is used when components work together to produce a new outcome.
    *   **Example:** `User_Service _AND_ Auth_Service`
*   **Tension: `_VS_`**
    *   **Meaning:** Represents a tension, conflict, or opposition between two or more elements. It is used to highlight areas where there are trade-offs or competing concerns.
    *   **Example:** `Auth_Service _VS_ Rate_Limiter`
*   **Progress: `_TO_`**
    *   **Meaning:** Represents a flow, sequence, or progression from one element to another. It is used to show the direction of a process or the relationship between stages in a workflow.
    *   **Example:** `Rate_Limiter _TO_ Checkout_Flow`

## Extensibility

The set of operators can be extended by creating new operators with the `_OPERATOR_` format. New operators should be clearly defined and documented before being used.

## Anti-Patterns

*   **Do not use natural language words without underscores.** For example, use `_AND_` instead of `AND`. This is to avoid ambiguity with natural language and to make the operators easy to parse.
*   **Do not create operators that are too similar to existing operators.** New operators should have a clear and distinct meaning.

